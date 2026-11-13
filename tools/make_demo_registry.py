"""Fabrique le registre de démonstration du site avec le vrai code d'AMR.

Tout est fictif (organisations, agents, décision) ; rien n'est simulé : chaque
réponse est celle que le registre a rendue. Le site ne fait que les afficher et
vérifier la signature de l'instantané dans le navigateur.

Chaque mandant enregistre sa clé puis signe son mandat, comme le ferait une vraie
organisation : le registre refuse ensuite tout mandat de ce mandant qui n'est pas
signé. Les clés privées des mandants ne quittent pas la mémoire de ce script.

    uv venv .venv && uv pip install --python .venv/bin/python git+https://github.com/JC7333/amr
    .venv/bin/python tools/make_demo_registry.py /tmp/amr-demo

Écrit assets/demo/lock-demo.json, registry-snapshot.jws, registry-key.json et registry-key.pem.
La clé privée reste dans le dossier de travail : la supprimer ensuite, ne jamais
la mettre dans le dépôt. Un mandat dure un an au plus : relancer ce script avant
la date d'expiration affichée sur la page « Vérifier », puis `python tools/build.py`.
"""

import asyncio
import base64
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "demo"

work = Path(sys.argv[1]).resolve()
work.mkdir(parents=True, exist_ok=True)
os.environ["AMR_DB_PATH"] = str(work / "demo.db")
os.environ["AMR_SIGNING_KEY_PATH"] = str(work / "demo_key.pem")
os.environ["AMR_PUBLIC_KEY_PATH"] = str(work / "demo_key.pub")
if (work / "demo.db").exists():
    sys.exit("Le dossier de travail contient déjà un registre : en donner un vide.")

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat  # noqa: E402

from amr.crypto.principal import b64url_encode, key_registration_payload  # noqa: E402
from amr.models.organ_decision import OrganDecision  # noqa: E402
from amr.templates import get_template  # noqa: E402
from amr.tools.create_mandate import create_mandate  # noqa: E402
from amr.tools.issue_action_token import issue_action_token  # noqa: E402
from amr.tools.issue_mandate_attestation import get_registry_public_key  # noqa: E402
from amr.tools.principal_keys import prepare_mandate_signature, register_principal_key  # noqa: E402
from amr.tools.revoke_mandate import revocation_payload, revoke_mandate  # noqa: E402

PRINCIPAL = "org:clinique-des-exemples"
OTHER_PRINCIPAL = "org:mutuelle-des-exemples"
AGENT = "agent:secretariat-consultations"
AUDIENCE = "recepteur:demonstration"

# (clé, type d'action, métadonnées, libellé FR, libellé EN)
CASES = [
    ("book", "appointment.book", {}, "Réserver un rendez-vous", "Book an appointment"),
    ("order_ok", "supplies.order", {"amount": "80", "currency": "EUR"},
     "Commander 80 € de fournitures", "Order €80 of supplies"),
    ("order_over", "supplies.order", {"amount": "2000", "currency": "EUR"},
     "Commander 2 000 € de fournitures", "Order €2,000 of supplies"),
    ("prescribe", "prescription", {}, "Renouveler une ordonnance", "Renew a prescription"),
    ("send", "patient_message.send", {}, "Envoyer un message à un patient", "Send a message to a patient"),
]


def claims(token: str) -> dict:
    part = token.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))


async def signed_mandate(principal_id: str, **args) -> dict:
    """Le mandant enregistre sa clé, signe le mandat, et le registre le crée."""
    private = Ed25519PrivateKey.generate()  # jamais écrite sur disque
    public = b64url_encode(private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw))
    proof = b64url_encode(private.sign(key_registration_payload(principal_id, public)))
    registered = json.loads(await register_principal_key(
        principal_id=principal_id, public_key=public, proof_signature=proof))
    assert registered.get("key_id"), registered
    unsigned = json.loads(await create_mandate(principal_id=principal_id, **args))
    assert unsigned.get("code") == "principal_signature_required", unsigned  # témoin : sans signature, refus
    prepared = json.loads(await prepare_mandate_signature(principal_id=principal_id, **args))
    signature = b64url_encode(private.sign(prepared["payload"].encode("utf-8")))
    created = json.loads(await create_mandate(
        principal_id=principal_id, principal_signature=signature, signed_at=prepared["signed_at"], **args))
    assert created.get("status") == "created", created
    created["principal_key_id"] = registered["key_id"]
    created["private"] = private
    return created


async def run() -> dict:
    try:
        from amr.db.engine import init_db

        await init_db()
    except Exception as exc:  # le registre s'initialise aussi tout seul
        print("init_db :", exc)

    template = get_template("agent-sante-rgpd")
    decision = OrganDecision(
        body="Commission du numérique (démonstration)",
        title="Assistant de secrétariat des consultations externes",
        decided_on="2026-11-10",
        reference="DEMO-2026-01",
        authorized_personnel=("Cadre de santé des consultations", "Responsable du secrétariat médical"),
    )
    kwargs = template.create_mandate_kwargs(organ_decision=decision)
    mandate = await signed_mandate(
        PRINCIPAL, agent_id=AGENT, scope=template.summary,
        legal_basis_regulation="Décision de la commission du numérique",
        legal_basis_article="DEMO-2026-01", duration_hours=8760, **kwargs)
    mandate_id = mandate["mandate_id"]

    cases = []
    for key, action_type, meta, fr, en in CASES:
        answer = json.loads(await issue_action_token(
            mandate_id=mandate_id, agent_id=AGENT, action=fr, audience=AUDIENCE,
            action_metadata_json=json.dumps(meta), action_type=action_type))
        case = {"key": key, "action_type": action_type, "metadata": meta, "fr": fr, "en": en}
        if answer.get("token"):
            c = claims(answer["token"])
            case.update(issued=True, lifetime_seconds=c["exp"] - c["iat"],
                        registry_check=bool(c.get("amr_registry_check")),
                        response={"token": answer["token"][:28] + "...", "expires_at": answer["expires_at"],
                                  "key_id": answer["key_id"]})
        else:
            case.update(issued=False, reason=answer["reason"], detail=answer.get("detail", ""),
                        response={k: v for k, v in answer.items() if k != "mandate_id"})
        cases.append(case)

    second = get_template("agent-support-client")
    other = await signed_mandate(
        OTHER_PRINCIPAL, agent_id="agent:accueil-adherents",
        scope=second.summary, legal_basis_regulation="Décision de la direction de la relation adhérents",
        legal_basis_article="DEMO-2026-02", duration_hours=8760, **second.create_mandate_kwargs())
    reason = "démonstration : mandat retiré par le mandant"
    refused = json.loads(await revoke_mandate(mandate_id=other["mandate_id"], reason=reason))
    assert refused.get("code") == "principal_signature_required", refused  # témoin : le retrait se signe aussi
    moment = datetime.now(timezone.utc).isoformat()
    withdrawal = b64url_encode(other["private"].sign(revocation_payload(
        mandate_id=other["mandate_id"], principal_id=OTHER_PRINCIPAL, reason=reason, signed_at=moment)))
    revoked = json.loads(await revoke_mandate(
        mandate_id=other["mandate_id"], reason=reason, principal_signature=withdrawal, signed_at=moment))
    assert revoked.get("status") == "revoked", revoked
    after = json.loads(await issue_action_token(
        mandate_id=other["mandate_id"], agent_id="agent:accueil-adherents", action="Répondre à un ticket",
        audience=AUDIENCE, action_type="ticket.answer"))
    assert after.get("denied") is True, after

    key = json.loads(await get_registry_public_key())
    perimeter = {k: kwargs.get(k) for k in ("allowed_actions", "forbidden_actions", "max_amount", "currency")}
    return {
        "generated_on": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "amr_version": metadata.version("mandatia"),
        "template": {"id": template.template_id, "version": template.version},
        "mandate_id": mandate_id,
        "revoked_mandate_id": other["mandate_id"],
        # L'identifiant que chaque mandant annonce : la page « Vérifier » le compare à
        # l'empreinte publiée par le registre (principal_ref), qui ne publie pas les noms.
        "announced_principals": {mandate_id: PRINCIPAL, other["mandate_id"]: OTHER_PRINCIPAL},
        "principal_key_id": mandate["principal_key_id"],
        "revoked_reason_after": after["reason"],
        "perimeter": perimeter,
        "cases": cases,
        "key": {"key_id": key["key_id"], "jwk": key["public_key_jwk"]},
    }


data = asyncio.run(run())
snapshot = work / "snapshot.jws"
done = subprocess.run(
    [sys.executable, "-m", "amr.public_registry", "export", "--out", str(snapshot),
     "--db", os.environ["AMR_DB_PATH"]], capture_output=True, text=True, env=os.environ)
if done.returncode != 0:
    sys.exit(f"export impossible : {done.stdout} {done.stderr}")

OUT.mkdir(parents=True, exist_ok=True)
key = data.pop("key")
(OUT / "registry-key.json").write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8")
raw_key = base64.urlsafe_b64decode(key["jwk"]["x"] + "=" * (-len(key["jwk"]["x"]) % 4))
pem = base64.b64encode(bytes.fromhex("302a300506032b6570032100") + raw_key).decode()
(OUT / "registry-key.pem").write_text(
    f"-----BEGIN PUBLIC KEY-----\n{pem}\n-----END PUBLIC KEY-----\n", encoding="utf-8")
(OUT / "registry-snapshot.jws").write_text(snapshot.read_text(encoding="utf-8").strip() + "\n", encoding="utf-8")
(OUT / "lock-demo.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("écrit :", ", ".join(sorted(p.name for p in OUT.iterdir())))
print("mandat actif :", data["mandate_id"], "| mandat révoqué :", data["revoked_mandate_id"])
print("clé privée à supprimer :", work / "demo_key.pem")
