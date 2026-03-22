#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

# Change to workspace directory
os.chdir(r'c:\Users\mateu\OneDrive\Documentos\pxg check')

# Files to fix
files = ['src/index.html', 'index.html']

for filepath in files:
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        continue
    
    # Read original file in binary mode
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Decode with error handling
    text = data.decode('utf-8', errors='replace')
    
    # Find the two corrupted Rainbow Orbs entries
    # We'll search for the pattern and replace byte-by-byte
    
    # Find first occurrence of "Rastreio de Rainbow Orbs"
    pattern = 'Rastreio de Rainbow Orbs'
    idx = text.find(pattern)
    
    if idx > 0:
        # Find second occurrence
        idx2 = text.find(pattern, idx + len(pattern))
        
        if idx2 > 0:
            # Get the lines around both occurrences
            # Go back to find the <li> opening tag of the first one
            li_start = text.rfind('\n', 0, idx)
            # Find the closing </li> of the second one
            li_end = text.find('</li>\n', idx2)
            
            if li_start > 0 and li_end > 0:
                # Extract the replacement section
                old_section = text[li_start:li_end+6]
                
                # Build the new section
                new_section = '''
                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔮</span>

                            <div>

                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>

                            </div>

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
                
                # Replace
                new_text = text[:li_start] + new_section + text[li_end+6:]
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_text)
                
                print(f'✓ {filepath} - Fixed!')
            else:
                print(f'✗ {filepath} - Could not find boundaries')
        else:
            print(f'✗ {filepath} - Could not find second entry')
    else:
        print(f'✗ {filepath} - Could not find first entry')

print('Done!')
