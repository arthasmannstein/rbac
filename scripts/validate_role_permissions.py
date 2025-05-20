import sys
from pathlib import Path

ROLES_ATOMIC_DIR = Path("roles/atomic")
PERMISSIONS_DIR = Path("permissions")

def extract_permission_from_role(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("- `") and ":" in line:
            return line.strip().strip("- `").strip()
    return None

def validate_permissions_in_roles():
    errors = []
    defined_permissions = set(p.stem for p in PERMISSIONS_DIR.glob("*.md"))
    used_permissions = set()

    for role_file in ROLES_ATOMIC_DIR.glob("*.md"):
        role_name = role_file.stem
        permission = extract_permission_from_role(role_file)
        if permission:
            perm_file_name = permission.replace(":", "-")
            used_permissions.add(perm_file_name)
            if perm_file_name not in defined_permissions:
                errors.append(f"❌ В атомарной роли `{role_name}` указано несуществующее разрешение `{permission}`.")
        else:
            errors.append(f"❌ В атомарной роли `{role_name}` не найдено разрешение.")

    unused_permissions = defined_permissions - used_permissions
    for unused in sorted(unused_permissions):
        errors.append(f"⚠️ Разрешение `{unused.replace('-', ':')}` не используется ни в одной роли.")

    return errors

if __name__ == "__main__":
    errs = validate_permissions_in_roles()
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    else:
        print("✅ Все разрешения существуют и используются.")
