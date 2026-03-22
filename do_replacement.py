#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.stdout.flush()
sys.stderr.flush()

try:
    # Read the file
    with open('src/index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Log file
    log = open('replacement_log.txt', 'w', encoding='utf-8')
    log.write('Starting replacement...\n')
    
    # Find lines containing "Rastreio de Rainbow Orbs"
    rainbow_lines = []
    for i, line in enumerate(lines):
        if 'Rastreio de Rainbow Orbs' in line:
            rainbow_lines.append((i, line))
            log.write(f'Found at line {i+1}: {line.strip()}\n')
    
    log.write(f'\nTotal occurrences: {len(rainbow_lines)}\n')
    
    if len(rainbow_lines) == 2:
        log.write('Both occurrences found - proceeding with replacement\n')
        
        # The second occurrence (index 1) should be replaced
        # Need to find the full <li>...</li> block around line 2
        second_orb_line = rainbow_lines[1][0]
        
        # Search backwards for opening <li>
        li_start = -1
        for i in range(second_orb_line, -1, -1):
            if '<li class="bg-slate-950' in lines[i]:
                li_start = i
                break
        
        # Search forwards for closing </li>
        li_end = -1
        for i in range(second_orb_line, len(lines)):
            if '</li>' in lines[i]:
                li_end = i
                break
        
        log.write(f'Found <li> block from line {li_start+1} to {li_end+1}\n')
        
        if li_start >= 0 and li_end >= 0:
            # Replace the content between li_start and li_end
            # But keep line li_start (opening <li>)
            # Replace from li_start+1 onward with new content
            
            new_li = '''
                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>
'''
            
            # Replace lines between li_start and li_end with new content
            lines[li_start+1:li_end] = [new_li]
            
            # Write back
            with open('src/index.html', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            log.write('Replacement successful!\n')
        else:
            log.write('ERROR: Could not find opening or closing </li>\n')
    else:
        log.write(f'ERROR: Expected 2 occurrences, found {len(rainbow_lines)}\n')
    
    log.close()
    
except Exception as e:
    with open('replacement_log.txt', 'a', encoding='utf-8') as log:
        log.write(f'ERROR: {str(e)}\n')
        import traceback
        log.write(traceback.format_exc())
