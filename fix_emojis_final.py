import re

files_to_fix = [
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html',
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\index.html'
]

for filepath in files_to_fix:
    print(f"\n{'='*60}")
    print(f"Processing: {filepath}")
    print(f"{'='*60}")
    
    try:
        # Read the file with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_len = len(content)
        print(f"File size: {original_len} bytes")
        
        # Count occurrences of "Rastreio de Rainbow Orbs"
        count = content.count('Rastreio de Rainbow Orbs')
        print(f"Found {count} occurrences of 'Rastreio de Rainbow Orbs'")
        
        if count < 2:
            print(f"SKIP: Only {count} occurrences found, need 2")
            continue
        
        # Find both occurrences
        idx1 = content.find('Rastreio de Rainbow Orbs')
        idx2 = content.find('Rastreio de Rainbow Orbs', idx1 + 1)
        
        print(f"First occurrence at: {idx1}")
        print(f"Second occurrence at: {idx2}")
        
        # Get context around each
        ctx1_start = max(0, idx1 - 200)
        ctx1_end = min(len(content), idx1 + 100)
        ctx1 = content[ctx1_start:ctx1_end]
        
        ctx2_start = max(0, idx2 - 200)
        ctx2_end = min(len(content), idx2 + 100)
        ctx2 = content[ctx2_start:ctx2_end]
        
        print(f"\nContext around first occurrence:")
        print(repr(ctx1[:100]))
        print(f"\nContext around second occurrence:")
        print(repr(ctx2[:100]))
        
        # Now do the replacements
        # Strategy: Use multi-step string replacement
        
        # Step 1: Fix the first entry emoji from corrupted char to 🔮
        # The corrupted emoji appears as replacement character before "Rastreio de Rainbow Orbs"
        # Pattern: <span class="text-lg">[corrupted]</span> ... text-purple-400 ... Rastreio de Rainbow Orbs
        
        # Find the pattern more carefully
        pattern_first = (
            r'(<span class="text-lg">).+?(?=</span>\s+\n\s+<div>\s+\n\s+<span[^>]*text-purple-400[^>]*>Rastreio de Rainbow Orbs)'
        )
        
        content_new = re.sub(pattern_first, r'\1🔮', content, count=1, flags=re.DOTALL)
        
        if content_new != content:
            print("\n✓ STEP 1: Fixed first occurrence emoji to 🔮")
            content = content_new
        else:
            print("\n✗ STEP 1: Failed to fix first occurrence")
        
        # Step 2: Fix the second entry
        # Need to change: emoji, title (Rastreio de Rainbow Orbs -> Despertador Cognitivo), 
        # color (text-purple-400 -> text-rose-400), description
        
        # Find the second occurrence more specifically
        # Pattern: <span class="text-lg">[corrupted]</span> ... text-purple-400 ... Rastreio de Rainbow Orbs ... Mapeamento interativo
        
        pattern_second = (
            r'(<span class="text-lg">).+?'
            r'(</span>\s+\n\s+<div>\s+\n\s+<span[^>]*text-purple-400[^>]*>)'
            r'Rastreio de Rainbow Orbs'
            r'(</span>\s+\n\s+<p[^>]*>)'
            r'Mapeamento interativo das 245 orbs\. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas\.'
            r'(</p>)'
        )
        
        replacement_second = (
            r'\1🔔\2Despertador Cognitivo\3'
            r'Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.'
            r'\4'
        )
        
        content_new = re.sub(pattern_second, replacement_second, content, count=1, flags=re.DOTALL)
        
        if content_new != content:
            print("✓ STEP 2: Fixed second occurrence emoji, title, and description")
            content = content_new
        else:
            print("✗ STEP 2: Failed to fix second occurrence")
        
        # Step 3: Fix the color class for second entry
        # Change text-purple-400 to text-rose-400 (only for Despertador Cognitivo)
        pattern_color = (
            r'(<span[^>]*text-)purple-400([^>]*>Despertador Cognitivo)'
        )
        replacement_color = r'\1rose-400\2'
        
        content_new = re.sub(pattern_color, replacement_color, content, count=1)
        
        if content_new != content:
            print("✓ STEP 3: Fixed color class for Despertador Cognitivo")
            content = content_new
        else:
            print("✗ STEP 3: Failed to fix color class")
        
        # Verify the fixes
        if '🔮' in content and '🔔' in content:
            print("\n✓ Both emojis found: 🔮 and 🔔")
        if 'Despertador Cognitivo' in content:
            print("✓ 'Despertador Cognitivo' found")
        if 'text-rose-400 uppercase tracking-widest block">Despertador Cognitivo' in content:
            print("✓ Correct color class for Despertador Cognitivo")
        if 'pulsações neon' in content:
            print("✓ New description found")
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✓✓✓ SUCCESS: {filepath} has been fixed! ✓✓✓")
        
    except Exception as e:
        print(f"\n✗✗✗ ERROR: {filepath}")
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print("ALL PROCESSING COMPLETE")
print(f"{'='*60}")
