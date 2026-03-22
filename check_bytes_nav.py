#!/usr/bin/env python3
with open('index.html', 'rb') as f:
    content = f.read()

def show_segment(label, anchor, offset=-80, length=80):
    idx = content.find(anchor)
    if idx < 0:
        print(f'{label}: NOT FOUND')
        return
    seg = content[max(0,idx+offset):idx+offset+length]
    print(f'{label} (anchor pos={idx}):')
    hex_row = ''
    chr_row = ''
    for b in seg:
        hex_row += f'{b:02x} '
        chr_row += chr(b) if 32 <= b < 127 else '.'
    print(f'  HEX: {hex_row}')
    print(f'  CHR: {chr_row}')

show_segment('Nav Treinadores', b'Treinadores', offset=-80, length=80)
show_segment('Nav Rainbow Orbs', b'Rainbow Orbs', offset=-80, length=80)
show_segment('Nav Ranking', b'Ranking</span', offset=-80, length=80)
show_segment('Nav Guias F2P', b'Guias F2P', offset=-80, length=80)
show_segment('Nav Pokelog', b'Pok\xef\xbf\xbdlog', offset=-80, length=80)
show_segment('Nav Admin', b'Painel Admin', offset=-80, length=80)

# Also check admin tabs
show_segment('Admin Feedbacks tab', b'Feedbacks</button', offset=-40, length=40)
show_segment('Admin Estatisticas tab', b'Estat\xef\xbf\xbdsticas</button', offset=-40, length=40)
