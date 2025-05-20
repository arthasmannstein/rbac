import pandas as pd
import os
import sys
from pathlib import Path

EXCEL_PATH = "matrix/aggregated_roles_matrix.xlsx"
OUTPUT_PATH = "diagrams/roles_graph.mmd"
ATOMIC_DIR = "roles/atomic"

def main():
    # Собираем список допустимых атомарных ролей
    atomic_role_names = set(f.stem for f in Path(ATOMIC_DIR).glob("*.md"))

    try:
        df = pd.read_excel(EXCEL_PATH)
    except Exception as e:
        print(f"❌ Ошибка при чтении {EXCEL_PATH}: {e}")
        sys.exit(1)

    lines = ["graph TD"]
    errors = []

    for _, row in df.iterrows():
        role = row["Агрегированная роль"]
        permissions = row.drop("Агрегированная роль").dropna().tolist()
        for perm in permissions:
            if perm not in atomic_role_names:
                errors.append(f"❌ В графе указана несуществующая атомарная роль `{perm}`.")
            lines.append(f"  {role} --> {perm}")

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Mermaid graph saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
