import os
from pathlib import Path

AGGREGATED_DIR = Path("roles/aggregated")
OUTPUT_PATH = "diagrams/roles_graph.mmd"

def parse_aggregated_md(file_path):
    role_name = file_path.stem
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

def main():
    lines = ["graph TD"]
    for file in AGGREGATED_DIR.glob("*.md"):
        role_name, atomic_roles = parse_aggregated_md(file)
        for atom in atomic_roles:
            lines.append(f"  {role_name} --> {atom}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Mermaid graph saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
