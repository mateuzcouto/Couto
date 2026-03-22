#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# Read the file
with open('src/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and verify both occurrences
count = content.count('Rastreio de Rainbow Orbs')
print(f'Found {count} occurrences of "Rastreio de Rainbow Orbs"')

# Create the pattern and replacement - match both orbs entries and replace second with Despertador
# This pattern matches the first <li> with first Rainbow Orbs and the second <li> with duplicate Rainbow Orbs
pattern = r'(<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\s*<span class="text-lg">🔮</span>\s*<div>\s*<span class="text-\[10px\] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>\s*<p class="text-\[10px\] text-slate-400 font-medium mt-0\.5 leading-snug">Mapeamento interativo das 245 orbs\. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas\.</p>\s*</div>\s*</li>)\s*(<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\s*<span class="text-lg">🔮</span>\s*<div>\s*<span class="text-\[10px\] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>\s*<p class="text-\[10px\] text-slate-400 font-medium mt-0\.5 leading-snug">Mapeamento interativo das 245 orbs\. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas\.</p>\s*</div>)'

replacement = r'\1                        </li>\n\n                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n\n                            <span class="text-lg">🔔</span>\n\n                            <div>\n\n                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>\n\n                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>\n\n                            </div>'

# Try the regex replacement
new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)

if new_content != content:
    print('\nReplacement successful!')
    with open('src/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('File updated: src/index.html')
    
    # Verify the changes
    with open('src/index.html', 'r', encoding='utf-8') as f:
        updated = f.read()
    
    despertador_count = updated.count('Despertador Cognitivo')
    orbs_count = updated.count('Rastreio de Rainbow Orbs')
    print(f'\nVerification:')
    print(f'  - "Rastreio de Rainbow Orbs": {orbs_count}')
    print(f'  - "Despertador Cognitivo": {despertador_count}')
    print(f'✓ Changes applied successfully!')
else:
    print('\nNo regex match found - file unchanged')
    print('Trying alternative approach with simpler pattern...')
