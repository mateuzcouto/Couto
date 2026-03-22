#!/usr/bin/env python3
import sys, os
os.chdir(r'c:\Users\mateu\OneDrive\Documentos\pxg check')
for fp in ['src/index.html', 'index.html']:
    with open(fp, 'rb') as f: data = f.read()
    search = b'<span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>'
    pos1 = data.find(search)
    pos2 = data.find(search, pos1+1) if pos1 != -1 else -1
    if pos1 > 0 and pos2 > 0:
        # Fix first emoji
        li_start = data.rfind(b'<li class="bg-slate-950', 0, pos1)
        emoji_start = data.rfind(b'<span class="text-lg">', 0, pos1)
        emoji_end = data.find(b'</span>', emoji_start) + 7
        emoji_new = b'<span class="text-lg">\xf0\x9f\x94\xae</span>'
        data = data[:emoji_start] + emoji_new + data[emoji_end:]
        
        # Fix second entry - find and replace entire li
        li_start2 = data.rfind(b'<li class="bg-slate-950', 0, pos2)
        li_end2 = data.find(b'</li>', pos2) + 5
        new_li2 = b'''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">
                            <span class="text-lg">\xf0\x9f\x94\x94</span>
                            <div>
                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>
                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulacao visual (pulsacoes neon) e audio dinamico despachado 5 minutos antes da iniciacao de Globais e Pokeparks.</p>
                            </div>
                        </li>'''
        data = data[:li_start2] + new_li2 + data[li_end2:]
        with open(fp, 'wb') as f: f.write(data)
        print(f'Fixed {fp}')
    else:
        print(f'ERROR in {fp}: pos1={pos1}, pos2={pos2}')
