#!/usr/bin/env python3
# Very simple line-based fix

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    rainbow_count = 0
    fixed = False
    
    for i, line in enumerate(lines):
        if 'Rastreio de Rainbow Orbs' in line and'text-purple-400' in line:
            rainbow_count += 1
            if rainbow_count == 1:
                # First one - no change needed to title
                pass
            elif rainbow_count == 2:
                # Second one - change to Despertador
                lines[i] = line.replace('Rastreio de Rainbow Orbs', 'Despertador Cognitivo').replace('text-purple-400', 'text-rose-400')
                fixed = True
        
        # Fix emojis - look for lines with just emoji span
        if '<span class="text-lg">' in line and '</span>' in line:
            # Check if the next meaningful line is Rainbow Orbs
            for j in range(i+1, min(i+10, len(lines))):
                if 'Rastreio de Rainbow Orbs' in lines[j]:
                    if j-i < 8:  # Close enough
                        rainbow_num = sum(1 for k in range(j) if 'Rastreio de Rainbow Orbs' in lines[k])
                        if rainbow_num == 1 and '🔮' not in line:
                            # First Rainbow - fix to 🔮
                            lines[i] = line.replace('</span>', '🔮</span>').replace('<span class="text-lg">', '<span class="text-lg">')
                            fixed = True
                        elif rainbow_num == 2 and '🔔' not in line:
                            # Second Rainbow(should be Despertador) - fix to 🔔
                            lines[i] = line.replace('</span>', '🔔</span>').replace('<span class="text-lg">', '<span class="text-lg">')
                            fixed = True
                    break
    
    if fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    return False

try:
    for f in ['src/index.html', 'index.html']:
        if fix_file(f):
            print(f'✓ Fixed {f}')
        else:
            print(f'⚠ No changes made to {f}')
except Exception as e:
    print(f'ERROR: {e}')
