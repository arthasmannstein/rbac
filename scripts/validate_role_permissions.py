import sys
from pathlib import Path

ROLES_ATOMIC_DIR = Path("roles/atomic")
PERMISSIONS_DIR = Path("permissions")
AGGREGATED_DIR = Path("roles/aggregated")
REPORT_PATH = Path("validation_report.md")

def extract_permission_from_role(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("- `") and ":" in line:
            return line.strip().strip("- `").strip()
    return None

def extract_used_permissions_from_aggregated():
    used_roles = set()
    for file in AGGREGATED_DIR.glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_block = False
        for line in lines:
            if line.strip().startswith("## Состав атомарных ролей"):
                in_block = True
                continue
            if in_block:
                if line.strip().startswith("- "):
                    role = line.strip().lstrip("- ").strip("`")
                    used_roles.add(role)
                elif line.strip() == "":
                    continue
                else:
                    break
    return used_roles

def extract_permission_reference(md_path):
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("- `") and ":" in line:
            return line.strip().strip("- `").strip()
    return None

def validate_all():
    errors = []
    warnings = []
    report_lines = ["# Отчёт по валидации ролевой модели\n"]

    defined_permissions = set(p.stem for p in PERMISSIONS_DIR.glob("*.md"))
    used_permissions = set()
    used_atomic_roles = extract_used_permissions_from_aggregated()

    atomic_roles_defined = set()
    permission_refs_from_roles = set()

    # 1. Проверка атомарных ролей
    for role_file in ROLES_ATOMIC_DIR.glob("*.md"):
        role_name = role_file.stem
        atomic_roles_defined.add(role_name)

        content = role_file.read_text(encoding="utf-8")
        if "## Назначение" not in content and "## Разрешение" not in content:
            errors.append(f"❌ Файл `{role_name}.md` не содержит необходимых секций `## Разрешение` или `## Назначение`.")

        permission = extract_permission_reference(role_file)
        if not permission:
            errors.append(f"❌ В атомарной роли `{role_name}` не найдено разрешение.")
            continue

        permission_refs_from_roles.add(permission)
        perm_file_name = permission.replace(":", "-")
        used_permissions.add(perm_file_name)
        if perm_file_name not in defined_permissions:
            errors.append(f"❌ В атомарной роли `{role_name}` указано несуществующее разрешение `{permission}`.")

    # 2. Проверка разрешений
    for perm_file in PERMISSIONS_DIR.glob("*.md"):
        perm_name = perm_file.stem
        if perm_name not in used_permissions:
            warnings.append(f"⚠️ Разрешение `{perm_name.replace('-', ':')}` не используется ни в одной роли.")
        content = perm_file.read_text(encoding="utf-8")
        if "## Описание" not in content:
            warnings.append(f"⚠️ Разрешение `{perm_name}` не содержит секции `## Описание`.")

    # 3. Проверка агрегатов
    for role in sorted(used_atomic_roles):
        if role not in atomic_roles_defined:
            errors.append(f"❌ В агрегированной роли указана несуществующая атомарная роль `{role}`.")

    # 4. Неиспользуемые атомарные роли
    unused_atomic_roles = atomic_roles_defined - used_atomic_roles
    for r in sorted(unused_atomic_roles):
        warnings.append(f"⚠️ Атомарная роль `{r}` не используется ни в одной агрегированной роли.")

    # Markdown report
    report_lines.append("## Статистика")
    report_lines += [
        "",
        "| Категория         | Кол-во |",
        "|-------------------|--------|",
        f"| Атомарные роли    | {len(atomic_roles_defined)} |",
        f"| Агрегаты          | {len(list(AGGREGATED_DIR.glob('*.md')))} |",
        f"| Разрешения        | {len(defined_permissions)} |",
        f"| Неисп. роли       | {len(unused_atomic_roles)} |",
        f"| Неисп. разрешения | {len(defined_permissions - used_permissions)} |",
        ""
    ]

    if errors:
        report_lines.append("## Ошибки")
        report_lines += [f"- {e}" for e in errors]
    else:
        report_lines.append("Нет критических ошибок")

    if warnings:
        report_lines.append("\n## Предупреждения")
        report_lines += [f"- {w}" for w in warnings]
    else:
        report_lines.append("\nНет предупреждений")

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print("Сформирован отчёт:", REPORT_PATH)

    if errors:
        sys.exit(1)

if __name__ == "__main__":
    validate_all()
