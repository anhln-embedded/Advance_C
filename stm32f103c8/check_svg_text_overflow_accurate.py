import os
import sys
import glob
import re
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

SVG_DIR = r"F:\Advance_C\stm32f103c8\images"
base_svgs = sorted([f for f in glob.glob(os.path.join(SVG_DIR, "*.svg")) if not ("_dark" in f or "_light" in f)])

print(f"Total base SVGs to inspect: {len(base_svgs)}")

# We will collect real issues
real_issues = []

for fpath in base_svgs:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        svg_text = f.read()

    # Parse CSS classes
    css_styles = {}
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', svg_text, re.DOTALL)
    for sb in style_blocks:
        rules = re.findall(r'([\.#a-zA-Z0-9_-]+)\s*\{([^}]+)\}', sb)
        for selector, rule in rules:
            selector = selector.strip()
            style_dict = {}
            for prop in rule.split(';'):
                if ':' in prop:
                    k, v = prop.split(':', 1)
                    style_dict[k.strip().lower()] = v.strip()
            css_styles[selector] = style_dict

    # Viewbox
    vb_m = re.search(r'viewBox=["\']([0-9\.\s-]+)["\']', svg_text)
    if vb_m:
        parts = [float(p) for p in vb_m.group(1).split()]
        vb_x, vb_y, vb_w, vb_h = parts[0], parts[1], parts[2], parts[3]
    else:
        vb_x, vb_y = 0.0, 0.0
        w_m = re.search(r'width=["\']([0-9\.]+)["\']', svg_text)
        h_m = re.search(r'height=["\']([0-9\.]+)["\']', svg_text)
        vb_w = float(w_m.group(1)) if w_m else 1000.0
        vb_h = float(h_m.group(1)) if h_m else 600.0

    # Parse Rectangles
    # find each <rect ... />
    rects = []
    for rm in re.finditer(r'<rect([^>]*)/?>', svg_text):
        rattr = rm.group(1)
        rx = re.search(r'x=["\']([0-9\.-]+)["\']', rattr)
        ry = re.search(r'y=["\']([0-9\.-]+)["\']', rattr)
        rw = re.search(r'width=["\']([0-9\.-]+)["\']', rattr)
        rh = re.search(r'height=["\']([0-9\.-]+)["\']', rattr)
        if rx and ry and rw and rh:
            x_val = float(rx.group(1))
            y_val = float(ry.group(1))
            w_val = float(rw.group(1))
            h_val = float(rh.group(1))
            # skip canvas backdrop
            if w_val >= vb_w * 0.98 and h_val >= vb_h * 0.98:
                continue
            rects.append({'x': x_val, 'y': y_val, 'w': w_val, 'h': h_val, 'raw': rattr})

    # Parse Text elements
    text_matches = re.finditer(r'<text([^>]*)>(.*?)</text>', svg_text, re.DOTALL)
    for tm in text_matches:
        t_attrs = tm.group(1)
        t_body = tm.group(2)

        # Check if text contains tspans or direct text
        tspans = re.findall(r'<tspan([^>]*)>(.*?)</tspan>', t_body, re.DOTALL)
        segments = []
        if tspans:
            for s_attrs, s_text in tspans:
                segments.append((t_attrs + " " + s_attrs, s_text))
        else:
            segments.append((t_attrs, t_body))

        for combined_attrs, seg_body in segments:
            clean_text = re.sub(r'<[^>]+>', '', seg_body).strip()
            # decode xml entities
            clean_text = clean_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            if not clean_text:
                continue

            # resolve styles from class
            class_m = re.search(r'class=["\']([^"\']+)["\']', combined_attrs)
            cls_name = ("." + class_m.group(1)) if class_m else ""
            c_style = css_styles.get(cls_name, {})

            # resolve font-size
            fs_m = re.search(r'font-size=["\']([0-9\.-]+)(?:px)?["\']', combined_attrs)
            if fs_m:
                font_size = float(fs_m.group(1))
            elif 'font-size' in c_style:
                fs_val = re.sub(r'[^0-9\.]', '', c_style['font-size'])
                font_size = float(fs_val) if fs_val else 14.0
            else:
                font_size = 14.0

            # resolve text-anchor
            ta_m = re.search(r'text-anchor=["\']([a-zA-Z]+)["\']', combined_attrs)
            if ta_m:
                anchor = ta_m.group(1)
            elif 'text-anchor' in c_style:
                anchor = c_style['text-anchor']
            else:
                anchor = 'start'

            # resolve x and y
            x_m = re.search(r'x=["\']([0-9\.-]+)["\']', combined_attrs)
            y_m = re.search(r'y=["\']([0-9\.-]+)["\']', combined_attrs)
            if not x_m or not y_m:
                continue
            x_pos = float(x_m.group(1))
            y_pos = float(y_m.group(1))

            # Character width factor:
            # - For uppercase/Vietnamese accents/bold: ~ 0.58
            # - Narrow chars (i, l, t, 1, space): smaller
            # Let's do a weighted char width calculation
            total_char_w = 0.0
            for ch in clean_text:
                if ch in 'ijlI.,:;!| ':
                    total_char_w += font_size * 0.28
                elif ch in 'mwMW_@%#':
                    total_char_w += font_size * 0.85
                elif ch.isupper():
                    total_char_w += font_size * 0.65
                else:
                    total_char_w += font_size * 0.52

            text_width = total_char_w

            if anchor == 'start':
                left_edge = x_pos
                right_edge = x_pos + text_width
            elif anchor == 'middle':
                left_edge = x_pos - text_width / 2.0
                right_edge = x_pos + text_width / 2.0
            elif anchor == 'end':
                left_edge = x_pos - text_width
                right_edge = x_pos

            # 1. Canvas Boundary Overflow
            if right_edge > (vb_x + vb_w - 6):
                ov = right_edge - (vb_x + vb_w)
                real_issues.append({
                    'file': fname, 'type': 'CANVAS_RIGHT_OVERFLOW',
                    'text': clean_text, 'overflow': round(ov, 1),
                    'right_edge': round(right_edge, 1), 'canvas_w': vb_w,
                    'x': x_pos, 'y': y_pos, 'font_size': font_size, 'anchor': anchor
                })
            if left_edge < (vb_x + 6):
                ov = (vb_x + 6) - left_edge
                real_issues.append({
                    'file': fname, 'type': 'CANVAS_LEFT_OVERFLOW',
                    'text': clean_text, 'overflow': round(ov, 1),
                    'left_edge': round(left_edge, 1), 'canvas_x': vb_x,
                    'x': x_pos, 'y': y_pos, 'font_size': font_size, 'anchor': anchor
                })

            # 2. Box / Rect Overflow
            # Find if there is a container rect designed for this text:
            # The text baseline y_pos is typically inside the rect (e.g. y_pos between rect.y + 10 and rect.y + rect.h)
            # and x_pos is roughly centered or inside rect.
            for r in rects:
                # Text vertical baseline is inside rect
                if (r['y'] < y_pos < r['y'] + r['h'] + 4) and (r['x'] - 5 <= x_pos <= r['x'] + r['w'] + 5):
                    # Check if text extends beyond rect's left or right edge
                    if left_edge < r['x'] - 2 or right_edge > r['x'] + r['w'] + 2:
                        ov = max(r['x'] - left_edge, right_edge - (r['x'] + r['w']))
                        # Only report significant overflows (> 4px)
                        if ov > 4.0:
                            real_issues.append({
                                'file': fname, 'type': 'BOX_OVERFLOW',
                                'text': clean_text, 'overflow': round(ov, 1),
                                'text_w': round(text_width, 1), 'box_w': r['w'],
                                'box_x': r['x'], 'box_y': r['y'],
                                'x': x_pos, 'y': y_pos, 'font_size': font_size, 'anchor': anchor
                            })
                            break

print(f"\nTotal real issues detected: {len(real_issues)}")
by_file = {}
for item in real_issues:
    by_file.setdefault(item['file'], []).append(item)

for fname, items in sorted(by_file.items()):
    print(f"\n📁 {fname}: {len(items)} issues")
    for it in items:
        if it['type'] == 'BOX_OVERFLOW':
            print(f"   ⚠️ [Box Overflow {it['overflow']}px] Box w={it['box_w']}, Text w={it['text_w']}, text=\"{it['text']}\" (fs={it['font_size']})")
        else:
            print(f"   🚨 [{it['type']} {it['overflow']}px] text=\"{it['text']}\" (x={it['x']}, fs={it['font_size']}, anchor={it['anchor']})")
