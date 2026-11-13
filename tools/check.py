"""Contrôles du site (aucune dépendance, Python 3.9+).

    python tools/check.py             contrôle les fichiers générés ; code 1 au premier défaut
    python tools/check.py --selftest  réintroduit chaque défaut connu et vérifie qu'il est vu

Ce que ces contrôles tiennent : pages à jour par rapport à src/, aucune ressource
chez un tiers, aucun style ni script en ligne, liens internes et ancres valides,
un seul titre principal, voix d'Audric (pas de tiret long, pas de formule interdite),
décisions du 13/11/2026 (ni « mandat légal », ni article 1984, ni « conforme », ni
« opposable » dans les pages nouvelles), démonstration réellement signée.
"""

import base64
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402

DASHES = ("—", "–", "…")
# Formules que la voix d'Audric interdit, partout.
VOICE = ("n'hésitez pas", "n’hésitez pas", "je me permets", "je serais ravi", "thermaliste", "startup",
         "au cœur de", "dans le cadre de", "par ailleurs")
# Décisions du 13/11/2026 et règles du Cap AMR, sur les pages nouvelles (pas les articles repris).
DECISIONS = ("mandat légal", "mandats légaux", "autorité légale", "art_1984", "article 1984", "legal mandate",
             "legal authority", "opposable", "conforme ai act", "compatible eidas", "ai act compliant",
             # 13/11/2026 au soir : le mandat est l'écrit d'une personne, jamais celui de l'agent
             "mandat de l'agent", "mandat donné à l'agent", "mandat donné à un agent", "mandataire",
             "agent's mandate", "mandate given to the agent", "mandate holder")
# La définition de « mandat » doit rester sur l'accueil, dans les deux langues.
DEFINITION = {"index.html": ("def_mandat", "au sens du code civil"),
              "en/index.html": ("def_mandat_en", "in the legal sense")}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.ids = []
        self.links = []
        self.resources = []
        self.inline = []
        self.lang = None
        self.title = ""
        self.desc = None
        self.canonical = None
        self.text = []
        self._stack = []
        self.noalt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._stack.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if "id" in a:
            self.ids.append(a["id"])
        if "style" in a:
            self.inline.append(f"attribut style sur <{tag}>")
        if tag == "style":
            self.inline.append("balise <style>")
        if tag == "script":
            if a.get("src"):
                self.resources.append(a["src"])
            elif a.get("type") not in ("application/ld+json", "application/json"):
                self.inline.append("script en ligne")
        if tag == "link":
            rel = a.get("rel", "")
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel not in ("alternate",):
                self.resources.append(a.get("href", ""))
        if tag in ("img", "source", "iframe", "video", "audio"):
            self.resources.append(a.get("src", ""))
            if tag == "img" and "alt" not in a:
                self.noalt += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        for key, value in attrs:
            if key.startswith("on"):
                self.inline.append(f"gestionnaire {key} en ligne")

    def handle_endtag(self, tag):
        while self._stack and self._stack.pop() != tag:
            pass

    def handle_data(self, data):
        if "title" in self._stack[-1:]:
            self.title += data
        if not {"script", "style", "pre", "code", "template"} & set(self._stack):
            self.text.append(data)


def parse(content):
    page = Page()
    page.feed(content)
    return page


def target_file(path, files):
    path = path.split("#")[0].split("?")[0]
    if path.endswith("/"):
        name = (path + "index.html").lstrip("/")
    else:
        name = path.lstrip("/")
        if name not in files:
            name += ".html"
    return name if name in files else None


# --- Ed25519 (RFC 8032), vérification seule, pour ne dépendre de rien -------------
P = 2**255 - 19
L = 2**252 + 27742317777372353535851937790883648493
D = -121665 * pow(121666, P - 2, P) % P
I = pow(2, (P - 1) // 4, P)


def _recover_x(y, sign):
    x2 = (y * y - 1) * pow(D * y * y + 1, P - 2, P) % P
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P:
        x = x * I % P
    if (x * x - x2) % P:
        return None
    return P - x if (x & 1) != sign else x


def _add(a, b):
    x1, y1, z1, t1 = a
    x2, y2, z2, t2 = b
    aa = (y1 - x1) * (y2 - x2) % P
    bb = (y1 + x1) * (y2 + x2) % P
    cc = 2 * t1 * t2 * D % P
    dd = 2 * z1 * z2 % P
    e, f, g, h = bb - aa, dd - cc, dd + cc, bb + aa
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def _mul(k, point):
    acc = (0, 1, 1, 0)
    while k:
        if k & 1:
            acc = _add(acc, point)
        point = _add(point, point)
        k >>= 1
    return acc


def _decode(raw):
    y = int.from_bytes(raw, "little")
    sign, y = y >> 255, y & ((1 << 255) - 1)
    x = _recover_x(y, sign) if y < P else None
    return None if x is None else (x, y, 1, x * y % P)


def ed25519_verify(public, message, signature):
    if len(public) != 32 or len(signature) != 64:
        return False
    a, r = _decode(public), _decode(signature[:32])
    s = int.from_bytes(signature[32:], "little")
    if a is None or r is None or s >= L:
        return False
    h = int.from_bytes(hashlib.sha512(signature[:32] + public + message).digest(), "little") % L
    by = 4 * pow(5, P - 2, P) % P
    base = (_recover_x(by, 0), by, 1, _recover_x(by, 0) * by % P)
    left, right = _mul(s, base), _add(r, _mul(h, a))
    return (left[0] * right[2] - right[0] * left[2]) % P == 0 and (left[1] * right[2] - right[1] * left[2]) % P == 0


def b64u(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def check_demo(jws, key, demo, today):
    errors = []
    try:
        head, payload, sig = jws.strip().split(".")
        header = json.loads(b64u(head))
        good = (header.get("alg") == "EdDSA" and header.get("kid") == key["jwk"]["kid"]
                and ed25519_verify(b64u(key["jwk"]["x"]), f"{head}.{payload}".encode(), b64u(sig)))
    except Exception:
        good = False
    if not good:
        return ["démonstration : la signature de registry-snapshot.jws ne correspond pas à registry-key.json"]
    mandates = {m["id"]: m for m in json.loads(b64u(payload))["amr_public_registry"]["mandates"]}
    return demo_content(mandates, demo, today)


def demo_content(mandates, demo, today):
    """Ce que la démonstration doit montrer, une fois la signature du registre vérifiée."""
    errors = []
    active, revoked = mandates.get(demo["mandate_id"]), mandates.get(demo["revoked_mandate_id"])
    for mandate in (active, revoked):
        if not mandate:
            continue
        if not mandate.get("principal_signed"):
            errors.append(f"démonstration : le mandat {mandate['id'][:8]} n'est pas signé par son mandant")
        announced = demo.get("announced_principals", {}).get(mandate["id"], "")
        if "sha256:" + hashlib.sha256(announced.encode()).hexdigest() != mandate.get("principal_ref"):
            errors.append(f"démonstration : le mandant annoncé pour {mandate['id'][:8]} ne correspond pas "
                          "à l'empreinte du registre")
    if not active or active["revoked_at"] or active["recorded_status"] != "active":
        errors.append("démonstration : le mandat actif n'est pas actif dans l'instantané")
    elif datetime.fromisoformat(active["expires_at"]) < today + timedelta(days=45):
        errors.append("démonstration : le mandat actif expire dans moins de 45 jours, relancer tools/make_demo_registry.py")
    if not revoked or not revoked["revoked_at"]:
        errors.append("démonstration : le mandat retiré n'est pas retiré dans l'instantané")
    if sum(1 for c in demo["cases"] if c["issued"]) < 1 or sum(1 for c in demo["cases"] if not c["issued"]) < 1:
        errors.append("démonstration : il faut au moins une action autorisée et une action refusée")
    return errors


def check(files, fresh, demo_files, today=None):
    """files : nom -> contenu sur le disque ; fresh : nom -> contenu que src/ produit maintenant."""
    today = today or datetime.now(timezone.utc)
    errors = []
    for name, content in fresh.items():
        if files.get(name) != content:
            errors.append(f"{name} : pas à jour par rapport à src/ (python tools/build.py)")
    shapes = {page[2]: page[5] for page in build.PAGES}
    pages = {name: parse(content) for name, content in files.items() if name.endswith(".html")}
    for name, page in pages.items():
        text = " ".join(page.text)
        low = text.lower()
        if page.h1 != 1:
            errors.append(f"{name} : {page.h1} titre(s) principal(aux), il en faut un seul")
        if page.lang not in ("fr", "en"):
            errors.append(f"{name} : langue du document absente")
        if not page.title.strip():
            errors.append(f"{name} : titre de page vide")
        if not page.desc or not 50 <= len(page.desc) <= 175:
            errors.append(f"{name} : description absente ou hors 50 à 175 caractères")
        if name != "404.html" and not page.canonical:
            errors.append(f"{name} : adresse canonique absente")
        for item in page.inline:
            errors.append(f"{name} : {item} (interdit par la politique de sécurité du site)")
        if page.noalt:
            errors.append(f"{name} : image sans texte de remplacement")
        if len(page.ids) != len(set(page.ids)):
            errors.append(f"{name} : identifiant en double")
        for res in page.resources:
            if not res.startswith("/") or res.startswith("//"):
                errors.append(f"{name} : ressource chargée hors du site ({res})")
            elif not (ROOT / res.lstrip("/")).exists():
                errors.append(f"{name} : ressource introuvable ({res})")
        for href in page.links:
            if href.startswith(("mailto:", "https://")):
                continue
            if href.startswith("http://data.europa.eu/eli/"):
                continue  # identifiant européen de la législation : son adresse officielle est en http
            if href.startswith("http://"):
                errors.append(f"{name} : lien non chiffré ({href})")
                continue
            if href.startswith("#"):
                if href[1:] not in page.ids:
                    errors.append(f"{name} : ancre introuvable ({href})")
                continue
            if not href.startswith("/"):
                errors.append(f"{name} : lien relatif ({href}), écrire une adresse qui commence par /")
                continue
            if href.endswith((".txt", ".xml", ".jws", ".json", ".pem", ".png", ".svg")):
                if href.lstrip("/") not in files and not (ROOT / href.lstrip("/")).exists():
                    errors.append(f"{name} : fichier introuvable ({href})")
                continue
            dest = target_file(href, files)
            if dest is None:
                errors.append(f"{name} : lien interne cassé ({href})")
            elif "#" in href and href.split("#")[1] not in pages[dest].ids:
                errors.append(f"{name} : ancre introuvable ({href})")
        for phrase in VOICE:
            if phrase in low:
                errors.append(f"{name} : formule interdite par la voix d'Audric (« {phrase} »)")
        if shapes.get(name) != "article":
            for mark in DASHES:
                if mark in text:
                    errors.append(f"{name} : tiret long ou points de suspension typographiques ({mark!r})")
            for phrase in DECISIONS:
                if phrase in low.replace("’", "'"):
                    errors.append(f"{name} : formulation écartée par décision (« {phrase} »)")
        if name in DEFINITION:
            fact, marker = DEFINITION[name]
            plain = " ".join(low.replace("\u00a0", " ").replace("\u202f", " ").split())
            if build.FACTS[fact].lower() not in plain or marker not in plain:
                errors.append(f"{name} : la définition de « mandat » décidée le 13/11/2026 est absente")
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    if re.search(r"@import|url\(\s*[\"']?(https?:)?//", css):
        errors.append("assets/site.css : ressource chargée hors du site")
    for font in re.findall(r'url\("(/assets/fonts/[^"]+)"\)', css):
        if not (ROOT / font.lstrip("/")).exists():
            errors.append(f"assets/site.css : police introuvable ({font})")
    sitemap = files.get("sitemap.xml", "")
    for pid, lang, out, *_ in build.PAGES:
        if pid != "notfound" and f"{build.SITE}{build.URL[(pid, lang)]}</loc>" not in sitemap:
            errors.append(f"sitemap.xml : page absente ({out})")
    errors += check_demo(demo_files["jws"], demo_files["key"], demo_files["demo"], today)
    try:
        headers = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))["headers"][0]["headers"]
        if not any(h["key"] == "Content-Security-Policy" and "default-src 'self'" in h["value"] for h in headers):
            errors.append("vercel.json : politique de sécurité du contenu absente")
    except Exception as exc:
        errors.append(f"vercel.json : illisible ({exc})")
    return errors


def on_disk():
    fresh = build.outputs()
    files = {name: (ROOT / name).read_text(encoding="utf-8") if (ROOT / name).exists() else None for name in fresh}
    demo = {"jws": (ROOT / "assets/demo/registry-snapshot.jws").read_text(encoding="utf-8"),
            "key": json.loads((ROOT / "assets/demo/registry-key.json").read_text(encoding="utf-8")),
            "demo": json.loads((ROOT / "assets/demo/lock-demo.json").read_text(encoding="utf-8"))}
    return files, fresh, demo


def selftest():
    """Chaque défaut est réintroduit un par un ; le contrôle doit le voir."""
    files, fresh, demo = on_disk()
    base = check(files, fresh, demo)
    if base:
        print("Le site a déjà des défauts, corriger d'abord :", *base, sep="\n  ")
        return 1
    home = files["index.html"]

    def both(change):
        """Le défaut est dans src/ et dans la page : seul le contrôle visé doit le voir."""
        f, g = dict(files), dict(fresh)
        f["index.html"] = g["index.html"] = change(home)
        return f, g, demo

    def stale():
        f = dict(files)
        f["index.html"] = home.replace("Pas de mandat valide", "Pas de mandat")
        return f, fresh, demo

    def forged():
        head, payload, sig = demo["jws"].strip().split(".")
        text = b64u(payload).decode().replace('"max_amount":"100"', '"max_amount":"100000"')
        text = text.replace('"max_amount": "100"', '"max_amount": "100000"')
        forged_payload = base64.urlsafe_b64encode(text.encode()).decode().rstrip("=")
        return files, fresh, dict(demo, jws=f"{head}.{forged_payload}.{sig}")

    cases = [
        ("page modifiée à la main sans passer par src/", "pas à jour", stale),
        ("police chargée chez Google", "hors du site",
         lambda: both(lambda h: h.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend"></head>'))),
        ("style en ligne", "attribut style", lambda: both(lambda h: h.replace('<p class="sub">', '<p class="sub" style="color:red">'))),
        ("script en ligne", "script en ligne", lambda: both(lambda h: h.replace("</body>", "<script>alert(1)</script></body>"))),
        ("lien interne cassé", "lien interne cassé", lambda: both(lambda h: h.replace('href="/verifier"', 'href="/verifer"', 1))),
        ("ancre disparue", "ancre introuvable", lambda: both(lambda h: h.replace('id="questions"', 'id="question"'))),
        ("tiret long dans un texte nouveau", "tiret long", lambda: both(lambda h: h.replace("AMR est ce mécanisme.", "AMR — ce mécanisme."))),
        ("retour de « mandat légal »", "écartée par décision", lambda: both(lambda h: h.replace("AMR est ce mécanisme.", "AMR crée un mandat légal."))),
        ("retour de « opposable »", "écartée par décision", lambda: both(lambda h: h.replace("AMR est ce mécanisme.", "Le mandat est opposable."))),
        ("retour du « mandat de l'agent »", "écartée par décision", lambda: both(lambda h: h.replace("AMR est ce mécanisme.", "Le mandat de l'agent est vérifié."))),
        ("définition de « mandat » retirée de l'accueil", "définition de « mandat »",
         lambda: both(lambda h: h.replace("au sens du Code civil", "au sens strict"))),
        ("mandant annoncé qui n'est pas celui du registre", "ne correspond pas à l'empreinte",
         lambda: (files, fresh, dict(demo, demo=dict(demo["demo"], announced_principals={
             k: "org:une-autre-clinique" for k in demo["demo"]["announced_principals"]})))),
        ("formule de machine", "voix d'Audric", lambda: both(lambda h: h.replace("AMR est ce mécanisme.", "N'hésitez pas à m'écrire."))),
        ("second titre principal", "titre(s) principal", lambda: both(lambda h: h.replace("<h2>Quatre temps", "<h1>Quatre temps").replace("dans cet ordre</h2>", "dans cet ordre</h1>"))),
        ("instantané falsifié (plafond 100 000 €)", "signature", forged),
        ("démonstration proche de l'expiration", "expire dans moins de 45 jours",
         lambda: (files, fresh, demo)),
    ]
    failed = 0
    for label, expected, make in cases:
        f, g, d = make()
        today = datetime(2027, 10, 15, tzinfo=timezone.utc) if "expiration" in label else None
        found = check(f, g, d, today)
        seen = any(expected in e for e in found)
        print(("vu      " if seen else "NON VU  ") + label)
        failed += 0 if seen else 1
    # L'instantané est signé par le registre : pour éprouver le contrôle « signé par son mandant »
    # sans casser cette signature, on retire la signature du mandant dans la copie déjà décodée.
    mandates = {m["id"]: dict(m, principal_signed=False)
                for m in json.loads(b64u(demo["jws"].split(".")[1]))["amr_public_registry"]["mandates"]}
    seen = any("pas signé par son mandant" in e
               for e in demo_content(mandates, demo["demo"], datetime.now(timezone.utc)))
    print(("vu      " if seen else "NON VU  ") + "mandat de démonstration non signé par son mandant")
    failed += 0 if seen else 1
    total = len(cases) + 1
    print(f"{total - failed} défauts réintroduits sur {total} détectés")
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    files, fresh, demo = on_disk()
    errors = check(files, fresh, demo)
    if errors:
        print(f"{len(errors)} défaut(s) :", *errors, sep="\n  ")
        return 1
    print(f"Contrôles passés : {len([n for n in files if n.endswith('.html')])} pages, liens, ressources, voix, "
          "décisions, signature de la démonstration.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
