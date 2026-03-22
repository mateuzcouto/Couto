#!/usr/bin/env python3
import os
import sys

filepath = r'c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html'

# Write execution proof immediately
with open(r'c:\Users\mateu\OneDrive\Documentos\pxg check\exec_proof.txt', 'w') as f:
    f.write('Script started\n')
    f.write(f'File: {filepath}\n')
    f.write(f'File exists: {os.path.exists(filepath)}\n')
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as html:
            content = html.read()
        
        f.write(f'File read successfully, length: {len(content)}\n')
        
        # Count Rastreio occurrences
        count = content.count('Rastreio de Rainbow Orbs')
        f.write(f'Found {count} "Rastreio de Rainbow Orbs" entries\n')
        
        # Find landmarks
        tel_pos = content.find('Telemetria Financeira')
        f2p_pos = content.find('Táticas F2P')
        f.write(f'Telemetria at: {tel_pos}\n')
        f.write(f'F2P at: {f2p_pos}\n')
        
        if tel_pos > 0 and f2p_pos > 0 and count == 2:
            f.write('\n=== READY TO FIX ===\n')
            f.write('Attempting fix...\n')
            
            # Find the li blocks
            li_tel_start = content.rfind('<li class="bg-slate-950', 0, tel_pos)
            li_tel_end = content.find('</li>', tel_pos) + 5
            
            li_f2p_start = content.rfind('<li class="bg-slate-950', 0, f2p_pos)
            li_f2p_end = content.find('</li>', f2p_pos) + 5
            
            f.write(f'Telemetria li: {li_tel_start} to {li_tel_end}\n')
            f.write(f'F2P li: {li_f2p_start} to {li_f2p_end}\n')
            
            # Extract items
            tel_html = content[li_tel_start:li_tel_end]
            f2p_html = content[li_f2p_start:li_f2p_end]
            
            # Build new section
            new_section = (
                content[:li_tel_start] +
                tel_html + '\n\n                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n'
                '                            <span class="text-lg">🔮</span>\n'
                '                            <div>\n'
                '                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>\n'
                '                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>\n'
                '                            </div>\n'
                '                        </li>\n\n                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n'
                '                            <span class="text-lg">🔔</span>\n'
                '                            <div>\n'
                '                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>\n'
                '                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>\n'
                '                            </div>\n'
                '                        </li>\n\n                        ' +
                f2p_html +
                content[li_f2p_end:]
            )
            
            # Write the fixed content
            with open(filepath, 'w', encoding='utf-8') as html:
                html.write(new_section)
            
            f.write('FIX COMPLETED!\n')
            
            # Verify
            with open(filepath, 'r', encoding='utf-8', errors='replace') as verify:
                fixed = verify.read()
            
            f.write(f'Verification - new length: {len(fixed)}\n')
            f.write(f'Despertador count: {fixed.count("Despertador Cognitivo")}\n')
            f.write('SUCCESS!')
        else:
            f.write('ERROR: Unable to apply fix\n')
            
    except Exception as e:
        f.write(f'EXCEPTION: {str(e)}\n')
        import traceback
        f.write(traceback.format_exc())

print("Check exc_proof.txt for results")
