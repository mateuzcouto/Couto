#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix corrupted Arsenal entries by working at the byte level
"""

def fix_file(filepath):
    print(f"\nFixing: {filepath}")
    
    # Read the file as bytes
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())
    
    # Find the two occurrences of "Rastreio de Rainbow Orbs" marker within the Arsenal section
    # We'll use the landmarks "Telemetria Financeira" and "Radar de atualizações"
    
    # These are unique points
    telemetria_pos = data.find(b'Telemetria Financeira')
    radar_pos = data.find(b'Radar de atualiza')  # Use partial to avoid encoding issues
    
    if telemetria_pos < 0 or radar_pos < 0:
        print("ERROR: Could not find landmarks")
        return False
    
    print(f"Found Telemetria at: {telemetria_pos}")
    print(f"Found Radar at: {radar_pos}")
    
    # Find the section boundaries
    # Go back from Telemetria find to find opening <li after header
    section_start = data.rfind(b'<li class="bg-slate-950', 0, telemetria_pos)
    if section_start < 0:
        section_start = data.rfind(b'<li', 0, telemetria_pos)
    
    # Go forward from Radar to find closing </li>
    section_end = data.find(b'</li>\n\n                    </ul>', radar_pos)
    if section_end < 0:
        section_end = data.find(b'</li>', radar_pos) + 5
    
    print(f"Section boundaries: {section_start} to {section_end}")
    
    # Build the replacement
    replacement = b'''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">\xf0\x9f\x94\xae</span>

                            <div>

                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>

                            </div>

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">\xf0\x9f\x94\x94</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">\xf0\x9f\x92\xa1</span>

                            <div>

                                <span class="text-[10px] font-black text-cyan-400 uppercase tracking-widest block">Táticas F2P (Anti-Inflação)</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Metodologia validada para níveis 400+. Permite concluir desafios mecânicos complexos baseando-se em sinergia, contornando a dependência de TMs com preços absurdos no mercado.</p>

                            </div>

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">\xf0\x9f\x93\xa1</span>

                            <div>

                                <span class="text-[10px] font-black text-blue-400 uppercase tracking-widest block">Radar de atualizações (Pokélog)</span>'''
    
    # Build the full content
    before_section = data[:section_start]
    # Find the "Telemetria Financeira" item end and Radar item start to preserve them
    # Actually, let's be more careful - we want to keep everything before Telemetria Financeira
    # and after Radar de atualizações
    
    # Better approach: find the opening <li... for Telemetria
    telemetria_li_start = data.rfind(b'<li', 0, telemetria_pos)
    telemetria_li_end = data.find(b'</li>', telemetria_pos) + 5
    
    # Find the opening <li... for Radar
    radar_li_start = data.rfind(b'<li', 0, radar_pos)
    radar_li_end = data.find(b'</li>', radar_pos) + 5
    
    print(f"Telemetria item: {telemetria_li_start} to {telemetria_li_end}")
    print(f"Radar item: {radar_li_start} to {radar_li_end}")
    
    # Extract the Telemetria and Radar items exactly
    telemetria_item = data[telemetria_li_start:telemetria_li_end]
    radar_item = data[radar_li_start:radar_li_end]
    
    # Build complete replacement
    complete_replacement = (
        data[:telemetria_li_start] +
        telemetria_item +
        b'\n\n                        ' +
        b'<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n\n                            <span class="text-lg">\xf0\x9f\x94\xae</span>\n\n                            <div>\n\n                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>\n\n                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>\n\n                            </div>\n\n                        </li>\n\n                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n\n                            <span class="text-lg">\xf0\x9f\x94\x94</span>\n\n                            <div>\n\n                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>\n\n                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>\n\n                            </div>\n\n                        </li>\n\n                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n\n                            <span class="text-lg">\xf0\x9f\x92\xa1</span>\n\n                            <div>\n\n                                <span class="text-[10px] font-black text-cyan-400 uppercase tracking-widest block">Táticas F2P (Anti-Inflação)</span>\n\n                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Metodologia validada para níveis 400+. Permite concluir desafios mecânicos complexos baseando-se em sinergia, contornando a dependência de TMs com preços absurdos no mercado.</p>\n\n                            </div>\n\n                        </li>\n\n                        ' +
        radar_item +
        data[radar_li_end:]
    )
    
    # Write back
    with open(filepath, 'wb') as f:
        f.write(complete_replacement)
    
    print(f"✓ Fixed {filepath}")
    return True

files = [
    'c:/Users/mateu/OneDrive/Documentos/pxg check/src/index.html',
    'c:/Users/mateu/OneDrive/Documentos/pxg check/index.html'
]

for filepath in files:
    try:
        import os
        if os.path.exists(filepath):
            fix_file(filepath)
        else:
            # Try with backslashes
            filepath_alt = filepath.replace('/', '\\')
            if os.path.exists(filepath_alt):
                fix_file(filepath_alt)
            else:
                print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

print("\nDone!")
