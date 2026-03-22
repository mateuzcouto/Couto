#!/usr/bin/env python3
# Fix corrupted Rainbow Orbs and Despertador Cognitivo entries

for filename in ['src/index.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the indices of the corrupted entries
    idx1 = content.find('Rastreio de Rainbow Orbs')
    idx2 = content.find('Rastreio de Rainbow Orbs', idx1 + 1)
    
    if idx1 > 0 and idx2 > idx1:
        # Find the start of the first <li> and end of second </li>
        li_start_1 = content.rfind('<li class="bg-slate-950', 0, idx1)
        li_end_2 = content.find('</li>', idx2) + len('</li>')
        
        if li_start_1 > 0 and li_end_2 > idx2:
            # Create the replacement text
            new_text = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

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
            
            # Replace in content
            new_content = content[:li_start_1] + new_text + content[li_end_2:]
            
            # Write back
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f'✓ {filename} fixed successfully!')
        else:
            print(f'✗ {filename}: Could not find list item boundaries')
    else:
        print(f'✗ {filename}: Could not find two Rainbow Orbs entries')
