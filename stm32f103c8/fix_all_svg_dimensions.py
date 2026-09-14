import os, re

images_dir = r"F:\Advance_C\stm32f103c8\images"
count = 0

for f in os.listdir(images_dir):
    if not f.endswith(".svg"):
        continue
    fpath = os.path.join(images_dir, f)
    with open(fpath, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Extract viewBox
    vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    if not vb_match:
        continue
    
    vb_w, vb_h = vb_match.group(1), vb_match.group(2)
    
    # Replace width="100%" height="100%" with width="{vb_w}" height="{vb_h}"
    new_content = re.sub(
        r'width="100%"\s+height="100%"',
        f'width="{vb_w}" height="{vb_h}"',
        content
    )
    
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as file:
            file.write(new_content)
        count += 1

print(f"Successfully updated intrinsic width/height on {count} SVG files.")
