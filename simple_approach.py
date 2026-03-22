import os
os.chdir(r'c:\Users\mateu\OneDrive\Documentos\pxg check')

# Just fix with simple string replacement for both files
for fname in ['index.html', 'src/index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Count rainbow orbs
    count = text.count('Rastreio de Rainbow Orbs')
    print(f'{fname}: {count} occurrences')
    
    # Simple approach: split by the common section and rebuild
    # Find "Telemetria Financeira" as anchor
    anchor = '<span class="text-[10px] font-black text-amber-400 uppercase tracking-widest block">Telemetria Financeira</span>'
    
    if anchor in text:
        parts = text.split(anchor)
        print(f'Split successfully for {fname}')
        
        # Find the FIRST occurrence of the problematic section after Telemetria
        after_telemetria = parts[1]
        
        # Find the </li></li> sequence that marks end of the problem section
        # Look for pattern: first </li> then another </li>
        
        # Find the first two <li> with Rastreio
        first_rastreio_pos = after_telemetria.find('Rastreio de Rainbow Orbs')
        second_rastreio_pos = after_telemetria.find('Rastreio de Rainbow Orbs', first_rastreio_pos + 1)
        
        if first_rastreio_pos > 0 and second_rastreio_pos > first_rastreio_pos:
            # Find closing </li> for second one
            closing_li = after_telemetria.find('</li>', second_rastreio_pos) + 5
            
            # Everything before first Rastreio
            before_problem = after_telemetria[:first_rastreio_pos]
            
            # Find opening <li> by going backwards
            li_open = before_problem.rfind('<li class="bg-slate-950')
            before_bad_lis = after_telemetria[:li_open]
            
            # After closing </li> of second Rainbow
            after_bad_lis = after_telemetria[closing_li:]
            
            # Reconstruct with correct entries
            correct_section = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

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
            
            # Rebuild the file
            new_text = parts[0] + anchor + before_bad_lis + correct_section + after_bad_lis
            
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_text)
            
            print(f'✓ {fname} fixed!')
