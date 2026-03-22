import os

def fix_arsenal(filepath):
    """Simpler fix using string replacement with file read/write"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    print(f"Processing {filepath}...")
    
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Check if content has the markers
        if 'Telemetria Financeira' not in content:
            print("ERROR: Telemetria Financeira not found")
            return
        
        if 'Rastreio de Rainbow Orbs' not in content:
            print("ERROR: Rastreio de Rainbow Orbs not found")  
            return
        
        # Find unique boundaries
        # Start: after Telemetria item
        # End: starting from Táticas F2P
        
        price = content.find('Telemetria Financeira')
        f2p_start = content.find('Táticas F2P (Anti-Inflação)')
        
        if price < 0 or f2p_start < 0:
            print("ERROR: Could not find landmarks")
            return
        
        #Find the <li containing Telemetria
        li_telemetria_start = content.rfind('<li class="bg-slate-950', 0, price)
        li_telemetria_end = content.find('</li>', price) + 5
        
        # Find the <li containing F2P
        li_f2p_start = content.rfind('<li class="bg-slate-950', 0, f2p_start)
        li_f2p_end = content.find('</li>', f2p_start) + 5
        
        print(f"Telemetria item: {li_telemetria_start}-{li_telemetria_end}")
        print(f"F2P item: {li_f2p_start}-{li_f2p_end}")
        
        # Extract items we want to keep
        telemetria_html = content[li_telemetria_start:li_telemetria_end]
        f2p_html = content[li_f2p_start:li_f2p_end]
        
        # New entries
        orbs_html = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔮</span>

                            <div>

                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>

                            </div>

                        </li>'''
        
        despertador_html = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
        
        # Build new section
        between = telemetria_html + '\n\n                        ' + orbs_html + '\n\n                        ' + despertador_html + '\n\n                        ' + f2p_html
        
        # Replace
        new_content = content[:li_telemetria_start] + between + content[li_f2p_end:]
        
        # Find the item after F2P (Radar) and keep it
        radar_pos = content.find('Radar de atualizações (Pokélog)')
        if radar_pos > 0:
            li_radar_start = content.rfind('<li class="bg-slate-950', li_f2p_end, radar_pos)
            li_radar_end = content.find('</li>', radar_pos) + 5
            radar_html = content[li_radar_start:li_radar_end]
            new_content = content[:li_telemetria_start] + between + '\n\n                        ' + radar_html + content[li_radar_end:]
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"SUCCESS: Fixed {filepath}")
        
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

# Fix both files
files = [
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html',
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\index.html'
]

for f in files:
    fix_arsenal(f)

print("DONE!")
