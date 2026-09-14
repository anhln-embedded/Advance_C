import os
import glob
import re

md_files = sorted(glob.glob("Bai *.md"))

def clean_math(match):
    s = match.group(1)
    # Common replacements
    s = s.replace(r"\to", "→")
    s = s.replace(r"\Rightarrow", "⇒")
    s = s.replace(r"\le", "≤")
    s = s.replace(r"\ge", "≥")
    s = s.replace(r"\approx", "≈")
    s = s.replace(r"\times", "×")
    s = s.replace(r"\cdot", "·")
    s = s.replace(r"\pm", "±")
    s = s.replace(r"\mu\text{s}", "µs")
    s = s.replace(r"\mu\text{A}", "µA")
    s = s.replace(r"\mu\text{F}", "µF")
    s = s.replace(r"\mu s", "µs")
    s = s.replace(r"\mu A", "µA")
    s = s.replace(r"\Omega", "Ω")
    s = s.replace(r"\text{k}\Omega", "kΩ")
    s = s.replace(r"\text{MHz}", "MHz")
    s = s.replace(r"\text{kHz}", "kHz")
    s = s.replace(r"\text{Hz}", "Hz")
    s = s.replace(r"\text{ms}", "ms")
    s = s.replace(r"\text{ns}", "ns")
    s = s.replace(r"\text{s}", "s")
    s = s.replace(r"\text{V}", "V")
    s = s.replace(r"\text{mA}", "mA")
    s = s.replace(r"\circ", "°")
    
    # Remove \text{...}
    s = re.sub(r'\\text\{([^}]+)\}', r'\1', s)
    # Remove \frac{a}{b} -> a / b
    s = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1 / \2)', s)
    
    # Clean subscripts V_{DD} -> VDD or V_DD
    s = re.sub(r'([A-Za-z]+)_\{([^}]+)\}', r'\1_\2', s)
    s = s.replace(r"\_", "_")
    s = s.replace(r"\ ", " ")
    
    return s.strip()

for fpath in md_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace $...$
    new_content = re.sub(r'\$([^\$\n]+)\$', clean_math, content)

    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Cleaned math in: {fpath}")

print("MATH CLEANUP COMPLETE!")
