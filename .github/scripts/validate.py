#!/usr/bin/env python3
"""
Validator AMR - GitHub Action natif (v3, pragmatique)

Vérifie les règles non-négociables sur amr-site.
Sortie: validator_report.md (commentaire de PR)
Code retour: 0 = OK, 1 = blocking errors

Changements v3 :
- Case-insensitive sur les checks d'articles juridiques
- Au moins 1 article AI Act + 1 article RGPD (peu importe lesquels) au lieu d'exiger 4 spécifiques
- issue_action_token : README OU deploy_guide (pas les deux)
"""

import os
import sys
import re
import yaml
from pathlib import Path

REPO_ROOT = Path(".")
TEMPLATES_DIR = REPO_ROOT / "templates"

# Fichiers obligatoires à la racine d'un template
REQUIRED_ROOT_FILES = ["README.md", "mandate.yaml", "deploy_guide.md"]

# Sous-dossiers obligatoires + nombre minimum de fichiers
REQUIRED_SUBDIRS = {
    "examples": {"ext": ".yaml", "min_count": 3},
    "compliance": {"ext": ".md", "min_count": 3},
}

# Patterns d'articles AI Act et RGPD (case-insensitive)
# On exige AU MOINS UN article de chaque famille, pas tous.
AI_ACT_ARTICLE_PATTERN = re.compile(
    r"\barticle\s+\d+", re.IGNORECASE
)
# Pour AI Act : on cherche des mentions du Règlement (UE) 2024/1689 ou article qui parle d'IA
AI_ACT_KEYWORDS = ["2024/1689", "ai act", "intelligence artificielle"]
# Pour RGPD : Règlement 2016/679 ou rgpd
RGPD_KEYWORDS = ["2016/679", "rgpd"]

FORBIDDEN_VOICE_TERMS = [
    "thermaliste",
    "je me permets",
    "n'hésitez pas",
    "je serais ravi",
    "n'hesitez pas",
]


def check_naming_convention(template_dirs):
    """Tous les dossiers templates doivent commencer par agent-"""
    errors = []
    for d in template_dirs:
        name = d.name
        if not name.startswith("agent-"):
            errors.append(
                f"Naming: dossier `templates/{name}/` doit commencer par `agent-` "
                f"(pattern obligatoire: `agent-{{domaine}}`). "
                f"À renommer en `templates/agent-{name}/`."
            )
    return errors


def check_structure(template_dir):
    """Chaque template doit avoir les fichiers racine + sous-dossiers avec assez de fichiers"""
    errors = []
    for required in REQUIRED_ROOT_FILES:
        f = template_dir / required
        if not f.exists():
            errors.append(
                f"Structure `{template_dir.name}/`: fichier racine manquant `{required}`"
            )
    for subdir_name, spec in REQUIRED_SUBDIRS.items():
        subdir = template_dir / subdir_name
        if not subdir.exists() or not subdir.is_dir():
            errors.append(
                f"Structure `{template_dir.name}/`: dossier manquant `{subdir_name}/`"
            )
            continue
        files = list(subdir.glob(f"*{spec['ext']}"))
        if len(files) < spec["min_count"]:
            errors.append(
                f"Structure `{template_dir.name}/{subdir_name}/`: "
                f"{len(files)} fichier(s) `{spec['ext']}` trouvé(s), "
                f"minimum {spec['min_count']} requis."
            )
    return errors


def check_yaml_valid(template_dir):
    """Tous les .yaml doivent être parsables"""
    errors = []
    yaml_files = list(template_dir.rglob("*.yaml"))
    for yf in yaml_files:
        try:
            with open(yf, "r", encoding="utf-8") as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(
                f"YAML invalide: `{yf.relative_to(REPO_ROOT)}` - {str(e).split(chr(10))[0]}"
            )
        except Exception as e:
            errors.append(f"Erreur lecture `{yf.relative_to(REPO_ROOT)}`: {e}")
    return errors


def check_legal_refs(template_dir):
    """Vérifier que le dossier compliance/ contient au moins une référence
    à AI Act et au moins une référence à RGPD (case-insensitive)."""
    warnings = []
    compliance_dir = template_dir / "compliance"
    if not compliance_dir.exists():
        return warnings

    all_text = ""
    for md_file in compliance_dir.glob("*.md"):
        try:
            all_text += md_file.read_text(encoding="utf-8") + "\n"
        except Exception:
            pass

    text_lower = all_text.lower()
    has_ai_act_keyword = any(kw in text_lower for kw in AI_ACT_KEYWORDS)
    has_rgpd_keyword = any(kw in text_lower for kw in RGPD_KEYWORDS)
    has_articles = bool(AI_ACT_ARTICLE_PATTERN.search(all_text))

    if not has_ai_act_keyword:
        warnings.append(
            f"`{template_dir.name}/compliance/`: aucune référence à l'AI Act détectée "
            f"(chercher `2024/1689`, `AI Act`, ou `intelligence artificielle`)"
        )
    if not has_rgpd_keyword:
        warnings.append(
            f"`{template_dir.name}/compliance/`: aucune référence au RGPD détectée "
            f"(chercher `2016/679` ou `RGPD`)"
        )
    if not has_articles:
        warnings.append(
            f"`{template_dir.name}/compliance/`: aucune mention d'article juridique précis détectée"
        )
    return warnings


def check_pivot_enforcement_mention(template_dir):
    """README.md OU deploy_guide.md doit mentionner issue_action_token"""
    warnings = []
    found = False
    for fname in ["README.md", "deploy_guide.md"]:
        f = template_dir / fname
        if f.exists():
            content = f.read_text(encoding="utf-8")
            if "issue_action_token" in content:
                found = True
                break
    if not found:
        warnings.append(
            f"`{template_dir.name}/`: ni README ni deploy_guide ne mentionnent `issue_action_token` "
            f"(pivot enforcement = argument commercial #1)"
        )
    return warnings


def check_voice_audric(template_dir):
    """Voix Audric: termes interdits absolus dans README"""
    warnings = []
    readme = template_dir / "README.md"
    if not readme.exists():
        return warnings
    content = readme.read_text(encoding="utf-8").lower()
    for term in FORBIDDEN_VOICE_TERMS:
        if term.lower() in content:
            warnings.append(
                f"Voix Audric: `{template_dir.name}/README.md` contient le terme interdit `{term}`"
            )
    return warnings


def main():
    blocking_errors = []
    warnings = []

    if not TEMPLATES_DIR.exists():
        print("Pas de dossier templates/ détecté. Skip validation templates.")
        write_report([], [], [])
        return 0

    template_dirs = [d for d in TEMPLATES_DIR.iterdir() if d.is_dir()]

    blocking_errors.extend(check_naming_convention(template_dirs))

    valid_templates = [d for d in template_dirs if d.name.startswith("agent-")]
    for tpl in valid_templates:
        blocking_errors.extend(check_structure(tpl))
        blocking_errors.extend(check_yaml_valid(tpl))
        warnings.extend(check_legal_refs(tpl))
        warnings.extend(check_pivot_enforcement_mention(tpl))
        warnings.extend(check_voice_audric(tpl))

    write_report(blocking_errors, warnings, valid_templates)

    print(f"Templates analysés : {len(valid_templates)}")
    print(f"Erreurs bloquantes : {len(blocking_errors)}")
    print(f"Warnings : {len(warnings)}")

    if blocking_errors:
        print("[FAIL] Erreurs bloquantes détectées")
        return 1
    print("[OK] Aucune erreur bloquante")
    return 0


def write_report(blocking_errors, warnings, valid_templates):
    """Génère validator_report.md pour commentaire PR"""
    lines = ["## Validator", ""]

    if not blocking_errors and not warnings:
        lines.append("✅ **Tous les checks structurels passent.**")
        lines.append("")
        lines.append(f"Templates analysés ({len(valid_templates)}):")
        for tpl in sorted(valid_templates, key=lambda d: d.name):
            lines.append(f"- `{tpl.name}/`")
        lines.append("")
        lines.append("_Le scoring qualitatif détaillé sera produit par la routine Claude Code à 8h Paris._")
    else:
        if blocking_errors:
            lines.append(f"### ❌ Erreurs bloquantes ({len(blocking_errors)})")
            lines.append("")
            lines.append("Ces erreurs doivent être corrigées avant merge :")
            lines.append("")
            for err in blocking_errors:
                lines.append(f"- {err}")
            lines.append("")

        if warnings:
            lines.append(f"### ⚠️ Warnings ({len(warnings)})")
            lines.append("")
            lines.append("Non-bloquants mais à examiner :")
            lines.append("")
            for w in warnings:
                lines.append(f"- {w}")
            lines.append("")

        if blocking_errors:
            lines.append("---")
            lines.append("")
            lines.append("⛔ **Ce check doit passer avant que la PR puisse être mergée.**")

    Path("validator_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
