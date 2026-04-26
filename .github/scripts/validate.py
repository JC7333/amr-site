#!/usr/bin/env python3
"""
Validator AMR - GitHub Action natif
Vérifie les règles non-négociables sur amr-site:
- Naming convention templates/agent-{domaine}/
- Structure 9 fichiers par template
- YAML valides
- Articles juridiques minimum cités

Sortie: validator_report.md (commentaire de PR)
Code retour: 0 = OK, 1 = blocking errors
"""

import os
import sys
import re
import yaml
from pathlib import Path

REPO_ROOT = Path(".")
TEMPLATES_DIR = REPO_ROOT / "templates"
REQUIRED_FILES_PER_TEMPLATE = [
    "README.md",
    "mandate.yaml",
    "deploy_guide.md",
    "examples/permissive.yaml",
    "examples/restrictive.yaml",
    "examples/balanced.yaml",
    "compliance/ai_act_mapping.md",
    "compliance/rgpd_mapping.md",
    "compliance/sector_specific.md",
]

REQUIRED_LEGAL_REFS_AI_ACT = [
    "Article 12",
    "Article 13",
    "Article 14",
    "Article 26",
]

REQUIRED_LEGAL_REFS_RGPD = [
    "Article 6",
    "Article 22",
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
                f"À renommer en `templates/agent-{name}/` via push-amr.ps1."
            )
    return errors


def check_structure(template_dir):
    """Chaque template doit avoir les 9 fichiers requis"""
    errors = []
    for required in REQUIRED_FILES_PER_TEMPLATE:
        f = template_dir / required
        if not f.exists():
            errors.append(
                f"Structure `{template_dir.name}/`: fichier manquant `{required}`"
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
    """Vérifier que les fichiers compliance citent bien les articles minimum"""
    warnings = []
    ai_act_file = template_dir / "compliance" / "ai_act_mapping.md"
    rgpd_file = template_dir / "compliance" / "rgpd_mapping.md"

    if ai_act_file.exists():
        content = ai_act_file.read_text(encoding="utf-8")
        for ref in REQUIRED_LEGAL_REFS_AI_ACT:
            if ref not in content:
                warnings.append(
                    f"`{template_dir.name}/compliance/ai_act_mapping.md` ne mentionne pas `{ref}`"
                )

    if rgpd_file.exists():
        content = rgpd_file.read_text(encoding="utf-8")
        for ref in REQUIRED_LEGAL_REFS_RGPD:
            if ref not in content:
                warnings.append(
                    f"`{template_dir.name}/compliance/rgpd_mapping.md` ne mentionne pas `{ref}`"
                )
    return warnings


def check_pivot_enforcement_mention(template_dir):
    """README.md et deploy_guide.md doivent mentionner issue_action_token"""
    warnings = []
    for fname in ["README.md", "deploy_guide.md"]:
        f = template_dir / fname
        if f.exists():
            content = f.read_text(encoding="utf-8")
            if "issue_action_token" not in content:
                warnings.append(
                    f"`{template_dir.name}/{fname}` ne mentionne pas `issue_action_token` "
                    f"(pivot enforcement = argument commercial #1)"
                )
    return warnings


def check_voice_audric(template_dir):
    """Voix Audric: termes interdits absolus"""
    warnings = []
    forbidden_terms = ["thermaliste", "je me permets", "n'hésitez pas", "je serais ravi"]
    readme = template_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
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

    # 1. Naming convention (BLOQUANT)
    blocking_errors.extend(check_naming_convention(template_dirs))

    # Pour chaque template valide, faire les autres checks
    valid_templates = [d for d in template_dirs if d.name.startswith("agent-")]
    for tpl in valid_templates:
        # 2. Structure (BLOQUANT pour les templates valides)
        struct_errs = check_structure(tpl)
        blocking_errors.extend(struct_errs)

        # 3. YAML valides (BLOQUANT)
        yaml_errs = check_yaml_valid(tpl)
        blocking_errors.extend(yaml_errs)

        # 4. Articles juridiques (WARNING)
        warnings.extend(check_legal_refs(tpl))

        # 5. Pivot enforcement (WARNING)
        warnings.extend(check_pivot_enforcement_mention(tpl))

        # 6. Voix Audric (WARNING)
        warnings.extend(check_voice_audric(tpl))

    write_report(blocking_errors, warnings, valid_templates)

    if blocking_errors:
        print(f"❌ {len(blocking_errors)} erreur(s) bloquante(s)")
        return 1
    else:
        print(f"✅ Aucune erreur bloquante. {len(warnings)} warning(s).")
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
