#!/usr/bin/env python3
"""
Fix corrupted Arsenal de Otimização section
Replaces duplicate Rainbow Orbs entries with correct content
"""

import os
import re

os.chdir(r'c:\Users\mateu\OneDrive\Documentos\pxg check')

def fix_arsenal_section(filepath):
    """Fix the Arsenal section in the given HTML file"""
    print(f"\n=== Processing {filepath} ===")
    
    # Read the file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading: {e}")
        return False
    
    # Find all occurrences of the title
    pattern = r'<span class="text-\[10px\] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>'
    matches = list(re.finditer(pattern, content))
    
    print(f"Found {len(matches)} occurrences of 'Rastreio de Rainbow Orbs'")
    
    if len(matches) != 2:
        print(f"ERROR: Expected 2 occurrences, found {len(matches)}")
        return False
    
    # Find the <li> containers
    pos1 = matches[0].start()
    pos2 = matches[1].start()
    
    # Go backwards to find opening <li> for first
    li_open_1 = content.rfind('<li class="bg-slate-950', 0, pos1)
    li_close_1 = content.find('</li>', pos1) + 5
    
    # Go backwards to find opening <li> for second
    li_open_2 = content.rfind('<li class="bg-slate-950', 0, pos2)
    li_close_2 = content.find('</li>', pos2) + 5
    
    print(f"First entry: positions {li_open_1}-{li_close_1}")
    print(f"Second entry: positions {li_open_2}-{li_close_2}")
    
    if li_open_1 < 0 or li_close_1 <= pos1 or li_open_2 < 0 or li_close_2 <= pos2:
        print("ERROR: Could not find <li> boundaries")
        return False
    
    # Create replacements
    new_entry_1 = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔮</span>

                            <div>

                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>

                            </div>

                        </li>'''
    
    new_entry_2 = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
    
    # Replace in reverse order (so positions don't shift)
    content = content[:li_open_2] + new_entry_2 + content[li_close_2:]
    content = content[:li_open_1] + new_entry_1 + content[li_close_1:]
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ File updated successfully")
        return True
    except Exception as e:
        print(f"ERROR writing: {e}")
        return False

# Fix both files
if __name__ == '__main__':
    print("=" * 50)
    print("Arsenal de Otimização Section Fixer")
    print("=" * 50)
    
    results = {}
    for filepath in ['src/index.html', 'index.html']:
        results[filepath] = fix_arsenal_section(filepath)
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    for filepath, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{filepath}: {status}")
    print("=" * 50)
