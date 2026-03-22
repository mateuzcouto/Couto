#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('src/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('debug_output.txt', 'w', encoding='utf-8') as out:
    orbs_count = content.count('Rastreio de Rainbow Orbs')
    out.write(f'Found {orbs_count} occurrences of "Rastreio de Rainbow Orbs"\n')
    
    # Find the two occurrences and their surrounding context
    import re
    matches = list(re.finditer('Rastreio de Rainbow Orbs', content))
    
    for i, match in enumerate(matches):
        # Find the <li> opening tag before this match
        search_start = max(0, match.start() - 500)
        before = content[search_start:match.start()]
        li_open_pos = before.rfind('<li class="bg-slate-950')
        
        if li_open_pos >= 0:
            li_start_abs = search_start + li_open_pos
            
            # Find the closing </li> after this match
            after = content[match.end():match.end() + 300]
            li_close_pos = after.find('</li>')
            if li_close_pos >= 0:
                li_end_abs = match.end() + li_close_pos + 5  # +5 for </li>
                
                li_block = content[li_start_abs:li_end_abs]
                out.write(f'\nOccurrence {i+1} <li> block:\n')
                out.write(repr(li_block) + '\n')
                out.write(f'Length: {len(li_block)}\n')
                out.write('---\n')

out.close()
print("Debug output written to debug_output.txt")
