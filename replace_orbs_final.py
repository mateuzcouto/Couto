#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

file_path = 'src/index.html'

# Create backup
shutil.copy(file_path, file_path + '.backup')

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Save original length
original_length = len(content)

# First, let's replace the SECOND occurrence of the entire <li> block
# We need to find and replace the second "Rastreio de Rainbow Orbs" within a <li> block

# Strategy: Find both <li> blocks, keep first, replace second's content

# Find all matches of "Rastreio de Rainbow Orbs"
import re

pattern = r'(<li[^>]*bg-slate-950[^>]*>.*?)(Rastreio de Rainbow Orbs)(.*?</li>)'
matches = list(re.finditer(pattern, content, re.DOTALL))

print(f"Found {len(matches)} <li> blocks with Rainbow Orbs")

if len(matches) >= 2:
    # We keep the first one, replace the second one
    second_match = matches[1]
    
    # Get the content before and after the second match
    before = content[:second_match.start()]
    match_content = second_match.group(0)
    after = content[second_match.end():]
    
    # Create the replacement - same opening <li>, different content, same closing </li>
    li_open_tag = second_match.group(1)
    old_inner = second_match.group(2) + second_match.group(3)
    
    # New content for Despertador
    new_inner = '''Despertador Cognitivo-->
                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
    
    # But we need the proper emoji and color too
    # Let's do a more targeted replacement
    
    # Replace the second li block more carefully
    # Find the second occurrence and modify just that block
    
    # Split by the pattern and count which one is second
    parts = content.split('Rastreio de Rainbow Orbs')
    if len(parts) >= 3:
        # Reconstruct: keep firs occurrence as-is, modify second
        # But we need to be careful about the structure
        
        # Different approach: find the line number and do line-based replacement
        lines = content.split('\n')
        
        # Find lines with "Rastreio de Rainbow Orbs"
        orb_line_indices = []
        for i, line in enumerate(lines):
            if 'Rastreio de Rainbow Orbs' in line:
                orb_line_indices.append(i)
        
        print(f"Found 'Rastreio de Rainbow Orbs' at lines: {[i+1 for i in orb_line_indices]}")
        
        if len(orb_line_indices) >= 2:
            # Second occurrence is at index 1
            second_orb_line_idx = orb_line_indices[1]
            
            # Find the <li> opening before this line
            li_start_idx = -1
            for i in range(second_orb_line_idx, -1, -1):
                if '<li class="bg-slate-950' in lines[i]:
                    li_start_idx = i
                    break
            
            # Find the </li> after this line
            li_end_idx = -1
            for i in range(second_orb_line_idx, len(lines)):
                if '</li>' in lines[i]:
                    li_end_idx = i
                    break
            
            print(f"Found <li> block from line {li_start_idx+1} to {li_end_idx+1}")
            
            if li_start_idx >= 0 and li_end_idx > li_start_idx:
                # Replace the content inside this <li>
                # Keep the opening <li> tag (li_start_idx)
                # Keep the closing </li> tag (li_end_idx)
                # Replace everything in between
                
                new_lines = (
                    lines[:li_start_idx+1] + 
                    [
                        '',
                        '                            <span class="text-lg">🔔</span>',
                        '',
                        '                            <div>',
                        '',
                        '                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>',
                        '',
                        '                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>',
                        '',
                        '                            </div>',
                        '',
                        lines[li_end_idx]
                    ] +
                    lines[li_end_idx+1:]
                )
                
                new_content = '\n'.join(new_lines)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✓ Replacement successful!")
                print(f"File size: {original_length} → {len(new_content)} bytes")
            else:
                print("ERROR: Could not find <li> opening or closing tag")
        else:
            print("ERROR: Could not find second occurrence")
    else:
       print("ERROR: Not enough occurrences found")

