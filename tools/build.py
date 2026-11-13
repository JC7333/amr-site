"""Génère le site mandatia.eu à partir de src/ (aucune dépendance, Python 3.9+).

    python tools/build.py          écrit les pages à la racine du dépôt
    python tools/build.py --check  n'écrit rien, échoue si une page n'est pas à jour

Une seule source par chose : les chiffres dans src/data/facts.json, les outils
dans src/data/tools.json, les gabarits dans src/data/gabarits.json, les questions
dans src/data/faq.json, la démonstration dans assets/demo/ (tools/make_demo_registry.py).
Ne jamais modifier à la main un fichier .html de la racine ou de en/ : modifier
src/, puis relancer ce script.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE = "https://www.mandatia.eu"
REPO = "https://github.com/JC7333/amr"
MAIL = "audric@mandatia.eu"


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


FACTS = load("src/data/facts.json")
TOOLS = load("src/data/tools.json")
GABARITS = load("src/data/gabarits.json")
FAQ = load("src/data/faq.json")
DEMO = load("assets/demo/lock-demo.json")
FACTS["tools_count"] = sum(len(g["tools"]) for g in TOOLS)
FACTS["templates_count"] = len(GABARITS)
FACTS["demo_date"] = "/".join(reversed(DEMO["generated_on"].split("-")))
MONTHS = "January February March April May June July August September October November December".split()
_y, _m, _d = DEMO["generated_on"].split("-")
FACTS["demo_date_en"] = f"{int(_d)} {MONTHS[int(_m) - 1]} {_y}"
FACTS["demo_mandate_id"] = DEMO["mandate_id"]
FACTS["demo_revoked_id"] = DEMO["revoked_mandate_id"]

# id, langue, fichier de sortie, source, clé de menu, forme, titre, description
PAGES = [
    ("home", "fr", "index.html", "fr/index.html", "", "plain",
     "AMR : pas de mandat valide, pas d'action",
     "AMR est un registre open source où un agent IA ne peut rien faire tant qu'une personne ou un organe ne l'a pas autorisé par écrit. Un tiers le vérifie en quelques secondes."),
    ("home", "en", "en/index.html", "en/index.html", "", "plain",
     "AMR: no valid mandate, no action",
     "AMR is an open-source registry where an AI agent can do nothing until a person or a body has authorized it in writing. A third party checks it in seconds."),
    ("verify", "fr", "verifier.html", "fr/verifier.html", "verify", "plain",
     "Vérifier un mandat | AMR",
     "Vérifiez dans votre navigateur un mandat du registre de démonstration : signature du registre, périmètre, statut. Sans compte, sans rien envoyer."),
    ("verify", "en", "en/verify.html", "en/verify.html", "verify", "plain",
     "Verify a mandate | AMR",
     "Check a mandate of the demonstration registry in your browser: registry signature, perimeter, status. No account, nothing sent."),
    ("templates", "fr", "gabarits.html", "fr/gabarits.html", "templates", "plain",
     "Gabarits de mandat par métier | AMR",
     "Cinq mandats types écrits dans le code d'AMR : santé, recrutement, crédit, assurance vie et santé, service client. Ce que l'agent peut faire, ce qu'il ne peut jamais faire."),
    ("templates", "en", "en/templates.html", "en/templates.html", "templates", "plain",
     "Mandate templates by trade | AMR",
     "Five mandate templates written into the AMR code: healthcare, recruitment, credit, life and health insurance, customer support. What the agent may do and may never do."),
    ("install", "fr", "installer.html", "fr/installer.html", "install", "plain",
     "Installer AMR, pour agents et développeurs | AMR",
     "Une commande pour installer AMR, les profils d'outils par rôle et la référence des outils MCP, chacun avec ses limites."),
    ("install", "en", "en/install.html", "en/install.html", "install", "plain",
     "Install AMR, for agents and developers | AMR",
     "One command to install AMR, tool profiles by role and the reference of the MCP tools, each with its limits."),
    ("brief", "fr", "essentiel.html", "fr/essentiel.html", "", "plain",
     "AMR, l'essentiel en une page",
     "Une page à imprimer ou à transmettre : ce qu'est AMR, ce qu'il fait, ce qu'il ne fait pas, comment l'essayer."),
    ("brief", "en", "en/brief.html", "en/brief.html", "", "plain",
     "AMR in one page",
     "One page to print or forward: what AMR is, what it does, what it does not do, how to try it."),
    ("why", "fr", "pourquoi-autorisation-prospective.html", "fr/pourquoi-autorisation-prospective.html", "", "article",
     "Pourquoi l'autorisation prospective | AMR",
     "Petit traité sur la différence entre prouver après et autoriser avant."),
    ("compliance", "fr", "pour-compliance-officers.html", "fr/pour-compliance-officers.html", "", "article",
     "Pour les compliance officers | AMR",
     "Ce qu'AMR change au quotidien quand vous devez encadrer le déploiement d'agents IA."),
    ("eulaw", "fr", "ia-agentique-droit-union.html", "fr/ia-agentique-droit-union.html", "", "article",
     "L'IA agentique dans le droit de l'Union | AMR",
     "Depuis l'été 2026, le règlement sur l'IA nomme l'IA agentique. Le texte, cité à la lettre, et ce qu'il ne dit pas."),
    ("eulaw", "en", "en/agentic-ai-eu-law.html", "en/agentic-ai-eu-law.html", "", "article",
     "Agentic AI in EU law | AMR",
     "Since summer 2026, the AI Act names agentic AI. The text, quoted word for word, and what it does not say."),
    ("legal", "fr", "mentions-legales.html", "fr/mentions-legales.html", "", "article",
     "Mentions légales | AMR", "Éditeur, hébergeur, licence et données personnelles du site mandatia.eu."),
    ("legal", "en", "en/legal-notice.html", "en/legal-notice.html", "", "article",
     "Legal notice | AMR", "Publisher, host, licence and personal data of the mandatia.eu website."),
    ("notfound", "fr", "404.html", "fr/404.html", "", "plain",
     "Page introuvable | AMR", "Cette page n'existe pas ou n'existe plus. Retour à l'accueil de mandatia.eu."),
]

URL = {}
for pid, lang, out, *_ in PAGES:
    path = "/" + out[: -len(".html")]
    path = path[: -len("index")] if path.endswith("/index") else path
    URL[(pid, lang)] = path


def url(pid, lang):
    """Adresse de la page dans cette langue, sinon dans l'autre."""
    return URL.get((pid, lang)) or URL[(pid, "fr")]


T = {
    "fr": {
        "skip": "Aller au contenu", "home": "Accueil AMR", "menu": "Menu",
        "nav": [("how", "/#fonctionnement", "Fonctionnement"), ("verify", url("verify", "fr"), "Vérifier"),
                ("templates", url("templates", "fr"), "Gabarits"), ("install", url("install", "fr"), "Installer"),
                ("faq", "/#questions", "Questions")],
        "write": "M'écrire", "other": "English",
        "tagline": "Le registre où un agent IA ne peut rien faire tant qu'un mandat ne l'a pas autorisé.",
        "who": "Audric BUGNARD, médecin à Aix-les-Bains",
        "cols": [
            ("Comprendre", [("/#fonctionnement", "Fonctionnement"), ("/#questions", "Questions"),
                            (url("brief", "fr"), "L'essentiel en une page"),
                            (url("why", "fr"), "Pourquoi autoriser avant"),
                            (url("compliance", "fr"), "Pour les responsables conformité"),
                            (url("eulaw", "fr"), "L'IA agentique dans le droit de l'Union")]),
            ("Utiliser", [(url("verify", "fr"), "Vérifier un mandat"), (url("templates", "fr"), "Gabarits"),
                          (url("install", "fr"), "Installer"), (url("install", "fr") + "#outils", "Les {tools_count} outils"),
                          (REPO, "Code sur GitHub"), ("https://pypi.org/project/mandatia/", "Paquet sur PyPI")]),
            ("Le site", [(url("legal", "fr"), "Mentions légales"), ("/llms.txt", "llms.txt, pour les agents"),
                         ("https://github.com/JC7333/amr-site", "Source de ce site")]),
        ],
        "legal": "Open source, licence Apache-2.0. Ce site ne dépose aucun cookie et ne charge rien chez un tiers.",
        "updated": "Mis à jour le {site_date}",
    },
    "en": {
        "skip": "Skip to content", "home": "AMR home", "menu": "Menu",
        "nav": [("how", "/en/#how", "How it works"), ("verify", url("verify", "en"), "Verify"),
                ("templates", url("templates", "en"), "Templates"), ("install", url("install", "en"), "Install"),
                ("faq", "/en/#questions", "Questions")],
        "write": "Write to me", "other": "Français",
        "tagline": "The registry where an AI agent can do nothing until a mandate has authorized it.",
        "who": "Audric BUGNARD, physician in Aix-les-Bains, France",
        "cols": [
            ("Understand", [("/en/#how", "How it works"), ("/en/#questions", "Questions"),
                            (url("brief", "en"), "AMR in one page"),
                            (url("eulaw", "en"), "Agentic AI in EU law"),
                            (url("why", "fr"), "Why authorize before (in French)"),
                            (url("compliance", "fr"), "For compliance officers (in French)")]),
            ("Use", [(url("verify", "en"), "Verify a mandate"), (url("templates", "en"), "Templates"),
                     (url("install", "en"), "Install"), (url("install", "en") + "#tools", "The {tools_count} tools"),
                     (REPO, "Code on GitHub"), ("https://pypi.org/project/mandatia/", "Package on PyPI")]),
            ("This site", [(url("legal", "en"), "Legal notice"), ("/llms.txt", "llms.txt, for agents"),
                           ("https://github.com/JC7333/amr-site", "Source of this site")]),
        ],
        "legal": "Open source, Apache-2.0 licence. This site sets no cookie and loads nothing from a third party.",
        "updated": "Updated {site_date_en}",
    },
}

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18" fill="#0b3436"/>'
        '<circle cx="20" cy="20" r="14.2" fill="none" stroke="#e3b04b" stroke-width="1.1"/>'
        '<path d="M12.8 20.6l5 4.6 9.4-10.6" fill="none" stroke="#fff" stroke-width="2.8" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON = {
    "ok": ('<svg class="mark" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#1b6e44"/>'
           '<path d="M7 12.4l3.3 3.2L17 8.6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" '
           'stroke-linejoin="round"/></svg>'),
    "no": ('<svg class="mark" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#a0372a"/>'
           '<path d="M8 8l8 8M16 8l-8 8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>'),
    "idle": ('<svg class="mark" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" '
             'stroke="#4c6466" stroke-width="2"/><path d="M12 7v5.5l3.2 2" fill="none" stroke="#4c6466" '
             'stroke-width="2" stroke-linecap="round"/></svg>'),
}


def esc(text):
    return html.escape(str(text), quote=True)


def fill(text):
    """Remplace {{f:clé}} par la valeur de facts.json ; une clé inconnue arrête tout."""
    def one(match):
        key = match.group(1)
        if key not in FACTS:
            raise SystemExit(f"fait inconnu : {key}")
        return esc(FACTS[key])
    return re.sub(r"\{\{f:([a-z_]+)\}\}", one, text)


def duration(seconds, lang):
    if seconds % 60 == 0:
        n = seconds // 60
        return f"{n} minute{'s' if n > 1 else ''}"
    return f"{seconds} secondes" if lang == "fr" else f"{seconds} seconds"


def verdict(case, lang):
    if case["issued"]:
        base = ("Autorisé. Jeton valable " if lang == "fr" else "Allowed. Token valid for ") + duration(case["lifetime_seconds"], lang)
        if case["registry_check"]:
            base += ", à revérifier au moment d'agir" if lang == "fr" else ", to be re-checked when acting"
        return base + "."
    detail = case.get("detail", "")
    if detail.startswith("amount_above_limit:"):
        amount = detail.split(":", 1)[1].replace(" EUR", "")
        return (f"Refusé. Le mandat plafonne une commande à {amount} €." if lang == "fr"
                else f"Refused. The mandate caps an order at €{amount}.")
    if detail.startswith("forbidden:"):
        return "Refusé. Le mandat l'interdit." if lang == "fr" else "Refused. The mandate forbids it."
    return "Refusé. Cette action n'est pas dans le mandat." if lang == "fr" else "Refused. This action is not in the mandate."


def block_lockdemo(lang):
    fr = lang == "fr"
    rows = []
    for case in DEMO["cases"]:
        kind = "ok" if case["issued"] else "no"
        raw = json.dumps(case["response"], ensure_ascii=False, indent=2)
        rows.append(
            f'<li><details class="try try-{kind}"><summary>{ICON[kind]}'
            f'<span class="what">{esc(case[lang])}</span>'
            f'<span class="verdict">{esc(verdict(case, lang))}</span></summary>'
            f"<pre>{esc(raw)}</pre></details></li>")
    title = ("Un assistant de secrétariat médical demande cinq actions" if fr
             else "A medical front-desk assistant asks for five actions")
    sub = ("Son mandat : lire le dossier, proposer des rendez-vous, rédiger, commander jusqu'à 100 €. Jamais prescrire ni écrire à un patient."
           if fr else "Its mandate: read the record, propose appointments, draft, order up to €100. Never prescribe or write to a patient.")
    foot = (f"Réponses réelles du registre AMR, produites le {FACTS['demo_date']} sur un mandat de démonstration. "
            "Ouvrez une ligne pour lire la réponse brute." if fr else
            f"Real answers of the AMR registry, produced on {FACTS['demo_date_en']} on a demonstration mandate. "
            "Open a line to read the raw answer.")
    return (f'<aside class="gate" aria-labelledby="gate-t"><div class="gate-head">{LOGO}'
            f'<div><h2 id="gate-t">{title}</h2><p>{sub}</p></div></div>'
            f'<ul class="tries">{"".join(rows)}</ul><p class="gate-foot">{foot}</p></aside>')


def block_tools(lang):
    out = []
    for group in TOOLS:
        items = "".join(
            f'<li><span class="tool">{esc(t["name"])}</span><div>{"".join(f"<p>{p}</p>" for p in t[lang])}</div></li>'
            for t in group["tools"])
        out.append(f'<section class="toolgroup" id="{group["id"]}"><h3>{esc(group[lang])}</h3>'
                   f'<ul class="tools">{items}</ul></section>')
    return "".join(out)


def block_gabarits(lang):
    labels = {"fr": ("Peut", "Ne peut jamais", "Plafonds et règles", "Limite connue", "Documentation du gabarit"),
              "en": ("May", "May never", "Ceilings and rules", "Known limit", "Template documentation")}[lang]
    out = []
    for g in GABARITS:
        d = g[lang]
        may = "".join(f"<li>{x}</li>" for x in d["may"])
        never = "".join(f"<li>{x}</li>" for x in d["never"])
        rules = "".join(f"<p>{x}</p>" for x in d["rules"])
        limit = "".join(f"<p>{x}</p>" for x in d["limit"])
        out.append(
            f'<section class="gabarit" id="{g["id"]}"><h2>{d["title"]}</h2>'
            f'<p class="id"><code>{g["id"]}</code> · <a href="{REPO}/blob/main/docs/templates/{g["id"]}.md">{labels[4]}</a></p>'
            f'<div class="cells"><div><h4>{ICON["ok"]}{labels[0]}</h4><ul>{may}</ul></div>'
            f'<div><h4>{ICON["no"]}{labels[1]}</h4><ul>{never}</ul></div>'
            f"<div><h4>{labels[2]}</h4>{rules}</div><div><h4>{labels[3]}</h4>{limit}</div></div></section>")
    return "".join(out)


def block_gabarits_teaser(lang):
    go = "Voir la fiche" if lang == "fr" else "See the sheet"
    rows = "".join(
        f'<li><a href="{url("templates", lang)}#{g["id"]}"><span class="name">{g[lang]["title"]}</span>'
        f'<span>{g[lang]["teaser"]}</span><span class="go">{go}</span></a></li>' for g in GABARITS)
    return f'<ul class="rows">{rows}</ul>'


def block_faq(lang):
    return '<div class="faq">' + "".join(
        f'<details id="{q["id"]}"><summary>{q[lang]["q"]}</summary><div class="answer">'
        f'{"".join(f"<p>{p}</p>" for p in q[lang]["a"])}</div></details>' for q in FAQ) + "</div>"


def block_lockdemo_list(lang):
    items = "".join(
        f'<li>{ICON["ok" if c["issued"] else "no"]}<span><strong>{esc(c[lang])}.</strong> {esc(verdict(c, lang))}</span></li>'
        for c in DEMO["cases"])
    return f'<ul class="ticks">{items}</ul>'


BLOCKS = {"lockdemo": block_lockdemo, "lockdemo_list": block_lockdemo_list, "tools": block_tools, "gabarits": block_gabarits,
          "gabarits_teaser": block_gabarits_teaser, "faq": block_faq}


def strip_tags(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def jsonld(pid, lang):
    if pid != "home":
        return ""
    app = {
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": "AMR (Agent Mandate Registry)", "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Linux, macOS, Windows", "url": SITE + url("home", lang),
        "license": "https://www.apache.org/licenses/LICENSE-2.0", "softwareVersion": FACTS["pypi_version"],
        "codeRepository": REPO, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "author": {"@type": "Person", "name": "Audric Bugnard"},
        "description": next(p[7] for p in PAGES if p[0] == "home" and p[1] == lang),
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q[lang]["q"]),
         "acceptedAnswer": {"@type": "Answer", "text": " ".join(strip_tags(fill(p)) for p in q[lang]["a"])}} for q in FAQ]}
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (app, faq))


SKIP_TYPO = {"pre", "code", "script", "style", "template", "textarea"}


def typo_fr(markup):
    """Espaces insécables du français, hors balises, code et scripts."""
    out, depth = [], 0
    for part in re.split(r"(<[^>]+>)", markup):
        if part.startswith("<"):
            name = re.match(r"</?([a-zA-Z0-9]+)", part)
            if name and name.group(1).lower() in SKIP_TYPO:
                depth += -1 if part.startswith("</") else 1
            out.append(part)
            continue
        if depth == 0:
            part = re.sub(r" ([:;?!»€%])", r"&nbsp;\1", part)
            part = part.replace("« ", "«&nbsp;")
            part = re.sub(r"(\d) (\d{3})(?!\d)", r"\1&nbsp;\2", part)
        out.append(part)
    return "".join(out)


def render(page):
    pid, lang, out, src, navkey, shape, title, desc = page
    t = T[lang]
    body = (SRC / "pages" / src).read_text(encoding="utf-8")
    body = re.sub(r"\{\{block:([a-z_]+)\}\}", lambda m: BLOCKS[m.group(1)](lang), body)
    body = body.replace("{{icon:ok}}", ICON["ok"]).replace("{{icon:no}}", ICON["no"]).replace("{{icon:idle}}", ICON["idle"])
    body = fill(body)
    if lang == "fr":
        body = typo_fr(body)
    if shape == "article":
        body = f'<article class="wrap">{body}</article>'
    other_lang = "en" if lang == "fr" else "fr"
    here = URL[(pid, lang)]
    has_other = (pid, other_lang) in URL
    other_url = URL[(pid, other_lang)] if has_other else URL[("home", other_lang)]
    alternates = ""
    if has_other and pid != "notfound":
        fr_url, en_url = URL[(pid, "fr")], URL[(pid, "en")]
        alternates = (f'<link rel="alternate" hreflang="fr" href="{SITE}{fr_url}">\n'
                      f'<link rel="alternate" hreflang="en" href="{SITE}{en_url}">\n'
                      f'<link rel="alternate" hreflang="x-default" href="{SITE}{fr_url}">\n')
    current = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{current if key == navkey else ""}>{label}</a>' for key, href, label in t["nav"])
    mailto = f"mailto:{MAIL}"
    cols = "".join(
        "<div><h2>" + head + "</h2><ul>"
        + "".join('<li><a href="' + h + '">' + fill_label(label) + "</a></li>" for h, label in links)
        + "</ul></div>" for head, links in t["cols"])
    robots = '<meta name="robots" content="noindex">\n' if pid == "notfound" else ""
    canonical = "" if pid == "notfound" else f'<link rel="canonical" href="{SITE}{here}">\n'
    scripts = '<script src="/assets/menu.js" defer></script>\n'
    if pid == "verify":
        scripts += '<script src="/assets/verify.js" defer></script>\n'
    if pid == "brief":
        scripts += '<script src="/assets/print.js" defer></script>\n'
    og_image = f"{SITE}/assets/og-{lang}.jpg"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}{canonical}{alternates}<meta property="og:type" content="website">
<meta property="og:site_name" content="AMR">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_GB'}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{here}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b3436">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/lexend-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
{jsonld(pid, lang)}{scripts}</head>
<body>
<a class="skip" href="#contenu">{t['skip']}</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{URL[('home', lang)]}" aria-label="{t['home']}">{LOGO}<span>AMR</span></a>
<nav class="nav" aria-label="{t['menu']}">{nav}<a class="lang" href="{other_url}" lang="{other_lang}" hreflang="{other_lang}">{t['other']}</a><a class="btn" href="{mailto}">{t['write']}</a></nav>
<details class="menu"><summary>{t['menu']}</summary><div class="menu-list">{nav}<a href="{other_url}" lang="{other_lang}" hreflang="{other_lang}">{t['other']}</a><a href="{mailto}">{t['write']}</a></div></details>
</div></header>
<main id="contenu">
{body}
</main>
<footer class="foot"><div class="wrap">
<div class="foot-in">
<div><a class="brand" href="{URL[('home', lang)]}" aria-label="{t['home']}">{LOGO}<span>AMR</span></a>
<p class="note">{t['tagline']}</p>
<p class="note">{t['who']}<br><a href="{mailto}">{MAIL}</a></p></div>
{cols}
</div>
<p class="legal"><span>{t['legal']}</span><span>{fill_label(t['updated'])}</span></p>
</div></footer>
</body>
</html>
"""


def fill_label(text):
    return text.format(**FACTS) if "{" in text else text


def sitemap():
    rows = []
    for pid, lang, *_ in PAGES:
        if pid == "notfound":
            continue
        rows.append(f"  <url><loc>{SITE}{URL[(pid, lang)]}</loc><lastmod>{FACTS['site_date_iso']}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def outputs():
    files = {page[2]: render(page) for page in PAGES}
    files["sitemap.xml"] = sitemap()
    files["robots.txt"] = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    files["llms.txt"] = fill((SRC / "llms.txt").read_text(encoding="utf-8"))
    return files


def main():
    check = "--check" in sys.argv
    stale = []
    for name, content in outputs().items():
        target = ROOT / name
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(name)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    if check and stale:
        print("Pas à jour (relancer python tools/build.py) :", ", ".join(stale))
        return 1
    print(f"{len(PAGES)} pages, {FACTS['tools_count']} outils, {FACTS['templates_count']} gabarits, {len(FAQ)} questions"
          + (" : à jour" if check else " : écrit"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
