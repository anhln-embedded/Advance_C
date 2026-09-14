import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\Advance_C\svg_overflow_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

vb = data['viewbox_issues']
print(f"=== ViewBox Issues ({len(vb)}) ===")
by_file = {}
for item in vb:
    by_file.setdefault(item['file'], []).append(item)

for fname, items in sorted(by_file.items()):
    max_ov = max(it['overflow'] for it in items)
    if max_ov > 5:
        print(f"{fname}: {len(items)} issues, max overflow: {max_ov}px")
        for it in items[:3]:
            print(f"   -> [{it['type']}] \"{it['text'][:45]}\" (ov={it['overflow']}px, x={it['x']}, fs={it['fs']}, vb_w={it['vb_w']})")

print("\n=== Box Issues Sample ===")
boxes = data['box_issues']
box_by_file = {}
for item in boxes:
    box_by_file.setdefault(item['file'], []).append(item)

for fname, items in sorted(box_by_file.items())[:10]:
    max_ov = max(it['overflow'] for it in items)
    print(f"{fname}: {len(items)} issues, max box overflow: {max_ov}px")
    for it in items[:2]:
        print(f"   -> \"{it['text'][:40]}\" (text_w={it['text_w']}, rect_w={it['rect_w']}, ov={it['overflow']}px)")
