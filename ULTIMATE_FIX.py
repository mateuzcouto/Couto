#!/usr/bin/env python3
"""Direct byte-level fix for Arsenal section"""
import os

os.chdir(r'c:\Users\mateu\OneDrive\Documentos\pxg check')

for filepath in ['index.html', 'src/index.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strategy: Find the Telemetria Financeira section, then replace the next two items
    
    # Find position of Telemetria
    telemetria_pos = content.find('Telemetria Financeira')
    if telemetria_pos < 0:
        print(f'ERROR: Could not find Telemetria in {filepath}')
        continue
    
    # Find the </li> after Telemetria
    telemetria_close = content.find('</li>', telemetria_pos) + 5
    
    # Now we need to replace the NEXT TWO <li> entries
    # Find first <li> after Telemetria
    first_li_start = content.find('<li class="bg-slate-950', telemetria_close)
    first_li_close = content.find('</li>', first_li_start) + 5
    
    # Find second <li> after first
    second_li_start = content.find('<li class="bg-slate-950', first_li_close)
    second_li_close = content.find('</li>', second_li_start) + 5
    
    if first_li_start > 0 and second_li_close > 0:
        # Create the replacement entries with Portuguese characters correctly encoded
        replacement = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔮</span>

                            <div>

                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>

                            </div>

                        </li>'''
        
        # Perform the replacement
        new_content = content[:first_li_start] + replacement + content[second_li_close:]
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'✓ Fixed {filepath}')
    else:
        print(f'ERROR in {filepath}: Could not find li boundaries')
