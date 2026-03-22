#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open('src/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences
orbs_count = content.count('Rastreio de Rainbow Orbs')
print(f'Found {orbs_count} occurrences of "Rastreio de Rainbow Orbs"')

# Find the occurrence positions
import re
matches = list(re.finditer('Rastreio de Rainbow Orbs', content))
print(f'Exact positions: {[m.start() for m in matches]}')

# Get context around each match
for i, match in enumerate(matches):
    start_pos = max(0, match.start() - 100)
    end_pos = min(len(content), match.end() + 100)
    print(f'\nContext {i+1} (pos {match.start()}):\n{repr(content[start_pos:end_pos])}')

# Now let's look for the closing </li> tags that follow each one
# to understand the full <li> block structure
print('\n' + '='*80)
print('Looking for full <li>...</li> blocks...\n')

# Find all <li> blocks that contain "Rastreio de Rainbow Orbs"
li_pattern = r'<li class="bg-slate-950[^<]*(?:(?!</li>).)*?Rastreio de Rainbow Orbs.*?</li>'
li_matches = list(re.finditer(li_pattern, content, re.DOTALL))
print(f'Found {len(li_matches)} complete <li> blocks with Rainbow Orbs')

for i, match in enumerate(li_matches):
    li_content = match.group(0)
    print(f'\n<li> Block {i+1} (length: {len(li_content)}):\n{repr(li_content[:200])}...')
