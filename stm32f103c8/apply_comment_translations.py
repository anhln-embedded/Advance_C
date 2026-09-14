# -*- coding: utf-8 -*-
import os
import sys
import glob
import re
import json

sys.path.append(r'F:\Advance_C\stm32f103c8')
from dict_batch1 import BATCH_MAP as m1
from dict_batch2 import BATCH_MAP as m2
from dict_batch3 import BATCH_MAP as m3
from dict_batch4 import BATCH_MAP as m4
from dict_batch5 import BATCH_MAP as m5

FULL_MAP = {}
FULL_MAP.update(m1)
FULL_MAP.update(m2)
FULL_MAP.update(m3)
FULL_MAP.update(m4)
FULL_MAP.update(m5)

# Sort keys by length descending to match longer phrases first if doing partial replacements
SORTED_KEYS = sorted(FULL_MAP.keys(), key=lambda x: len(x), reverse=True)

def translate_single_line_comment(line):
    # Match // comment at end of line or on its own line
    # Note: avoid matching inside string literals e.g. "http://"
    if '//' not in line:
        return line
    
    # Check if // is inside quotes
    # Simple check: count double quotes before //
    parts = line.split('//', 1)
    before = parts[0]
    comment = parts[1]
    
    # If odd number of quotes before //, it's inside a string literal
    if before.count('"') % 2 != 0:
        return line
    
    # Strip leading/trailing whitespace from comment
    c_stripped = comment.strip()
    
    # Check exact match
    if c_stripped in FULL_MAP:
        # Preserve original spacing after //
        m_space = re.match(r'^(\s*)', comment)
        leading_space = m_space.group(1) if m_space else ' '
        if not leading_space:
            leading_space = ' '
        return before + '//' + leading_space + FULL_MAP[c_stripped]
    
    # Try case-insensitive or stripped match
    for k in SORTED_KEYS:
        if k in c_stripped:
            comment = comment.replace(k, FULL_MAP[k])
            return before + '//' + comment

    return line

def translate_block_comment(line):
    if '/*' not in line or '*/' not in line:
        return line
    
    def repl(match):
        inner = match.group(1)
        inner_stripped = inner.strip()
        if inner_stripped in FULL_MAP:
            # Preserve space around comment
            return f"/* {FULL_MAP[inner_stripped]} */"
        for k in SORTED_KEYS:
            if k in inner_stripped:
                inner = inner.replace(k, FULL_MAP[k])
        return f"/*{inner}*/"

    return re.sub(r'/\*(.*?)\*/', repl, line)

def process_code_block(block_text):
    lines = block_text.split('\n')
    new_lines = []
    for line in lines:
        l = translate_single_line_comment(line)
        l = translate_block_comment(l)
        new_lines.append(l)
    return '\n'.join(new_lines)

def process_file(fpath, dry_run=False):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for code blocks: ```[tag]\n...\n```
    pattern = re.compile(r'(```[a-zA-Z0-9_-]*\r?\n)(.*?)(```)', re.DOTALL)

    def block_replacer(match):
        header = match.group(1)
        body = match.group(2)
        footer = match.group(3)
        # Check if block looks like C/C++ code or contains // or /*
        if '//' in body or '/*' in body:
            new_body = process_code_block(body)
            return header + new_body + footer
        return match.group(0)

    new_content = pattern.sub(block_replacer, content)

    if not dry_run and new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == '__main__':
    files = sorted(glob.glob(r'F:\Advance_C\stm32f103c8\Bai *.md'))
    print(f"Loaded {len(FULL_MAP)} translation entries.")
    print(f"Processing {len(files)} markdown files...")
    
    updated_count = 0
    for f in files:
        fname = os.path.basename(f)
        changed = process_file(f, dry_run=False)
        if changed:
            updated_count += 1
            print(f"  [UPDATED] {fname}")
        else:
            print(f"  [UNCHANGED] {fname}")

    print(f"\nDone! Updated {updated_count} files.")
