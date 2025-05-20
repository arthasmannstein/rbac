import os
import pandas as pd
import yaml
from pathlib import Path
import sys

AGGREGATED_DIR = "roles/aggregated"
ATOMIC_DIR = "roles/atomic"
OUTPUT_MD = "docs/roles_table.md"
OUTPUT_XLSX = "matrix/roles_table.xlsx"
OUTPUT_YAML = "export/roles_for_avanpost.yaml"

def parse_aggregated_md(file_path):
    role_name = Path(file_path).stem
    atomic_roles = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        in_block = False
        for line in lines:
            if line.strip().startswith("## Состав атомарных ролей"):
                in_block = True
                continue
            if in_block:
                if line.strip().startswith("- "):
                    atomic_roles.append(line.strip().lstrip("- ").strip("`"))
                elif line.strip() == "":
                    continue
                else:
                    break
    return role_name, atomic_roles

def validate_aggregated_roles(roles_data, atomic_role_names):
    errors = []
    for item in roles_data:
        role = item['Агрегированная роль']
        atoms = item['Атомарные роли'].split(", ") if item['Атомарные роли'] else []
        if not atoms:
            errors.append(f" Роль `{role}` не содержит атомарных ролей.")
        for atom in atoms:
            if atom not in atomic_role_names:
                errors.append(f" В роли `{role}` указана несуществующая атомарная роль `{atom}`.")
        if len(atoms) != len(set(atoms)):
            errors.append(f" В роли `{role}` есть повторяющиеся атомарные роли.")
    return errors

def main():
    roles_data = []
    yaml_data = {"roles": []}

    # Собираем все существующие атомарные роли
    atomic_role_names = set(f.stem for f in Path(ATOMIC_DIR).glob("*.md"))

    for file in sorted(Path(AGGREGATED_DIR).glob("*.md")):
        role, atomic_roles = parse_aggregated_md(file)
        roles_data.append({"Агрегированная роль": role, "Атомарные роли": ", ".join(atomic_roles)})
        yaml_data["roles"].append({
            "name": role,
            "description": f"{role} aggregated role",
            "permissions": atomic_roles,
            "scope": "global"
        })

    # Валидация
    errors = validate_aggregated_roles(roles_data, atomic_role_names)
    if errors:
        print("\n".join(errors))
        sys.exit(1)

    # Markdown
    md_lines = [
        "| Агрегированная роль | Атомарные роли |",
        "|---------------------|----------------|"
    ]
    for row in roles_data:
        md_lines.append(f"| {row['Агрегированная роль']} | {row['Атомарные роли']} |")

    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # Excel
    os.makedirs(os.path.dirname(OUTPUT_XLSX), exist_ok=True)
    df = pd.DataFrame(roles_data)
    df.to_excel(OUTPUT_XLSX, index=False)

    # YAML
    os.makedirs(os.path.dirname(OUTPUT_YAML), exist_ok=True)
    with open(OUTPUT_YAML, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

    print(" Все артефакты успешно сгенерированы.")

if __name__ == "__main__":
    main()
