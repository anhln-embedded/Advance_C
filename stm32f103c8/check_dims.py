import os, re

dir_p = r"F:\Advance_C\stm32f103c8\images"
for f in sorted(os.listdir(dir_p)):
    if f.endswith(".svg") and not f.endswith("_dark.svg") and not f.endswith("_light.svg"):
        content = open(os.path.join(dir_p, f), encoding="utf-8").read(300)
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
        wh = re.search(r'width="([^"]+)"\s+height="([^"]+)"', content)
        if vb and wh:
            print(f"{f:35}: vb={vb.group(1)}x{vb.group(2)}, wh={wh.group(1)}x{wh.group(2)}")
