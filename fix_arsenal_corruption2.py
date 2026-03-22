#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix corrupted Arsenal section using regex pattern matching"""

import os
import re

def fix_file(filepath):
    """Fix the corrupted Arsenal section in the given HTML file"""
    print(f"\nProcessing: {filepath}")
    
    # Read the file
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Pattern to match two consecutive "Rastreio de Rainbow Orbs" entries with corrupted emojis
    # The pattern matches: <li...> ... Rastreio de Rainbow Orbs ... </li> (first entry)
    # Followed by: <li...> ... Rastreio de Rainbow Orbs ... </li> (second entry, to be replaced)
    
    # This regex will match the problematic section
    pattern = r'(<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\s*<span class="text-lg">[^<]*</span>\s*<div>\s*<span class="text-\[10px\] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>\s*<p class="text-\[10px\] text-slate-400 font-medium mt-0\.5 leading-snug">Mapeamento interativo das 245 orbs\..*?</li>)\s*(<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\s*<span class="text-lg">[^<]*</span>\s*<div>\s*<span class="text-\[10px\] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>\s*<p class="text-\[10px\] text-slate-400 font-medium mt-0\.5 leading-snug">Mapeamento interativo das 245 orbs\..*?</li>)'
    
    def replace_func(match):
        # Keep the first entry but fix its emoji
        first_entry = match.group(1)
        # Replace the corrupted emoji with 🔮
        first_fixed = re.sub(
            r'<span class="text-lg">[^<]*</span>',
            '<span class="text-lg">🔮</span>',
            first_entry,
            count=1
        )
        
        # Create the replacement for the second entry
        replacement = '''                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
        
        return first_fixed + '\n\n                        ' + replacement
    
    # Try the regex replacement
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"WARNING: Regex pattern did not match. Trying alternative approach...")
        # Alternative: look for the exact text pattern more loosely
        # Just search for the two consecutive Rastreio entries and replace them
        
        # First, let's find where to split based on text content uniqueness
        # Find "Telemetria Financeira" and "Táticas F2P" as landmarks
        
        tel_pos = content.find('Telemetria Financeira')
        tactical_pos = content.find('Táticas F2P')
        
        if tel_pos > 0 and tactical_pos > 0:
            # Find the opening <li> before Telemetria
            search_start = content.rfind('<li', 0, tel_pos)
            # Find the closing </li> after Táticas but before next item
            search_end = content.find('</li>', tactical_pos) + 5
            
            # Extract the section
            before = content[:search_start]
            section = content[search_start:search_end]
            after = content[search_end:]
            
            print(f"Found section between Telemetria and Táticas F2P")
            
            # Build replacement section with all items
            new_section = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">💰</span>

                            <div>

                                <span class="text-[10px] font-black text-amber-400 uppercase tracking-widest block">Telemetria Financeira</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Painel de fluxo de caixa que compila matematicamente os lucros líquidos diários, semanais e mensais de cada personagem.</p>

                            </div>

                        </li>

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

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">💡</span>

                            <div>

                                <span class="text-[10px] font-black text-cyan-400 uppercase tracking-widest block">Táticas F2P (Anti-Inflação)</span>'''
            
            new_content = before + new_section + after
        else:
            print(f"ERROR: Could not find Telemetria Financeira or Táticas F2P")
            return False
    
    # Write back
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
            import traceback
            traceback.print_exc()
    else:
        print(f"File not found: {filepath}")

print("\nDone!")
