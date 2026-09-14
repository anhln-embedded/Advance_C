import glob
import re

md_files = sorted(glob.glob("Bai *.md"))

for fpath in md_files:
    content = open(fpath, "r", encoding="utf-8").read()
    
    while "\\frac" in content:
        content = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1 / \2)", content)
    
    content = content.replace(r"\ll", "<<").replace(r"\mid", "|").replace(r"\%", "%").replace(r"\Delta", "Δ")
    content = re.sub(r"\$([^\$\n]+)\$", r"\1", content)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("Second pass complete!")
