#!/usr/bin/env python3
with open('index.html', 'rb') as f:
    content = f.read()

# Find all "text-base">" occurrences
pattern = b'text-base">'
pos = 0
count = 0
while count < 15:
    idx = content.find(pattern, pos)
    if idx < 0:
        break
    # Show bytes after pattern
    after = content[idx+len(pattern):idx+len(pattern)+20]
    hex_after = ' '.join(f'{b:02x}' for b in after)
    chr_after = ''.join(chr(b) if 32 <= b < 127 else '?' for b in after)
    # Get context before to identify what nav button this is
    before_ctx = content[max(0,idx-200):idx].decode('utf-8', 'replace')
    # Find nearest label
    nav_label = ''
    for nav in ['Treinadores', 'Rainbow', 'Ranking', 'Guias', 'Pok', 'Sobre', 'Painel', 'Admin']:
        if nav in before_ctx[-300:] or nav in content[idx:idx+500].decode('utf-8','replace')[:300]:
            nav_label = nav
            break
    print(f'pos={idx} [{nav_label}]: bytes={hex_after} | chars={chr_after}')
    pos = idx + 1
    count += 1
