import glob
import re
import os

md_files = sorted(glob.glob("Bai *.md"))
missing = []
found = 0

for f in md_files:
    content = open(f, encoding="utf-8").read()
    imgs = re.findall(r'src=["\']([^"\']+)["\']', content)
    for img in imgs:
        full_path = os.path.join(r"F:\Advance_C\stm32f103c8", img.replace("/", os.sep))
        if not os.path.exists(full_path):
            missing.append((f, img))
        else:
            found += 1

print(f"Checked {found} image tags across {len(md_files)} lessons.")
print(f"Total Missing: {len(missing)}")
for m in missing:
    print("  -> Missing:", m)
