import sys
# Read and fix the corrupted file

filepath = 'src/index.html'

# Read the file as binary
with open(filepath, 'rb') as fh:
    content_bytes = fh.read()

# Try to decode - corrupted bytes might appear as replacement chars
content = content_bytes.decode('utf-8', errors='replace')

# Count occurrences
count_rainbow = content.count('Rastreio de Rainbow Orbs')
print(f'Found {count_rainbow} occurrences of "Rastreio de Rainbow Orbs"')

# If we have 2, we need to fix them
if count_rainbow == 2:
    # Find where they start
    idx = -1
    for i in range(2):
        idx = content.find('Rastreio de Rainbow Orbs', idx + 1)
        print(f'Occurrence {i+1} at position {idx}')
    
    # Now work with the raw bytes more carefully
    # We can't easily match the corrupted emoji, so let's search for patterns before and after
    
    # Look for: <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>
    # and find both instances
    
    # Let's split by this pattern
    parts = content.split('<span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>')
    
    if len(parts) == 3:  # Before Rainbow 1, between, after Rainbow 2
        print(f'Successfully split into {len(parts)} parts')
        
        # Now rebuild with correct emojis
        result = parts[0]  # Everything before first Rainbow
        
        # Add first Rainbow with correct emoji
        result += '<span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>'
        result += parts[1]  # The middle part (between the two rainbows)
        
        # Replace the middle part's title and emoji
        # The middle part contains "<li class...> <span class="text-lg">...</span> <div>..."
        # We need to find and replace the Rainbow title with Despertador
        
        middle = parts[1]
        
        # Find the first occurrence of "Rastreio de Rainbow Orbs" in middle
        idx_middle =middle.find('Rastreio de Rainbow Orbs')
        if idx_middle > -1:
            # This should be replaced with Despertador
            middle_replaced = middle[:idx_middle] + 'Despertador Cognitivo' + middle[idx_middle + len('Rastreio de Rainbow Orbs'):]
            
            # Now also fix the emoji and color in the <span class="text-[10px]..."> part
            # Replace text-purple-400 with text-rose-400 in this middle section
            # Be careful - only replace in the specific part
            
            # Go back in the middle_replaced to find the <span class="text-lg">?</span>
            # Pattern: <span class="text-lg">[any char]</span> before <span class="text-[10px]...>Despertador
            
            li_idx = middle_replaced.rfind('<li class="bg-slate-950 rounded-xl p-3')
            if li_idx > -1:
                before_li = middle_replaced[:li_idx]
                from_li = middle_replaced[li_idx:]
                
                # Find the emoji span and the text-purple-400
                emoji_end = from_li.find('</span>')
                if emoji_end > -1:
                    # Replace the emoji span with correct emoji
                    before_emoji = from_li[:from_li.find('<span class="text-lg">')+len('<span class="text-lg">')]
                    after_emoji_open = from_li[from_li.find('</span>'):]
                    
                    # Now find "text-purple-400" in the rest and replace with "text-rose-400"
                    rest = after_emoji_open
                    rest = rest.replace('text-purple-400', 'text-rose-400', 1)
                    
                    from_li = before_emoji + '🔔' + rest
                    middle_replaced = before_li + from_li
        
        # Also fix the first emoji (should be 🔮)
        # Find the <span class="text-lg"> before "Rastreio de Rainbow Orbs" and fix it
        parts_fixed = parts[0] + '<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">\n\n                            <span class="text-lg">🔮</span>'
        
        # Continue building
        result = parts_fixed + parts[1]
        
        # Find and replace the second occurrence
        idx2 = result.find('<span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>')
        if idx2 > -1:
            # Go back to find the <li> for this one
            li_back = result.rfind('<li class="bg-slate-950', 0, idx2)
            if li_back > -1:
                # Find the </li> for this one
                li_close = result.find('</li>', idx2)
                if li_close > -1:
                    # Get the section to replace
                    old_section = result[li_back:li_close+5]
                    
                    # Build the new section
                    new_li = '''<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>'''
                    
                    # Remove old and add new
                    fixed = result[:li_back] + new_li + result[li_close+5:]
                    
                    # Write back
                    with open(filepath, 'w', encoding='utf-8') as fw:
                        fw.write(fixed)
                    
                    print('✓ src/index.html fixed!')
                else:
                    print('Could not find closing </li>')
            else:
                print('Could not find opening <li>')
        else:
            print('Could not find second Rainbow pattern')
    else:
        print(f'Split resulted in {len(parts)} parts, expected 3')

print('Done!')
