import glob
import re
import os

scripts = sorted(glob.glob(r"F:\Advance_C\stm32f103c8\*.py"))

for s in scripts:
    with open(s, "r", encoding="utf-8") as f:
        c = f.read()
    matches = re.findall(r'save_svg\(\s*["\']([^"\']+\.svg)["\']', c)
    if not matches:
        matches = re.findall(r'open\([^,]+["\']([^"\']+\.svg)["\']', c)
    matches = sorted(list(set(matches)))
    if matches:
        print(f"{os.path.basename(s)}:")
        for m in matches:
            print(f"  - {m}")
