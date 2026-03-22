#!/usr/bin/env python3
# Read file and fix the corrupted entries by rewriting the entire file

filepath = 'src/index.html'

# Read file as bytes to handle encoding issues
with open(filepath, 'rb') as f:
    content_bytes = f.read()

# Convert to string
content_str = content_bytes.decode('utf-8', errors='ignoreif')

# Find the section and do replacements
# We'll search for the unique pattern: '<span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>'
# And replace the emoji spans before it

# Strategy: Find both occurrences and fix them separately

# First, split by the title span to find where the emoji should be
pattern_title = '<span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>'
pattern_emoji_open = '<span class="text-lg">'
pattern_emoji_close = '</span>'

# Find first occurrence
idx1 = content_str.find(pattern_title)
if idx1 > 0:
    # Go back to find the emoji span
    emoji_start = content_str.rfind(pattern_emoji_open, 0, idx1)
    emoji_end = content_str.find(pattern_emoji_close, emoji_start)
   
    if emoji_start > 0 and emoji_end > emoji_start:
        # Fix first emoji: replace whatever is between tags with 🔮
        old_emoji_1 = content_str[emoji_start:emoji_end+len(pattern_emoji_close)]
        new_emoji_1 = '<span class="text-lg">🔮</span>'
        content_str = content_str[:emoji_start] + new_emoji_1 + content_str[emoji_end+len(pattern_emoji_close):]

# Find second occurrence
idx2 = content_str.find(pattern_title, idx1 + len(pattern_title))
if idx2 > 0:
    # Go back to find the emoji span for the second one
    emoji_start_2 = content_str.rfind(pattern_emoji_open, 0, idx2)
    emoji_end_2 = content_str.find(pattern_emoji_close, emoji_start_2)
    
    if emoji_start_2 > 0 and emoji_end_2 > emoji_start_2:
        # Find the full li element for this second one
        li_start = content_str.rfind('<li class="bg-slate-950', 0, idx2)
        li_end = content_str.find('</li>', idx2) + len('</li>')
        
        if li_start > 0 and li_end > idx2:
            # Replace the entire second entry
            old_entry = content_str[li_start:li_end]
            
            new_entry = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
            
            content_str = content_str[:li_start] + new_entry + content_str[li_end:]

# Write the fixed content
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content_str)

print('✓ src/index.html fixed!')

# Do the same for index.html
filepath2 = 'index.html'

with open(filepath2, 'rb') as f:
    content_bytes2 = f.read()

content_str2 = content_bytes2.decode('utf-8', errors='ignore')

# Apply the same fixes
idx1 = content_str2.find(pattern_title)
if idx1 > 0:
    emoji_start = content_str2.rfind(pattern_emoji_open, 0, idx1)
    emoji_end = content_str2.find(pattern_emoji_close, emoji_start)
   
    if emoji_start > 0 and emoji_end > emoji_start:
        new_emoji_1 = '<span class="text-lg">🔮</span>'
        content_str2 = content_str2[:emoji_start] + new_emoji_1 + content_str2[emoji_end+len(pattern_emoji_close):]

idx2 = content_str2.find(pattern_title, idx1 + len(pattern_title))
if idx2 > 0:
    emoji_start_2 = content_str2.rfind(pattern_emoji_open, 0, idx2)
    emoji_end_2 = content_str2.find(pattern_emoji_close, emoji_start_2)
    
    if emoji_start_2 > 0 and emoji_end_2 > emoji_start_2:
        li_start = content_str2.rfind('<li class="bg-slate-950', 0, idx2)
        li_end = content_str2.find('</li>', idx2) + len('</li>')
        
        if li_start > 0 and li_end > idx2:
            new_entry = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
            
            content_str2 = content_str2[:li_start] + new_entry + content_str2[li_end:]

with open(filepath2, 'w', encoding='utf-8') as f:
    f.write(content_str2)

print('✓ index.html fixed!')
print('Done!')
