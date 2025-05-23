#!/usr/bin/env python3

import os
import sys

FILE = "/usr/local/lib/python3.12/site-packages/tabbed_admin/admin.py"
OLD_IMPORT = "from django.utils.translation import ugettext_lazy as _"
NEW_IMPORT = "from django.utils.translation import gettext_lazy as _"

def patch_tabbed_admin():
    if not os.path.exists(FILE):
        print(f"❌ File not found: {FILE}")
        sys.exit(1)

    with open(FILE, "r") as f:
        content = f.read()

    if OLD_IMPORT not in content:
        print("✅ Already patched or different version — no changes needed.")
        return

    content = content.replace(OLD_IMPORT, NEW_IMPORT)

    with open(FILE, "w") as f:
        f.write(content)

    print("✅ Successfully patched tabbed_admin to use gettext_lazy.")

if __name__ == "__main__":
    patch_tabbed_admin()

