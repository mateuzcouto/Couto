#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix corrupted Arsenal section in index.html files"""

import os
import re

def fix_file(filepath):
    """Fix the corrupted Arsenal section in the given HTML file"""
    print(f"\nProcessing: {filepath}")
    
    # Read the file with UTF-8 encoding
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Find position to help with debugging
    orbs_pos = content.find('Rastreio de Rainbow Orbs')
    if orbs_pos == -1:
        print(f"ERROR: Could not find 'Rastreio de Rainbow Orbs' in {filepath}")
        return False
    
    print(f"Found first 'Rastreio de Rainbow Orbs' at position {orbs_pos}")
    
    # Print some context around it to see the corrupted emoji
    print(f"Context before first:  {repr(content[orbs_pos-100:orbs_pos])}")
    
    # Find the second occurrence
    orbs_pos2 = content.find('Rastreio de Rainbow Orbs', orbs_pos + 1)
    if orbs_pos2 == -1:
        print(f"ERROR: Could not find second 'Rastreio de Rainbow Orbs' in {filepath}")
        return False
        
    print(f"Found second 'Rastreio de Rainbow Orbs' at position {orbs_pos2}")
    print(f"Context before second: {repr(content[orbs_pos2-100:orbs_pos2])}")
    
    # Build the replacement section
    # We need to replace from the start of the first entry through the end of the second
    # to capture and fix both entries
    
    # Find the start of first entry (look backward for <li class...)
    start_search = content.rfind('<li class="bg-slate-950', 0, orbs_pos)
    print(f"First entry starts at: {start_search}")
    
    # Find the end of second entry (look forward for closing </li>)
    end_search = content.find('</li>', orbs_pos2)
    # Need to make sure we get to the closing of the second entry
    temp_search = content.find('</li>', orbs_pos)
    end_search = content.find('</li>', content.find('</li>', temp_search) + 1)
    print(f"Second entry ends around: {end_search}")
    
    # Extract the section to understand structure
    problem_section = content[start_search:end_search+5]
    print(f"\n=== PROBLEM SECTION ===\n{problem_section[:500]}\n...")
    
    # Create the replacement with correct emojis and structure
    replacement = '''                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

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
    
    # Replace the section
    new_content = content[:start_search] + replacement + content[end_search+5:]
    
    # Write back with UTF-8 encoding
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Fixed {filepath}")
    return True

# Fix both files
files = [
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html',
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\index.html'
]

for filepath in files:
    if os.path.exists(filepath):
        try:
            fix_file(filepath)
        except Exception as e:
            print(f"ERROR fixing {filepath}: {e}")
    else:
        print(f"File not found: {filepath}")

print("\nDone!")
