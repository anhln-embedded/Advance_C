import os
import sys
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

svg_dir = r"F:\Advance_C\stm32f103c8\images"
svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))

print(f"Analyzing {len(svg_files)} SVGs...")

viewbox_issues = []
box_issues = []

for fpath in svg_files:
    fname = os.path.basename(fpath)
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        vb_match = re.search(r'viewBox=["\']([0-9\.\s-]+)["\']', content)
        if vb_match:
            parts = [float(p) for p in vb_match.group(1).split()]
            vb_x, vb_y, vb_w, vb_h = parts[0], parts[1], parts[2], parts[3]
        else:
            vb_x, vb_y = 0.0, 0.0
            w_m = re.search(r'width=["\']([0-9\.]+)["\']', content)
            h_m = re.search(r'height=["\']([0-9\.]+)["\']', content)
            vb_w = float(w_m.group(1)) if w_m else 1000.0
            vb_h = float(h_m.group(1)) if h_m else 600.0

        # Find all rects: x, y, width, height
        rects = []
        for rm in re.finditer(r'<rect([^>]*)/?>', content):
            r_attr = rm.group(1)
            rx_m = re.search(r'x=["\']([0-9\.-]+)["\']', r_attr)
            ry_m = re.search(r'y=["\']([0-9\.-]+)["\']', r_attr)
            rw_m = re.search(r'width=["\']([0-9\.-]+)["\']', r_attr)
            rh_m = re.search(r'height=["\']([0-9\.-]+)["\']', r_attr)
            if rx_m and ry_m and rw_m and rh_m:
                rx = float(rx_m.group(1))
                ry = float(ry_m.group(1))
                rw = float(rw_m.group(1))
                rh = float(rh_m.group(1))
                # ignore full-background rects
                if rw < vb_w * 0.95 or rh < vb_h * 0.95:
                    rects.append({'x': rx, 'y': ry, 'w': rw, 'h': rh})

        # Find all text elements
        text_matches = re.finditer(r'<text([^>]*)>(.*?)</text>', content, re.DOTALL)
        for tm in text_matches:
            attrs = tm.group(1)
            raw_body = tm.group(2)
            
            tspans = re.findall(r'<tspan([^>]*)>(.*?)</tspan>', raw_body, re.DOTALL)
            items_to_check = []
            if tspans:
                for t_attr, t_text in tspans:
                    items_to_check.append((attrs + " " + t_attr, t_text))
            else:
                items_to_check.append((attrs, raw_body))

            for a_str, t_body in items_to_check:
                text_val = re.sub(r'<[^>]+>', '', t_body).strip()
                if not text_val:
                    continue

                x_m = re.search(r'x=["\']([0-9\.-]+)["\']', a_str)
                y_m = re.search(r'y=["\']([0-9\.-]+)["\']', a_str)
                fs_m = re.search(r'font-size=["\']([0-9\.-]+)(?:px)?["\']', a_str)
                anchor_m = re.search(r'text-anchor=["\']([a-zA-Z]+)["\']', a_str)

                x = float(x_m.group(1)) if x_m else 0.0
                y = float(y_m.group(1)) if y_m else 0.0
                fs = float(fs_m.group(1)) if fs_m else 14.0
                anchor = anchor_m.group(1) if anchor_m else "start"

                char_w = fs * 0.58
                text_w = len(text_val) * char_w

                if anchor == "start":
                    left = x
                    right = x + text_w
                elif anchor == "middle":
                    left = x - text_w / 2.0
                    right = x + text_w / 2.0
                elif anchor == "end":
                    left = x - text_w
                    right = x

                # 1. Viewbox overflow check
                if right > (vb_x + vb_w - 5):
                    overflow_amount = right - (vb_x + vb_w)
                    viewbox_issues.append({
                        'file': fname, 'type': 'VIEWBOX_RIGHT', 'text': text_val,
                        'overflow': round(overflow_amount, 1), 'x': x, 'y': y, 'fs': fs, 'len': len(text_val), 'vb_w': vb_w
                    })
                if left < (vb_x + 5):
                    overflow_amount = (vb_x + 5) - left
                    viewbox_issues.append({
                        'file': fname, 'type': 'VIEWBOX_LEFT', 'text': text_val,
                        'overflow': round(overflow_amount, 1), 'x': x, 'y': y, 'fs': fs, 'len': len(text_val), 'vb_x': vb_x
                    })

                # 2. Check if text is meant to be inside a rect box
                for r in rects:
                    # check if text center or baseline is inside or vertically aligned with rect
                    if (r['y'] - 5 <= y <= r['y'] + r['h'] + 5) and (r['x'] - 10 <= x <= r['x'] + r['w'] + 10):
                        # Text seems to belong to this rect
                        if left < r['x'] - 2 or right > r['x'] + r['w'] + 2:
                            # Box overflow
                            box_overflow = max(r['x'] - left, right - (r['x'] + r['w']))
                            box_issues.append({
                                'file': fname, 'type': 'BOX_OVERFLOW', 'text': text_val,
                                'overflow': round(box_overflow, 1), 'text_w': round(text_w, 1),
                                'rect_w': r['w'], 'x': x, 'y': y, 'fs': fs, 'rect': r
                            })
                            break

    except Exception as e:
        print(f"Error {fname}: {e}")

print(f"ViewBox edge issues: {len(viewbox_issues)}")
print(f"Rect Box overflow issues: {len(box_issues)}")

with open(r"F:\Advance_C\svg_overflow_report.json", "w", encoding="utf-8") as f:
    json.dump({'viewbox_issues': viewbox_issues, 'box_issues': box_issues}, f, ensure_ascii=False, indent=2)

print("Report saved to svg_overflow_report.json")

