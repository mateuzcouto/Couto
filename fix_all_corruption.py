#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE FIX: Restore all ?? (literal question marks from emoji encoding failure)
and U+FFFD (replacement chars from accented-char encoding failure) in index.html and src/index.html.

Root cause:
  - Set-Content without -Encoding UTF8 wrote file as ANSI/CP1252
    → emoji → '?' (0x3F each codepoint)
    → accented chars preserved as single CP1252 bytes (e.g. é→0xE9, ã→0xE3)
  - Then Get-Content -Encoding UTF8 on the CP1252 file
    → the CP1252 bytes for accented chars (0xE0-0xFF) were misread as UTF-8 lead bytes
    → without valid continuation bytes → U+FFFD (EF BF BD) written into file
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FFFD = '\ufffd'

def fix_content(c):
    # ==========================================================================
    # SECTION 1: Fix emoji ?? patterns (literal question marks, context-anchored)
    # Each '?' = one Unicode codepoint that couldn't encode in CP1252
    # ==========================================================================

    # --- NAV SIDEBAR ICONS ---
    # Each nav button: <span class="text-base">??</span> before <span class="text-[...]">LABEL</span>
    c = c.replace('<span class="text-base">??</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-blue-400 uppercase tracking-widest">Treinadores</span>',
                  '<span class="text-base">\U0001f3cb\ufe0f</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-blue-400 uppercase tracking-widest">Treinadores</span>')
    c = c.replace('<span class="text-base">??</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-purple-400 uppercase tracking-widest">Rainbow Orbs</span>',
                  '<span class="text-base">\U0001f308\ufe0f</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-purple-400 uppercase tracking-widest">Rainbow Orbs</span>')
    c = c.replace('<span class="text-base">??</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-amber-400 uppercase tracking-widest">Ranking</span>',
                  '<span class="text-base">\U0001f3c6\ufe0f</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-amber-400 uppercase tracking-widest">Ranking</span>')
    c = c.replace('<span class="text-base">??</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-emerald-400 uppercase tracking-widest">Guias F2P (Lv 500+)</span>',
                  '<span class="text-base">\U0001f4d6\ufe0f</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-emerald-400 uppercase tracking-widest">Guias F2P (Lv 500+)</span>')
    # Pokelog - Pok has FFFD for é so anchor on group-hover color
    c = c.replace('<span class="text-base">??</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-cyan-400 uppercase tracking-widest">',
                  '<span class="text-base">\U0001f4e1\ufe0f</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-cyan-400 uppercase tracking-widest">')
    c = c.replace('<span class="text-base">??</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-pink-400 uppercase tracking-widest">Sobre o Projeto</span>',
                  '<span class="text-base">\u2139\ufe0f</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                            <span class="text-[10px] font-black text-slate-300 group-hover:text-pink-400 uppercase tracking-widest">Sobre o Projeto</span>')
    c = c.replace('<span class="text-base">???</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                                <span class="text-[10px] font-black text-slate-300 group-hover:text-rose-400 uppercase tracking-widest">Painel Admin</span>',
                  '<span class="text-base">\u2699\ufe0f\U0001f512</span>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n                                <span class="text-[10px] font-black text-slate-300 group-hover:text-rose-400 uppercase tracking-widest">Painel Admin</span>')

    # --- ANNOUNCEMENT STRIP ---
    c = c.replace('?? An\ufffdn\ufffdcio Ativo', '\U0001f4e2\ufe0f Anún\ufffdcio Ativo')
    # After FFFD fix below, Anúncio will be fully fixed. Use pre-FFFD anchor:
    c = c.replace('?? An\ufffdncio Ativo', '\U0001f4e2\ufe0f Anúncio Ativo')

    # --- F2P GUIDE BULLET ICONS (colored diamond bullets) ---
    c = c.replace('<span class="text-blue-500 mt-0.5">??</span>', '<span class="text-blue-500 mt-0.5">\u25c6\ufe0f</span>')
    c = c.replace('<span class="text-emerald-500 mt-0.5">??</span>', '<span class="text-emerald-500 mt-0.5">\u25c6\ufe0f</span>')
    c = c.replace('<span class="text-purple-500 mt-0.5">??</span>', '<span class="text-purple-500 mt-0.5">\u25c6\ufe0f</span>')
    c = c.replace('<span class="text-amber-500 mt-0.5">??</span>', '<span class="text-amber-500 mt-0.5">\u25c6\ufe0f</span>')
    c = c.replace('<span class="text-pink-400 mt-0.5">??</span>', '<span class="text-pink-400 mt-0.5">\u25c6\ufe0f</span>')
    c = c.replace('<span class="text-orange-500 mt-0.5">??</span>', '<span class="text-orange-500 mt-0.5">\u25c6\ufe0f</span>')

    # --- ADMIN TAB BUTTONS ---
    c = c.replace("console.log('?? Feedbacks clicked'", "console.log('\U0001f4ac\ufe0f Feedbacks clicked'")
    c = c.replace("console.log('?? Announcements clicked'", "console.log('\U0001f4e2\ufe0f Announcements clicked'")
    c = c.replace("console.log('?? Content clicked'", "console.log('\U0001f4dd\ufe0f Content clicked'")
    c = c.replace('?? Feedbacks', '\U0001f4ac\ufe0f Feedbacks')
    c = c.replace('?? Estat\ufffdst\ufffdcas', '\U0001f4ca\ufe0f Estat\ufffdst\ufffdcas')  # fallback
    c = c.replace('?? Estat\ufffdsticas', '\U0001f4ca\ufe0f Estat\ufffdsticas')
    c = c.replace('?? An\ufffdncios', '\U0001f4e2\ufe0f An\ufffdncios')
    c = c.replace('?? Usu\ufffdr\ufffdos', '\U0001f465\ufe0f Usu\ufffdr\ufffdos')  # fallback
    c = c.replace('?? Usu\ufffdrios', '\U0001f465\ufe0f Usu\ufffdrios')
    c = c.replace('?? Conte\ufffdd\ufffd', '\U0001f4dd\ufe0f Conte\ufffdd\ufffd')   # fallback
    c = c.replace('?? Conte\ufffddo', '\U0001f4dd\ufe0f Conte\ufffddo')
    c = c.replace('?? Configura\uFFFD\uFFFDes', '\u2699\ufe0f Configura\uFFFD\uFFFDes')

    # --- ADMIN STATS PANEL ---
    c = c.replace('?? Usu\ufffdrios</p>', '\U0001f465\ufe0f Usu\ufffdrios</p>')
    c = c.replace("'?? Usu\ufffdriosl", "'\U0001f465\ufe0f Usu\ufffdriosl")
    c = c.replace('?? Usu\ufffdrios\n', '\U0001f465\ufe0f Usu\ufffdrios\n')
    c = c.replace('<p class="text-[10px] text-slate-400 uppercase font-black">?? Usu\ufffdrios</p>',
                  '<p class="text-[10px] text-slate-400 uppercase font-black">\U0001f465\ufe0f Usu\ufffdrios</p>')
    c = c.replace('<p class="text-[10px] text-slate-400 uppercase font-black">Usu\ufffdrios</p>',
                  '<p class="text-[10px] text-slate-400 uppercase font-black">Usu\ufffdrios</p>')

    # Top Clans label in admin stats
    c = c.replace('Top ?? Cl\ufffds</p>', 'Top \U0001f3f0\ufe0f Cl\ufffds</p>')
    c = c.replace("'Sem ?? Cl\ufffd'", "'Sem Cl\ufffd'")

    # --- BOSS ALERT HTML ---
    c = c.replace('class="pokeball-alert-icon text-center">????</div>',
                  'class="pokeball-alert-icon text-center">\u26a1\ufe0f\u26a1\ufe0f</div>')
    c = c.replace('class="boss-alert-title">?? BOSS SELVAGEM!</h2>',
                  'class="boss-alert-title">\u26a0\ufe0f BOSS SELVAGEM!</h2>')
    c = c.replace('style="font-size: 2em;">??</span>',
                  'style="font-size: 2em;">\u26a0\ufe0f</span>')
    # Single ? before boss-threat
    c = c.replace('<div>? <span id="boss-threat">',
                  '<div>\u26a0 <span id="boss-threat">')
    # Single ? for TIPO
    c = c.replace('<div style="margin-top: 8px;">? TIPO:',
                  '<div style="margin-top: 8px;">\U0001f3af TIPO:')
    # Single ? for combat countdown
    c = c.replace('? O COMBATE INICIA EM SEGUNDOS!',
                  '\u23f0 O COMBATE INICIA EM SEGUNDOS!')
    # ???? PREPARE-SE SEMPRE!
    c = c.replace('???? PREPARE-SE SEMPRE!',
                  '\u2694\ufe0f\u2694\ufe0f PREPARE-SE SEMPRE!')
    # Button: ? ENTENDI ? PREPARADO
    c = c.replace('? ENTENDI ? PREPARADO',
                  '\u2705 ENTENDI \u2694\ufe0f PREPARADO')

    # --- FORM LABELS ---
    c = c.replace('?? N\ufffddvel de Pesca', '\U0001f3a3\ufe0f N\ufffddvel de Pesca')
    c = c.replace('?? Pok\ufffddmon Capturados', '\U0001f3af\ufe0f Pok\ufffddmon Capturados')
    c = c.replace('?? Pok\ufffdmon Capturados', '\U0001f3af\ufe0f Pok\ufffdmon Capturados')

    # --- FOOTER BUTTONS ---
    c = c.replace('??</span> Sugest', '\U0001f4ac\ufe0f</span> Sugest')
    c = c.replace('??</span> Apoiar Cri', '\U0001f49a\ufe0f</span> Apoiar Cri')
    c = c.replace('??</span> Hist', '\U0001f4dc\ufe0f</span> Hist')

    # --- WORLD COLORS JS OBJECT ---
    c = c.replace("'Gold': { text: 'text-yellow-500', icon: ' ? ' }",
                  "'Gold': { text: 'text-yellow-500', icon: ' \u2b50 ' }")
    c = c.replace("'Aurora': { text: 'text-green-400', icon: '??' }",
                  "'Aurora': { text: 'text-green-400', icon: '\U0001f33f\ufe0f' }")
    c = c.replace("'Omega': { text: 'text-red-600', icon: '??' }",
                  "'Omega': { text: 'text-red-600', icon: '\u267e\ufe0f' }")
    c = c.replace("'Emerald': { text: 'text-emerald-400', icon: '??' }",
                  "'Emerald': { text: 'text-emerald-400', icon: '\U0001f48e\ufe0f' }")
    c = c.replace("'Cosmic': { text: 'text-purple-500', icon: '?' }",
                  "'Cosmic': { text: 'text-purple-500', icon: '\U0001f52e' }")
    c = c.replace("'Steel': { text: 'text-slate-400', icon: '??' }",
                  "'Steel': { text: 'text-slate-400', icon: '\u2699\ufe0f' }")
    c = c.replace("'Wind': { text: 'text-cyan-400', icon: '??' }",
                  "'Wind': { text: 'text-cyan-400', icon: '\U0001f32c\ufe0f' }")
    c = c.replace("'Lunar': { text: 'text-indigo-300', icon: '??' }",
                  "'Lunar': { text: 'text-indigo-300', icon: '\U0001f319\ufe0f' }")
    c = c.replace("'Ocean': { text: 'text-blue-500', icon: '??' }",
                  "'Ocean': { text: 'text-blue-500', icon: '\U0001f30a\ufe0f' }")
    c = c.replace("'Obsidian': { text: 'text-slate-700', icon: ' ? ' }",
                  "'Obsidian': { text: 'text-slate-700', icon: ' \u26ab ' }")
    c = c.replace("'Flame': { text: 'text-orange-500', icon: '??' }",
                  "'Flame': { text: 'text-orange-500', icon: '\U0001f525\ufe0f' }")
    c = c.replace("'Rainbow': { text: 'text-pink-400', icon: '??' }",
                  "'Rainbow': { text: 'text-pink-400', icon: '\U0001f308\ufe0f' }")
    c = c.replace("'Soul': { text: 'text-violet-500', icon: ' ? ' }",
                  "'Soul': { text: 'text-violet-500', icon: ' \U0001f49c ' }")
    c = c.replace("return colors[world] || { text: 'text-slate-400', icon: ' ? ' }",
                  "return colors[world] || { text: 'text-slate-400', icon: ' \u2b50 ' }")

    # --- CLAN DATA JS OBJECT ---
    c = c.replace("volcanic: { name: \"Volcanic\", color: \"bg-red-600\", icon: \"??\",",
                  "volcanic: { name: \"Volcanic\", color: \"bg-red-600\", icon: \"\U0001f30b\ufe0f\",")
    c = c.replace("seavell: { name: \"Seavell\", color: \"bg-blue-600\", icon: \"??\",",
                  "seavell: { name: \"Seavell\", color: \"bg-blue-600\", icon: \"\U0001f30a\ufe0f\",")
    c = c.replace("orebound: { name: \"Orebound\", color: \"bg-amber-800\", icon: \"??\",",
                  "orebound: { name: \"Orebound\", color: \"bg-amber-800\", icon: \"\u26cf\ufe0f\",")
    c = c.replace("wingeon: { name: \"Wingeon\", color: \"bg-sky-400\", icon: \"???\",",
                  "wingeon: { name: \"Wingeon\", color: \"bg-sky-400\", icon: \"\U0001f32a\ufe0f\",")
    c = c.replace("naturia: { name: \"Naturia\", color: \"bg-green-600\", icon: \"??\",",
                  "naturia: { name: \"Naturia\", color: \"bg-green-600\", icon: \"\U0001f33f\ufe0f\",")
    c = c.replace("malefic: { name: \"Malefic\", color: \"bg-purple-700\", icon: \"??\",",
                  "malefic: { name: \"Malefic\", color: \"bg-purple-700\", icon: \"\u2620\ufe0f\",")
    c = c.replace("raibolt: { name: \"Raibolt\", color: \"bg-yellow-500\", icon: \"?\",",
                  "raibolt: { name: \"Raibolt\", color: \"bg-yellow-500\", icon: \"\u26a1\",")
    c = c.replace("psycraft: { name: \"Psycraft\", color: \"bg-pink-500\", icon: \"??\",",
                  "psycraft: { name: \"Psycraft\", color: \"bg-pink-500\", icon: \"\U0001f52e\ufe0f\",")
    c = c.replace("ironhard: { name: \"Ironhard\", color: \"bg-slate-500\", icon: \"??\",",
                  "ironhard: { name: \"Ironhard\", color: \"bg-slate-500\", icon: \"\u2699\ufe0f\",")

    # --- BOSS DATA JS OBJECT ---
    c = c.replace("'Sunflora': { key: 'boss12', storageKey: 'boss12', emoji: '??', icon: '??', danger: '? Cr\ufffdt\ufffdco'",
                  "'Sunflora': { key: 'boss12', storageKey: 'boss12', emoji: '\u2600\ufe0f', icon: '\u2600\ufe0f', danger: '\u26a0 Cr\ufffdt\ufffdco'")
    c = c.replace("'Sunflora': { key: 'boss12', storageKey: 'boss12', emoji: '??', icon: '??', danger: '? Cr\ufffdtico'",
                  "'Sunflora': { key: 'boss12', storageKey: 'boss12', emoji: '\u2600\ufe0f', icon: '\u2600\ufe0f', danger: '\u26a0 Cr\ufffdtico'")
    c = c.replace("'Magcargo': { key: 'boss16', storageKey: 'boss16', emoji: '??', icon: '??', danger: '? Cr\ufffdtico'",
                  "'Magcargo': { key: 'boss16', storageKey: 'boss16', emoji: '\u2668\ufe0f', icon: '\u2668\ufe0f', danger: '\u26a0 Cr\ufffdtico'")
    c = c.replace("'Tyranitar': { key: 'boss20', storageKey: 'boss20', emoji: '??', icon: '??', danger: '?? EXTREMO'",
                  "'Tyranitar': { key: 'boss20', storageKey: 'boss20', emoji: '\u2620\ufe0f', icon: '\u2620\ufe0f', danger: '\u26a0\ufe0f EXTREMO'")
    c = c.replace("'Dragonair': { key: 'boss12', storageKey: 'boss12', emoji: '??', icon: '??', danger: '? ALTO'",
                  "'Dragonair': { key: 'boss12', storageKey: 'boss12', emoji: '\u26a1\ufe0f', icon: '\u26a1\ufe0f', danger: '\u26a0 ALTO'")
    c = c.replace("'Mamoswine': { key: 'boss23', storageKey: 'boss23', emoji: '??', icon: '??\ufffd', danger: '? Cr\ufffdtico'",
                  "'Mamoswine': { key: 'boss23', storageKey: 'boss23', emoji: '\u2744\ufe0f', icon: '\u2744\ufe0f\xb0', danger: '\u26a0 Cr\ufffdtico'")
    # Handle degree sign that might already be U+00B0 vs FFFD
    c = c.replace("'Mamoswine': { key: 'boss23', storageKey: 'boss23', emoji: '??', icon: '??°', danger: '? Cr\ufffdtico'",
                  "'Mamoswine': { key: 'boss23', storageKey: 'boss23', emoji: '\u2744\ufe0f', icon: '\u2744\ufe0f°', danger: '\u26a0 Cr\ufffdtico'")

    # --- EPIC BOSS MESSAGES ---
    c = c.replace("'Sunflora': { emoji: \"??\", icon: \"??\", msg: \"SUNFLORA SELVAGEM APARECEU\",",
                  "'Sunflora': { emoji: \"\u2600\ufe0f\", icon: \"\u2600\ufe0f\", msg: \"SUNFLORA SELVAGEM APARECEU\",")
    c = c.replace("'Magcargo': { emoji: \"??\", icon: \"??\", msg: \"MAGCARGO INCANDESCENTE\",",
                  "'Magcargo': { emoji: \"\u2668\ufe0f\", icon: \"\u2668\ufe0f\", msg: \"MAGCARGO INCANDESCENTE\",")
    c = c.replace("'Tyranitar': { emoji: \"??\", icon: \"??\", msg: \"TYRANITAR COLOSSAL\",",
                  "'Tyranitar': { emoji: \"\u2620\ufe0f\", icon: \"\u2620\ufe0f\", msg: \"TYRANITAR COLOSSAL\",")
    c = c.replace("'Dragonair': { emoji: \"??\", icon: \"??\", msg: \"DRAGONAIR APARECEU\",",
                  "'Dragonair': { emoji: \"\u26a1\ufe0f\", icon: \"\u26a1\ufe0f\", msg: \"DRAGONAIR APARECEU\",")
    c = c.replace("'Mamoswine': { emoji: \"??\ufffd\", icon: \"??\ufffd\", msg: \"MAMOSWINE CONGELANDO!\",",
                  "'Mamoswine': { emoji: \"\u2744\ufe0f\xb0\", icon: \"\u2744\ufe0f\xb0\", msg: \"MAMOSWINE CONGELANDO!\",")
    c = c.replace("'Mamoswine': { emoji: \"??°\", icon: \"??°\", msg: \"MAMOSWINE CONGELANDO!\",",
                  "'Mamoswine': { emoji: \"\u2744\ufe0f°\", icon: \"\u2744\ufe0f°\", msg: \"MAMOSWINE CONGELANDO!\",")
    # Default epic msg
    c = c.replace("emoji: \"??\", type: \"COMBATE\",", "emoji: \"\U0001f3ae\ufe0f\", type: \"COMBATE\",")

    # --- EPIC NOTIFICATIONS ---
    c = c.replace("'Sunflora': { title: \"?? SUNFLORA SELVAGEM APARECEU! ??\", emoji: \"??\", type: \"SOLAR\", threat: \"? Cr\ufffdtico\" }",
                  "'Sunflora': { title: \"\u2600\ufe0f SUNFLORA SELVAGEM APARECEU! \u2600\ufe0f\", emoji: \"\u2600\ufe0f\", type: \"SOLAR\", threat: \"\u26a0 Crítico\" }")
    c = c.replace("'Magcargo': { title: \"?? MAGCARGO INCANDESCENTE! ??\", emoji: \"??\", type: \"FOGO\", threat: \"? Cr\ufffdtico\" }",
                  "'Magcargo': { title: \"\u2668\ufe0f MAGCARGO INCANDESCENTE! \u2668\ufe0f\", emoji: \"\u2668\ufe0f\", type: \"FOGO\", threat: \"\u26a0 Crítico\" }")
    c = c.replace("'Tyranitar': { title: \"?? TYRANITAR COLOSSAL! ??\", emoji: \"??\", type: \"ROCHA\", threat: \"?? EXTREMO\" }",
                  "'Tyranitar': { title: \"\u2620\ufe0f TYRANITAR COLOSSAL! \u2620\ufe0f\", emoji: \"\u2620\ufe0f\", type: \"ROCHA\", threat: \"\u26a0\ufe0f EXTREMO\" }")
    c = c.replace("'Dragonair': { title: \"?? DRAGONAIR APARECEU! ??\", emoji: \"??\", type: \"DRAG\ufffdo\", threat: \"? ALTO\" }",
                  "'Dragonair': { title: \"\u26a1\ufe0f DRAGONAIR APARECEU! \u26a1\ufe0f\", emoji: \"\u26a1\ufe0f\", type: \"DRAGÃO\", threat: \"\u26a0 ALTO\" }")
    c = c.replace("'Dragonair': { title: \"?? DRAGONAIR APARECEU! ??\", emoji: \"??\", type: \"DRAG\uFFFDO\", threat: \"? ALTO\" }",
                  "'Dragonair': { title: \"\u26a1\ufe0f DRAGONAIR APARECEU! \u26a1\ufe0f\", emoji: \"\u26a1\ufe0f\", type: \"DRAGÃO\", threat: \"\u26a0 ALTO\" }")
    c = c.replace("'Mamoswine': { title: \"??\ufffd MAMOSWINE GELADO! ??\ufffd\", emoji: \"??\ufffd\", type: \"GELO\", threat: \"? Cr\ufffdtico\" }",
                  "'Mamoswine': { title: \"\u2744\ufe0f° MAMOSWINE GELADO! \u2744\ufe0f°\", emoji: \"\u2744\ufe0f°\", type: \"GELO\", threat: \"\u26a0 Crítico\" }")
    c = c.replace("'Mamoswine': { title: \"??° MAMOSWINE GELADO! ??°\", emoji: \"??°\", type: \"GELO\", threat: \"? Cr\ufffdtico\" }",
                  "'Mamoswine': { title: \"\u2744\ufe0f° MAMOSWINE GELADO! \u2744\ufe0f°\", emoji: \"\u2744\ufe0f°\", type: \"GELO\", threat: \"\u26a0 Crítico\" }")
    c = c.replace("'Pok\ufffddpark': { title: \"?? POK\ufffddPARK COME\ufffddANDO AGORA! ??\", emoji: \"??\", type: \"EVENTO\", threat: \"? ALTO\" }",
                  "'Poképark': { title: \"\U0001f3aa\ufe0f POKÉPARK COMEÇANDO AGORA! \U0001f3aa\ufe0f\", emoji: \"\U0001f3aa\ufe0f\", type: \"EVENTO\", threat: \"\u26a0 ALTO\" }")
    c = c.replace("'Pok\ufffdpark': { title: \"?? POK\ufffdPARK COME\ufffdANDO AGORA! ??\", emoji: \"??\", type: \"EVENTO\", threat: \"? ALTO\" }",
                  "'Poképark': { title: \"\U0001f3aa\ufe0f POKÉPARK COMEÇANDO AGORA! \U0001f3aa\ufe0f\", emoji: \"\U0001f3aa\ufe0f\", type: \"EVENTO\", threat: \"\u26a0 ALTO\" }")
    # Default notification
    c = c.replace('emoji: "??", type: "COMBATE", threat: "? Cr\ufffdtico"',
                  'emoji: "\U0001f3ae\ufe0f", type: "COMBATE", threat: "\u26a0 Crítico"')

    # --- NOTIFICATION BODY STRING ---
    c = c.replace('??????????????????\n? TIPO:', '\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\n\u26a1 TIPO:')
    c = c.replace('??????????????????\\n? TIPO:', '\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\u26a1\ufe0f\\n\u26a1 TIPO:')
    c = c.replace('\\n?? N\ufffddvel:', '\\n\u26a1\ufe0f N\ufffddvel:')
    c = c.replace('\\n?? N\ufffdvel:', '\\n\u26a1\ufe0f N\ufffdvel:')
    c = c.replace('`?? ALERTA Cr\ufffdtico DE COMBATE! ??`',
                  '`\U0001f3ae\ufe0f ALERTA CRÍTICO DE COMBATE! \U0001f3ae\ufe0f`')

    # --- EPIC BOSS DATA (bossData for in-combat display, separate from cycle data) ---
    c = c.replace("'Sunflora': { emoji: \"??\", title: \"SUNFLORA SELVAGEM APARECEU\", type: \"SOLAR\",",
                  "'Sunflora': { emoji: \"\u2600\ufe0f\", title: \"SUNFLORA SELVAGEM APARECEU\", type: \"SOLAR\",")
    c = c.replace("'Magcargo': { emoji: \"??\", title: \"MAGCARGO INCANDESCENTE\", type: \"FOGO\",",
                  "'Magcargo': { emoji: \"\u2668\ufe0f\", title: \"MAGCARGO INCANDESCENTE\", type: \"FOGO\",")
    c = c.replace("'Tyranitar': { emoji: \"??\", title: \"TYRANITAR COLOSSAL\", type: \"ROCHA\",",
                  "'Tyranitar': { emoji: \"\u2620\ufe0f\", title: \"TYRANITAR COLOSSAL\", type: \"ROCHA\",")
    c = c.replace("'Dragonair': { emoji: \"??\", title: \"DRAGONAIR APARECEU\", type: \"DRAG\ufffdo\",",
                  "'Dragonair': { emoji: \"\u26a1\ufe0f\", title: \"DRAGONAIR APARECEU\", type: \"DRAGÃO\",")
    c = c.replace("'Dragonair': { emoji: \"??\", title: \"DRAGONAIR APARECEU\", type: \"DRAG\uFFFDO\",",
                  "'Dragonair': { emoji: \"\u26a1\ufe0f\", title: \"DRAGONAIR APARECEU\", type: \"DRAGÃO\",")
    c = c.replace("'Mamoswine': { emoji: \"??\ufffd\", title: \"MAMOSWINE GELADO\",",
                  "'Mamoswine': { emoji: \"\u2744\ufe0f°\", title: \"MAMOSWINE GELADO\",")
    c = c.replace("'Mamoswine': { emoji: \"??°\", title: \"MAMOSWINE GELADO\",",
                  "'Mamoswine': { emoji: \"\u2744\ufe0f°\", title: \"MAMOSWINE GELADO\",")
    c = c.replace("'Pok\ufffddpark': { emoji: \"??\", title: \"POK\ufffddPARK COME\ufffddANDO AGORA\",",
                  "'Poképark': { emoji: \"\U0001f3aa\ufe0f\", title: \"POKÉPARK COMEÇANDO AGORA\",")
    c = c.replace("'Pok\ufffdpark': { emoji: \"??\", title: \"POK\ufffdPARK COME\ufffdANDO AGORA\",",
                  "'Poképark': { emoji: \"\U0001f3aa\ufe0f\", title: \"POKÉPARK COMEÇANDO AGORA\",")
    # Default threat for display
    c = c.replace('threat: "? Cr\ufffdtico"', 'threat: "\u26a0 Crítico"')
    c = c.replace("threat: '? Cr\ufffdtico'", "threat: '\u26a0 Crítico'")

    # Admin new announcement header
    c = c.replace('?? Novo An\ufffdncio', '\U0001f4e2\ufe0f Novo An\ufffdncio')
    # Admin content manager
    c = c.replace('?? Gerenciar Conte\ufffddo', '\U0001f4dd\ufe0f Gerenciar Conte\ufffddo')
    c = c.replace('?? Bosses Dispon\ufffddveis', '\U0001f3ae\ufe0f Bosses Dispon\ufffddveis')
    c = c.replace('?? Bosses Dispon\ufffdveis', '\U0001f3ae\ufe0f Bosses Dispon\ufffdveis')
    # Admin settings header
    c = c.replace('?? Configura\uFFFD\uFFFDes do Sistema', '\u2699\ufe0f Configurações do Sistema')
    # Admin settings toggles
    c = c.replace('?? Modo Manuten\uFFFD\uFFFDo', '\U0001f6e0\ufe0f Modo Manuten\uFFFD\uFFFDo')
    c = c.replace('? Desabilitar Feedback de Usu\ufffdr\ufffdos', '\U0001f6ab Desabilitar Feedback de Usu\ufffdr\ufffdos')
    c = c.replace('? Desabilitar Feedback de Usu\ufffdrios', '\U0001f6ab Desabilitar Feedback de Usu\ufffdrios')

    # User logged in console log
    c = c.replace("console.log('?? Usu\ufffdr\ufffdlo logado:'", "console.log('\U0001f464 Usu\ufffdr\ufffdio logado:'")
    c = c.replace("console.log('?? Usu\ufffdrio logado:'", "console.log('\U0001f464 Usu\ufffdrio logado:'")

    # Version available notification
    c = c.replace('Nova Vers\ufffdo Dispon\ufffddvel! ?', 'Nova Vers\ufffdo Dispon\ufffddvel! \u2728')
    c = c.replace('Nova Vers\ufffdvel Dispon\ufffddvel! ?', 'Nova Vers\ufffdvel Dispon\ufffddvel! \u2728')

    # Copyright symbol
    c = c.replace('? 2026 PXG Check Project', '\xa9 2026 PXG Check Project')

    # Poképark event key in JS
    c = c.replace("name: 'Pok\ufffddpark'", "name: 'Poképark'")
    c = c.replace("name: 'Pok\ufffdpark'", "name: 'Poképark'")
    c = c.replace("displayName: 'Pok\ufffddpark'", "displayName: 'Poképark'")
    c = c.replace("displayName: 'Pok\ufffdpark'", "displayName: 'Poképark'")

    # General single ? threat for ALTO (used in multiple places)
    c = c.replace('"? ALTO"', '"\u26a0 ALTO"')
    c = c.replace("'? ALTO'", "'\u26a0 ALTO'")
    c = c.replace('"?? EXTREMO"', '"\u26a0\ufe0f EXTREMO"')
    c = c.replace("'?? EXTREMO'", "'\u26a0\ufe0f EXTREMO'")

    # Comments with ?? (CSS/JS)
    c = c.replace('/* ? ANIMA', '/* \u2728 ANIMA')
    c = c.replace('/* ? EPIC', '/* \u2728 EPIC')

    # ==========================================================================
    # SECTION 2: Fix U+FFFD (accented character recovery)
    # Order: longer/more specific patterns FIRST to avoid partial matches
    # ==========================================================================

    # ----- 2-FFFD patterns (duas letras corrompidas em sequência) -----
    
    # ão patterns (ã+o → FFFD + o is just 1 FFFD; ção → 2 FFFD + o)
    c = c.replace('Anima\uFFFD\uFFFDo', 'Animação')
    c = c.replace('anima\uFFFD\uFFFDo', 'animação')
    c = c.replace('Pulsa\uFFFD\uFFFDo', 'Pulsação')
    c = c.replace('pulsa\uFFFD\uFFFDo', 'pulsação')
    c = c.replace('Notifica\uFFFD\uFFFDo', 'Notificação')
    c = c.replace('notifica\uFFFD\uFFFDo', 'notificação')
    c = c.replace('Atualiza\uFFFD\uFFFDo', 'Atualização')
    c = c.replace('atualiza\uFFFD\uFFFDo', 'atualização')
    c = c.replace('Automatiza\uFFFD\uFFFDo', 'Automatização')
    c = c.replace('automatiza\uFFFD\uFFFDo', 'automatização')
    c = c.replace('Estimula\uFFFD\uFFFDo', 'Estimulação')
    c = c.replace('estimula\uFFFD\uFFFDo', 'estimulação')
    c = c.replace('Configura\uFFFD\uFFFDo', 'Configuração')
    c = c.replace('configura\uFFFD\uFFFDo', 'configuração')
    c = c.replace('Configura\uFFFD\uFFFDes', 'Configurações')
    c = c.replace('configura\uFFFD\uFFFDes', 'configurações')
    c = c.replace('Aplica\uFFFD\uFFFDo', 'Aplicação')
    c = c.replace('aplica\uFFFD\uFFFDo', 'aplicação')
    c = c.replace('Composi\uFFFD\uFFFDo', 'Composição')
    c = c.replace('composi\uFFFD\uFFFDo', 'composição')
    c = c.replace('Conex\uFFFD\uFFFDo', 'Conexão')
    c = c.replace('conex\uFFFD\uFFFDo', 'conexão')
    c = c.replace('Gest\uFFFD\uFFFDo', 'Gestão')  # less common than single FFFD
    c = c.replace('gest\uFFFD\uFFFDo', 'gestão')
    c = c.replace('Defini\uFFFD\uFFFDo', 'Definição')
    c = c.replace('Unifica\uFFFD\uFFFDo', 'Unificação')
    c = c.replace('unifica\uFFFD\uFFFDo', 'unificação')
    c = c.replace('Informa\uFFFD\uFFFDes', 'Informações')
    c = c.replace('informa\uFFFD\uFFFDes', 'informações')
    c = c.replace('Observa\uFFFD\uFFFDo', 'Observação')
    c = c.replace('observa\uFFFD\uFFFDo', 'observação')
    c = c.replace('Observa\uFFFD\uFFFDes', 'Observações')
    c = c.replace('observa\uFFFD\uFFFDes', 'observações')
    c = c.replace('Reformata\uFFFD\uFFFDo', 'Reformatação')
    c = c.replace('formata\uFFFD\uFFFDo', 'formatação')
    c = c.replace('Formata\uFFFD\uFFFDo', 'Formatação')
    c = c.replace('Marca\uFFFD\uFFFDes', 'Marcações')
    c = c.replace('marca\uFFFD\uFFFDes', 'marcações')
    c = c.replace('Marca\uFFFD\uFFFDo', 'Marcação')
    c = c.replace('Coloca\uFFFD\uFFFDo', 'Colocação')
    c = c.replace('Descri\uFFFD\uFFFDo', 'Descrição')
    c = c.replace('descri\uFFFD\uFFFDo', 'descrição')
    c = c.replace('Cria\uFFFD\uFFFDo', 'Criação')
    c = c.replace('cria\uFFFD\uFFFDo', 'criação')
    c = c.replace('Migra\uFFFD\uFFFDo', 'Migração')
    c = c.replace('migra\uFFFD\uFFFDo', 'migração')
    c = c.replace('Fun\uFFFD\uFFFDo', 'Função')
    c = c.replace('fun\uFFFD\uFFFDo', 'função')
    c = c.replace('Remo\uFFFD\uFFFDo', 'Remoção')
    c = c.replace('remo\uFFFD\uFFFDo', 'remoção')
    c = c.replace('valida\uFFFD\uFFFDo', 'validação')
    c = c.replace('Valida\uFFFD\uFFFDo', 'Validação')
    c = c.replace('liga\uFFFD\uFFFDo', 'ligação')
    c = c.replace('Liga\uFFFD\uFFFDo', 'Ligação')
    c = c.replace('opera\uFFFD\uFFFDo', 'operação')
    c = c.replace('Opera\uFFFD\uFFFDo', 'Operação')
    c = c.replace('Separa\uFFFD\uFFFDo', 'Separação')
    c = c.replace('Aten\uFFFD\uFFFDo', 'Atenção')
    c = c.replace('aten\uFFFD\uFFFDo', 'atenção')
    c = c.replace('Cita\uFFFD\uFFFDo', 'Citação')
    c = c.replace('coment\uFFFD\uFFFDo', 'comentário')  # no FFFD for this? Actually ário = á+r+i+o
    c = c.replace('sincroniza\uFFFD\uFFFDo', 'sincronização')
    c = c.replace('Sincroniza\uFFFD\uFFFDo', 'Sincronização')
    c = c.replace('Verifica\uFFFD\uFFFDo', 'Verificação')
    c = c.replace('verifica\uFFFD\uFFFDo', 'verificação')

    # Plural -ões endings (ç+õ = FFFD+FFFD + es? or different)
    # Actually -ções: ç=FFFD, ã=FFFD, o, e, s → ção=\uFFFD\uFFFDo
    c = c.replace('Anima\uFFFD\uFFFDes', 'Animações')
    c = c.replace('anima\uFFFD\uFFFDes', 'animações')
    c = c.replace('ANIMA\uFFFD\uFFFDES', 'ANIMAÇÕES')
    c = c.replace('Pulsa\uFFFD\uFFFDes', 'Pulsações')
    c = c.replace('pulsa\uFFFD\uFFFDes', 'pulsações')
    c = c.replace('agita\uFFFD\uFFFDes', 'agitações')
    c = c.replace('notifica\uFFFD\uFFFDes', 'notificações')
    c = c.replace('Notifica\uFFFD\uFFFDes', 'Notificações')
    c = c.replace('vibra\uFFFD\uFFFDes', 'vibrações')
    c = c.replace('Vibra\uFFFD\uFFFDes', 'Vibrações')

    # ----- Single FFFD patterns -----

    # É, É (uppercase at start of word)
    c = c.replace('\uFFFDPICAS', 'ÉPICAS')
    c = c.replace('\uFFFDPICO', 'ÉPICO')
    c = c.replace('\uFFFDpica', 'épica')
    c = c.replace('\uFFFDpico', 'épico')
    c = c.replace('\uFFFDpicas', 'épicas')
    c = c.replace('\uFFFDpicos', 'épicos')
    c = c.replace('TEM\uFFFDTICA', 'TEMÁTICA')
    c = c.replace('Tem\uFFFDtica', 'Temática')
    c = c.replace('tem\uFFFDtica', 'temática')
    c = c.replace('TEM\uFFFDTICAS', 'TEMÁTICAS')
    c = c.replace('tem\uFFFDticas', 'temáticas')
    c = c.replace('Tem\uFFFDticas', 'Temáticas')

    # Pokémon-related
    c = c.replace('Pok\uFFFDmon', 'Pokémon')
    c = c.replace('POK\uFFFDMON', 'POKÉMON')
    c = c.replace('Pok\uFFFDbola', 'Pokébola')
    c = c.replace('Pok\uFFFDBOLA', 'POKÉBOLA')
    c = c.replace('Pok\uFFFDball', 'Pokéball')
    c = c.replace('Pok\uFFFDpark', 'Poképark')
    c = c.replace('POK\uFFFDPARK', 'POKÉPARK')
    c = c.replace('Pok\uFFFDlog', 'Pokélog')
    c = c.replace('POK\uFFFDLOG', 'POKÉLOG')

    # VISÃO / visão
    c = c.replace('VIS\uFFFDO', 'VISÃO')
    c = c.replace('vis\uFFFDo', 'visão')
    c = c.replace('Vis\uFFFDo', 'Visão')

    # DRAGÃO / dragão
    c = c.replace('DRAG\uFFFDO', 'DRAGÃO')
    c = c.replace('Drag\uFFFDo', 'Dragão')
    c = c.replace('drag\uFFFDo', 'dragão')

    # COMEÇANDO etc.
    c = c.replace('COME\uFFFDANDO', 'COMEÇANDO')
    c = c.replace('Come\uFFFDando', 'Começando')
    c = c.replace('come\uFFFDando', 'começando')

    # Gestão (single FFFD for ã)
    c = c.replace('Gest\uFFFDo', 'Gestão')
    c = c.replace('gest\uFFFDo', 'gestão')

    # Crítico / crítico
    c = c.replace('Cr\uFFFDtico', 'Crítico')
    c = c.replace('cr\uFFFDtico', 'crítico')
    c = c.replace('CR\uFFFDTICO', 'CRÍTICO')

    # Anúncio / anúncio
    c = c.replace('An\uFFFDncio', 'Anúncio')
    c = c.replace('an\uFFFDncio', 'anúncio')
    c = c.replace('An\uFFFDncios', 'Anúncios')
    c = c.replace('an\uFFFDncios', 'anúncios')

    # Diárias / diárias
    c = c.replace('Di\uFFFDrias', 'Diárias')
    c = c.replace('di\uFFFDrias', 'diárias')

    # -ário/-ária endings
    c = c.replace('Usu\uFFFDrio', 'Usuário')
    c = c.replace('usu\uFFFDrio', 'usuário')
    c = c.replace('Usu\uFFFDrios', 'Usuários')
    c = c.replace('usu\uFFFDrios', 'usuários')
    c = c.replace('Di\uFFFDrio', 'Diário')
    c = c.replace('di\uFFFDrio', 'diário')
    c = c.replace('Hor\uFFFDrio', 'Horário')
    c = c.replace('hor\uFFFDrio', 'horário')
    c = c.replace('Hor\uFFFDrios', 'Horários')
    c = c.replace('Or\uFFFD\uFFFDrio', 'Orçário')  # unlikely
    c = c.replace('tempor\uFFFDrio', 'temporário')
    c = c.replace('Tempor\uFFFDrio', 'Temporário')
    c = c.replace('sali\uFFFDncias', 'saliências')

    # -ável/-ível endings
    c = c.replace('Dispon\uFFFDvel', 'Disponível')
    c = c.replace('dispon\uFFFDvel', 'disponível')
    c = c.replace('poss\uFFFDvel', 'possível')
    c = c.replace('Poss\uFFFDvel', 'Possível')
    c = c.replace('compat\uFFFDvel', 'compatível')

    # -ção → single FFFD cases (where ç is only one corrupted char and ã is fine)
    # Actually no: ç=E7→FFFD, ã=E3→FFFD. So -ção always has 2× FFFD.
    # But: Ação = Á+ç+ã+o = Á=0xC1 (2-byte lead in UTF-8), ç=0xE7 (3-byte lead), ã=E3, o=6F
    # C1 → 0xC1 = 11000001. As 2-byte lead needs C1 XX with XX in 80-BF. ç=E7 is NOT 10xxxxxx → invalid → FFFD.
    # So Á alone → FFFD, ç alone → FFFD, ã alone → FFFD.
    # "Ação" in CP1252: C1 E7 E3 6F → each of C1,E7,E3 → FFFD→ 3 FFFDs + o!
    # But "ação" (lowercase a + ção = a + ç + ã + o): a=61 + ç=E7 + ã=E3 + o=6F → E7→FFFD, E3→FFFD → ação = "a\uFFFD\uFFFDo"
    # So lowercase 'a' before -ção is fine (ASCII), giving 2×FFFD pattern.
    # "Ação" (uppercase) = Á+ção: Á=C1→FFFD, + 2×FFFD for ção + o = 3×FFFD+o
    c = c.replace('\uFFFD\uFFFD\uFFFDo', 'Ação')  # could be "Ação" (3 FFFDs + o)
    # Actually let me be more careful with this:
    c = c.replace('A\uFFFD\uFFFDo', 'Ação')
    c = c.replace('a\uFFFD\uFFFDo', 'ação')  # already handled by pattern above
    
    # More 2-FFFD patterns
    c = c.replace('Conte\uFFFDdo', 'Conteúdo')
    c = c.replace('conte\uFFFDdo', 'conteúdo')
    c = c.replace('Estat\uFFFDstica', 'Estatística')
    c = c.replace('estat\uFFFDstica', 'estatística')
    c = c.replace('Estat\uFFFDsticas', 'Estatísticas')
    c = c.replace('estat\uFFFDsticas', 'estatísticas')
    c = c.replace('Vers\uFFFDo', 'Versão')
    c = c.replace('vers\uFFFDo', 'versão')
    c = c.replace('Vers\uFFFDes', 'Versões')

    # É-words (é = 0xE9 → FFFD)  
    c = c.replace('N\uFFFDvel', 'Nível')
    c = c.replace('n\uFFFDvel', 'nível')
    c = c.replace('Cen\uFFFDrio', 'Cenário')
    c = c.replace('cen\uFFFDrio', 'cenário')
    c = c.replace('Cen\uFFFDrios', 'Cenários')

    # Ó-words (ó = 0xF3 → FFFD)
    c = c.replace('C\uFFFDdigo', 'Código')
    c = c.replace('c\uFFFDdigo', 'código')
    c = c.replace('m\uFFFDximo', 'máximo')
    c = c.replace('M\uFFFDximo', 'Máximo')
    c = c.replace('m\uFFFDnimo', 'mínimo')
    c = c.replace('M\uFFFDnimo', 'Mínimo')
    c = c.replace('m\uFFFDtodo', 'método')
    c = c.replace('M\uFFFDtodo', 'Método')
    c = c.replace('n\uFFFDmero', 'número')
    c = c.replace('N\uFFFDmero', 'Número')
    c = c.replace('\uFFFDltimo', 'último')
    c = c.replace('\uFFFDltimas', 'últimas')
    c = c.replace('\uFFFDltimamente', 'ultimamente')

    # Â/â (â = 0xE2... wait: but â in UTF-8 = C3 A2 = 2-byte seq. C3=1-byte CP1252 for Ã → written as C3. A2=continuation → C3 A2 = valid UTF-8 for â! So â SURVIVES! Let me reconsider.
    # Actually: Â = U+00C2. CP1252 byte = 0xC2. In UTF-8: 0xC2 is a 2-byte lead needing 1 continuation.
    # Next byte depends on what follows. If 'â' is followed by a regular letter 'n' (0x6E), then:
    # C2 6E: C2=lead, 6E=ASCII not continuation → FFFD for C2. 0x6E='n'. So â → FFFD.
    # But â in UTF-8 = C3 A2. When written as CP1252: C3→Ã, A2=continuation byte in UTF-8
    # Wait: CP1252 for â (U+00E2) = 0xE2 (single byte). Not C3 A2.
    # When CP1252 0xE2 is read as UTF-8: E2 = 3-byte lead. Next 2 must be 80-BF.
    # If next is an ASCII char, invalid → FFFD.
    # So â → FFFD (same as other accented chars).
    c = c.replace('Banco\uFFFD', 'Banco')  # probably not needed
    c = c.replace('C\uFFFDlculo', 'Cálculo')
    c = c.replace('c\uFFFDlculo', 'cálculo')
    c = c.replace('Pr\uFFFDtico', 'Prático')
    c = c.replace('pr\uFFFDtico', 'prático')
    c = c.replace('Autom\uFFFDtico', 'Automático')
    c = c.replace('autom\uFFFDtico', 'automático')
    c = c.replace('Autom\uFFFDtica', 'Automática')
    c = c.replace('autom\uFFFDtica', 'automática')
    c = c.replace('Cient\uFFFDfico', 'Científico')
    c = c.replace('cient\uFFFDfico', 'científico')
    c = c.replace('Cient\uFFFDfica', 'Científica')
    c = c.replace('cient\uFFFDfica', 'científica')
    c = c.replace('Din\uFFFDmico', 'Dinâmico')
    c = c.replace('din\uFFFDmico', 'dinâmico')
    c = c.replace('Gram\uFFFDtica', 'Gramática')
    c = c.replace('tem\uFFFDtico', 'temático')
    c = c.replace('Tem\uFFFDtico', 'Temático')
    c = c.replace('Matem\uFFFDtico', 'Matemático')
    c = c.replace('matem\uFFFDtico', 'matemático')
    c = c.replace('Matem\uFFFDtica', 'Matemática')
    c = c.replace('matem\uFFFDtica', 'matemática')

    # Specific words from file
    c = c.replace('B\uFFFDsico', 'Básico')
    c = c.replace('b\uFFFDsico', 'básico')
    c = c.replace('B\uFFFDsica', 'Básica')
    c = c.replace('b\uFFFDsica', 'básica')
    c = c.replace('B\uFFFDsicos', 'Básicos')
    c = c.replace('B\uFFFDsicas', 'Básicas')
    c = c.replace('\uFFFDcone', 'Ícone')
    c = c.replace('\uFFFDcones', 'Ícones')
    c = c.replace('T\uFFFDtulo', 'Título')
    c = c.replace('t\uFFFDtulo', 'título')
    c = c.replace('T\uFFFDtulos', 'Títulos')
    c = c.replace('T\uFFFDticos', 'Táticos')
    c = c.replace('t\uFFFDticos', 'táticos')
    c = c.replace('T\uFFFDtica', 'Tática')
    c = c.replace('t\uFFFDtica', 'tática')
    c = c.replace('T\uFFFDticas', 'Táticas')
    c = c.replace('t\uFFFDticas', 'táticas')
    c = c.replace('T\uFFFDtico', 'Tático')
    c = c.replace('t\uFFFDtico', 'tático')
    c = c.replace('t\uFFFDpico', 'típico')
    c = c.replace('T\uFFFDpico', 'Típico')
    c = c.replace('t\uFFFDpica', 'típica')
    c = c.replace('T\uFFFDpica', 'Típica')
    c = c.replace('R\uFFFDpida', 'Rápida')
    c = c.replace('r\uFFFDpida', 'rápida')
    c = c.replace('R\uFFFDpido', 'Rápido')
    c = c.replace('r\uFFFDpido', 'rápido')
    c = c.replace('Dram\uFFFDtica', 'Dramática')
    c = c.replace('dram\uFFFDtica', 'dramática')
    c = c.replace('Urg\uFFFDncia', 'Urgência')
    c = c.replace('El\uFFFDtrico', 'Elétrico')
    c = c.replace('el\uFFFDtrico', 'elétrico')
    c = c.replace('El\uFFFDtrica', 'Elétrica')
    c = c.replace('El\uFFFDtricos', 'Elétricos')
    c = c.replace('Energ\uFFFDtico', 'Energético')
    c = c.replace('energ\uFFFDtico', 'energético')
    c = c.replace('est\uFFFDmulo', 'estímulo')
    c = c.replace('Est\uFFFDmulo', 'Estímulo')
    c = c.replace('estrat\uFFFDgia', 'estratégia')
    c = c.replace('Estrat\uFFFDgia', 'Estratégia')
    c = c.replace('estrat\uFFFDgias', 'estratégias')
    c = c.replace('Estrat\uFFFDgias', 'Estratégias')
    c = c.replace('experi\uFFFDncia', 'experiência')
    c = c.replace('Experi\uFFFDncia', 'Experiência')
    c = c.replace('R\uFFFDgressivo', 'Regressivo')
    c = c.replace('regress\uFFFDvo', 'regressivo')
    c = c.replace('sint\uFFFDtico', 'sintético')
    c = c.replace('Otimiza\uFFFD\uFFFDo', 'Otimização')
    c = c.replace('otimiza\uFFFD\uFFFDo', 'otimização')
    c = c.replace('Refinamento', 'Refinamento')  # no FFFD
    c = c.replace('T\uFFFDtico de', 'Tático de')
    c = c.replace('refinamento T\uFFFDtico', 'refinamento Tático')
    c = c.replace('Refinamento T\uFFFDtico', 'Refinamento Tático')

    # confus-ão, ões endings that weren't caught
    c = c.replace('confus\uFFFDo', 'confusão')
    c = c.replace('Confus\uFFFDo', 'Confusão')
    c = c.replace('exig\uFFFDncia', 'exigência')
    c = c.replace('Exig\uFFFDncia', 'Exigência')
    c = c.replace('exposi\uFFFD\uFFFDo', 'exposição')
    c = c.replace('Exposi\uFFFD\uFFFDo', 'Exposição')

    # Specific from file scan
    c = c.replace('autom\uFFFDtica', 'automática')
    c = c.replace('C\uFFFDlculo', 'Cálculo')
    c = c.replace('c\uFFFDlculo', 'cálculo')
    c = c.replace('dura\uFFFD\uFFFDo', 'duração')
    c = c.replace('Dura\uFFFD\uFFFDo', 'Duração')
    c = c.replace('identidade', 'identidade')  # no FFFD
    c = c.replace('sincroniza\uFFFD\uFFFDo', 'sincronização')
    c = c.replace('otimiza\uFFFD\uFFFDo', 'otimização')

    c = c.replace('sep\uFFFDl', 'separárl')  # unlikely; skip
    c = c.replace('Pr\uFFFDx. Reset', 'Próx. Reset')
    c = c.replace('pr\uFFFDx. Reset', 'próx. Reset')

    c = c.replace('S\uFFFDo', 'São')  # for São Paulo type uses or "são (they are)"
    c = c.replace('s\uFFFDo', 'são')
    c = c.replace('Gin\uFFFDsios', 'Ginásios')
    c = c.replace('gin\uFFFDsios', 'ginásios')
    c = c.replace('C\uFFFDes Legend\uFFFDrios', 'Cães Lendários')
    c = c.replace('c\uFFFDes legend\uFFFDrios', 'cães lendários')
    c = c.replace('Legend\uFFFDrios', 'Lendários')
    c = c.replace('legend\uFFFDrios', 'lendários')

    c = c.replace('Profiss\uFFFDo', 'Profissão')
    c = c.replace('profiss\uFFFDo', 'profissão')
    c = c.replace('Profiss\uFFFDes', 'Profissões')
    c = c.replace('Sess\uFFFDo', 'Sessão')
    c = c.replace('sess\uFFFDo', 'sessão')
    c = c.replace('Vis\uFFFDo', 'Visão')
    c = c.replace('vis\uFFFDo', 'visão')

    c = c.replace('Cl\uFFFD\b', 'Clã')
    c = c.replace('cl\uFFFD', 'clã')
    c = c.replace('Cl\uFFFDs', 'Clãs')
    c = c.replace('Cl\uFFFD', 'Clã')

    c = c.replace('Sem Profiss\uFFFDo', 'Sem Profissão')

    # Admin comments
    c = c.replace('ADMINISTRA\uFFFD\uFFFDO', 'ADMINISTRAÇÃO')
    c = c.replace('administra\uFFFD\uFFFDo', 'administração')
    c = c.replace('SEGURAN\uFFFDA', 'SEGURANÇA')
    c = c.replace('Seguran\uFFFDa', 'Segurança')
    c = c.replace('seguran\uFFFDa', 'segurança')

    # Encoding/sanitization terms
    c = c.replace('sanitiza\uFFFD\uFFFDo', 'sanitização')
    c = c.replace('Sanitiza\uFFFD\uFFFDo', 'Sanitização')
    c = c.replace('encripta\uFFFD\uFFFDo', 'encriptação')
    c = c.replace('Encripta\uFFFD\uFFFDo', 'Encriptação')

    # More from file lines
    c = c.replace('Requisito B\uFFFDsic', 'Requisito Básic')
    c = c.replace('Gest\uFFFDo de Ber', 'Gestão de Ber')
    c = c.replace('Caminho Estelar', 'Caminho Estelar')  # no FFFD
    c = c.replace('Cr\uFFFDtico opcional', 'Crítico opcional')
    c = c.replace('Cr\uFFFDtico\)', 'Crítico)')

    # Error messages
    c = c.replace('N\uFFFDo foi poss\uFFFDvel', 'Não foi possível')
    c = c.replace('n\uFFFDo foi poss\uFFFDvel', 'não foi possível')
    c = c.replace('N\uFFFDo \uFFFD admin', 'Não é admin')
    c = c.replace('n\uFFFDo \uFFFD admin', 'não é admin')
    c = c.replace('falha ao', 'falha ao')  # no FFFD
    c = c.replace('Falha ao atualizar an\uFFFDncio', 'Falha ao atualizar anúncio')
    c = c.replace('falha ao atualizar an\uFFFDncio', 'falha ao atualizar anúncio')
    c = c.replace('Erro Cr\uFFFDtico', 'Erro Crítico')
    c = c.replace('erro cr\uFFFDtico', 'erro crítico')
    c = c.replace('Erro de conex\uFFFDo', 'Erro de conexão')
    c = c.replace('erro de conex\uFFFDo', 'erro de conexão')
    c = c.replace('Sem an\uFFFDncios', 'Sem anúncios')
    c = c.replace('Sem conte\uFFFDdo', 'Sem conteúdo')
    c = c.replace('Sem an\uFFFDncio ativo', 'Sem anúncio ativo')

    # Common JS comments
    c = c.replace('Din\uFFFDmico', 'Dinâmico')
    c = c.replace('Mapeamento Din\uFFFDmico', 'Mapeamento Dinâmico')

    # é in various contexts
    c = c.replace('\uFFFD uma lista', 'é uma lista')
    c = c.replace('\uFFFD admin', 'é admin')
    c = c.replace('\uFFFD poss\uFFFDvel', 'é possível')
    c = c.replace('\uFFFD uma', 'é uma')
    c = c.replace('\xc2\xa0', '\xa0')  # NBSP double-encoded

    # Version / release notes (changelog section)
    c = c.replace('Atualiza\uFFFD\uFFFDo v', 'Atualização v')
    c = c.replace('Vers\uFFFDo 1.', 'Versão 1.')
    c = c.replace('Vers\uFFFDo do App', 'Versão do App')
    c = c.replace('VERS\uFFFDO 1.', 'VERSÃO 1.')
    c = c.replace('Identidade Visual', 'Identidade Visual')  # no FFFD
    c = c.replace('Codifica\uFFFD\uFFFDo Visual', 'Codificação Visual')
    c = c.replace('codifica\uFFFD\uFFFDo visual', 'codificação visual')
    c = c.replace('Color Coding\)', 'Color Coding)')  # fine
    c = c.replace('Aten\uFFFD\uFFFDo Cognitiva', 'Atenção Cognitiva')
    c = c.replace('Otimiza\uFFFD\uFFFDo de Layout', 'Otimização de Layout')
    c = c.replace('reestruturado de forma fluida', 'reestruturado de forma fluida')  # fine
    c = c.replace('c\uFFFDdigo principal', 'código principal')
    c = c.replace('Arquitetura de Software\)', 'Arquitetura de Software)')  # fine
    c = c.replace('softwaree c\uFFFDdigo', 'software e código')
    c = c.replace('\uFFFDcone (favicon)', 'Ícone (favicon)')
    c = c.replace('Notifica\uFFFD\uFFFDes de Alto Impacto', 'Notificações de Alto Impacto')
    c = c.replace('est\uFFFDmulos visuais', 'estímulos visuais')
    c = c.replace('Log Oficial Integrado', 'Log Oficial Integrado')  # fine
    c = c.replace('Liga\uFFFD\uFFFDo Direta', 'Ligação Direta')
    c = c.replace('Ajuste de Hor\uFFFDrios', 'Ajuste de Horários')
    c = c.replace('sincroniza\uFFFD\uFFFDo', 'sincronização')
    c = c.replace('Novo Hor\uFFFDrio', 'Novo Horário')
    c = c.replace('Aten\uFFFD\uFFFDo \(Marcadores\)', 'Atenção (Marcadores)')
    c = c.replace('marca\uFFFD\uFFFDo', 'marcação')  # already handled
    c = c.replace('Dados Cient\uFFFDficos', 'Dados Científicos')
    c = c.replace('dados cient\uFFFDficos', 'dados científicos')
    c = c.replace('Refinamento T\uFFFDtico', 'Refinamento Tático')
    c = c.replace('Dados Precisos', 'Dados Precisos')  # fine
    c = c.replace('t\uFFFDtico sobre a exig\uFFFDncia', 'tático sobre a exigência')
    c = c.replace('Unifica\uFFFD\uFFFDo do Sistema', 'Unificação do Sistema')
    c = c.replace('c\uFFFDdigo principal \(Hardcoded\)', 'código principal (Hardcoded)')
    c = c.replace('Privacidade Cibersegura', 'Privacidade Cibersegura')  # fine
    c = c.replace('Remo\uFFFD\uFFFDo definitiva', 'Remoção definitiva')
    c = c.replace('Qualidade de Vida', 'Qualidade de Vida')  # fine
    c = c.replace('Bot\uFFFDes para', 'Botões para')
    c = c.replace('bot\uFFFDes para', 'botões para')

    # More FFFD patterns from extended scan
    c = c.replace('agora fazem parte do c\uFFFDdigo', 'agora fazem parte do código')
    c = c.replace('Adicionada Dura\uFFFD\uFFFDo Estimada', 'Adicionada Duração Estimada')
    c = c.replace('As chaves de storage', 'As chaves de storage')  # fine
    c = c.replace('s\uFFFDo mantidas', 'são mantidas')
    c = c.replace('Calcula n\uFFFDmero de dias', 'Calcula número de dias')
    c = c.replace('Obt\uFFFDm o \uFFFDndice', 'Obtém o índice')
    c = c.replace('Fun\uFFFD\uFFFDo para obter', 'Função para obter')
    c = c.replace('Mapeamento de nomes de boss para dados t\uFFFDpicos', 'Mapeamento de nomes de boss para dados típicos')
    c = c.replace('L\uFFFDgica: Verifica', 'Lógica: Verifica')
    c = c.replace('L\uFFFDgica Cient\uFFFDfica', 'Lógica Científica')
    c = c.replace('Alerta 5 min antes', 'Alerta 5 min antes')  # fine
    c = c.replace('Feedback Auditivo Matem\uFFFDtico', 'Feedback Auditivo Matemático')
    c = c.replace('Feedback Visual \(Notifica\uFFFD\uFFFDo Push', 'Feedback Visual (Notificação Push')
    c = c.replace('do Sistema Operativo\)', 'do Sistema Operativo)')
    c = c.replace('Mensagens \uFFFDpicas tem\uFFFDticas baseadas', 'Mensagens épicas temáticas baseadas')
    c = c.replace('Feedback Visual Gamer \(Alerta t\uFFFDpico', 'Feedback Visual Gamer (Alerta típico')
    c = c.replace('Dados tem\uFFFDticos do Boss', 'Dados temáticos do Boss')
    c = c.replace('Aplica\uFFFD\uFFFDo autom\uFFFDtica de Estado', 'Aplicação automática de Estado')
    c = c.replace('Ativa/Desativa o modo COMBATE \uFFFDPICO', 'Ativa/Desativa o modo COMBATE ÉPICO')
    c = c.replace('Adiciona classe de combate \uFFFDpica', 'Adiciona classe de combate épica')
    c = c.replace('Adiciona \uFFFDcone de Pok\uFFFDbola girando', 'Adiciona ícone de Pokébola girando')
    c = c.replace('Oculta o alerta ap\uFFFDs', 'Oculta o alerta após')
    c = c.replace('ap\uFFFDs', 'após')
    c = c.replace('@pis', '@pis')  # fine
    c = c.replace('SISTEMA DE ADMINISTRA\uFFFD\uFFFDO', 'SISTEMA DE ADMINISTRAÇÃO')
    c = c.replace('Escuta a cole\uFFFD\uFFFDo de tickets', 'Escuta a coleção de tickets')
    c = c.replace('Sem Profiss\uFFFDo', 'Sem Profissão')
    c = c.replace('Total de Usu\uFFFDrios', 'Total de Usuários')
    c = c.replace('An\uFFFDnimo', 'Anônimo')
    c = c.replace('\uFFFDltima visita', 'última visita')
    c = c.replace('Nenhuma sess\uFFFDo de visitante', 'Nenhuma sessão de visitante')
    c = c.replace('sess\uFFFDes recentes', 'sessões recentes')
    c = c.replace('Modo visitante: exibindo sess\uFFFDes recentes', 'Modo visitante: exibindo sessões recentes')
    c = c.replace('Modo local: estat\uFFFDsticas limitadas', 'Modo local: estatísticas limitadas')
    c = c.replace('Gerenciar Conte\uFFFDdo', 'Gerenciar Conteúdo')
    c = c.replace('gerenciar conte\uFFFDdo', 'gerenciar conteúdo')
    c = c.replace('Vers\uFFFDo do App', 'Versão do App')
    c = c.replace('edite diretamente o c\uFFFDdigo HTML', 'edite diretamente o código HTML')
    c = c.replace('configura\uFFFD\uFFFDes', 'configurações')
    c = c.replace('Configura\uFFFD\uFFFDes do Sistema', 'Configurações do Sistema')
    c = c.replace('Modo Manuten\uFFFD\uFFFDo', 'Modo Manutenção')
    c = c.replace('modo manuten\uFFFD\uFFFDo', 'modo manutenção')
    c = c.replace('Desabilitar Feedback de Usu\uFFFDrios', 'Desabilitar Feedback de Usuários')
    c = c.replace('Limite de Level M\uFFFDximo', 'Limite de Level Máximo')

    # Fallback CSV/JSON parsing comments
    c = c.replace('Fallback cient\uFFFDfico', 'Fallback científico')
    c = c.replace('Deteta automaticamente qual separador foi usado no ficheiro', 'Deteta automaticamente qual separador foi usado no ficheiro')  # fine
    c = c.replace('V\uFFFDrgula, Ponto-e-v\uFFFDgula ou Tab', 'Vírgula, Ponto-e-vírgula ou Tab')
    c = c.replace('Pula as linhas de cabe\uFFFDalho', 'Pula as linhas de cabeçalho')
    c = c.replace('N\uFFFDo foi poss\uFFFDvel aceder', 'Não foi possível aceder')
    c = c.replace('Mapeamento Din\uFFFDmico: Extrai os valores por POSI\uFFFD\uFFFDO', 'Mapeamento Dinâmico: Extrai os valores por POSIÇÃO')
    c = c.replace('Cen\uFFFDrio A: O JSON \uFFFD uma lista', 'Cenário A: O JSON é uma lista')
    c = c.replace('Cen\uFFFDrio B: O JSON \uFFFD uma lista', 'Cenário B: O JSON é uma lista')
    c = c.replace('Limpeza final de seguran\uFFFDa', 'Limpeza final de segurança')
    c = c.replace('Se falhar a leitura JSON', 'Se falhar a leitura JSON')  # fine
    c = c.replace('aciona o Fallback Cient\uFFFDfico', 'aciona o Fallback Científico')
    c = c.replace('Erro Cr\uFFFDtico no Banco de Orbs', 'Erro Crítico no Banco de Orbs')
    c = c.replace('Erro de conex\uFFFDo ao Banco', 'Erro de conexão ao Banco')
    c = c.replace('Dispara a fun\uFFFD\uFFFDo de carregamento', 'Dispara a função de carregamento')

    # Auth UI comments
    c = c.replace('Fun\uFFFDes de Auth e UI de Perfil', 'Funções de Auth e UI de Perfil')
    c = c.replace('Valida\uFFFD\uFFFDo de admin via Firestore', 'Validação de admin via Firestore')
    c = c.replace('seguro, server-side verifica', 'seguro, server-side verifica')  # fine
    c = c.replace('Valida\uFFFD\uFFFDo segura de admin via Firestore', 'Validação segura de admin via Firestore')
    c = c.replace('n\uFFFDo exp\uFFFDe email', 'não expõe email')
    c = c.replace('SISTEMA DE AUTO-ATUALIZA\uFFFD\uFFFDO', 'SISTEMA DE AUTO-ATUALIZAÇÃO')
    c = c.replace('SEGURAN\uFFFDA E ADMINISTRA\uFFFD\uFFFDO MESTRA', 'SEGURANÇA E ADMINISTRAÇÃO MESTRA')
    c = c.replace('SISTEMA DE CICLO DE BOSSES DI\uFFFDRIOS', 'SISTEMA DE CICLO DE BOSSES DIÁRIOS')
    c = c.replace('Valida\uFFFD\uFFFDo segura', 'Validação segura')
    c = c.replace('~ Admin detectado via sess\uFFFDo local', '~ Admin detectado via sessão local')
    c = c.replace('n\uFFFDo \uFFFD admin', 'não é admin')
    c = c.replace('~~~ Valida\uFFFD\uFFFDo de dados de entrada', '~~~ Validação de dados de entrada')
    c = c.replace('Fun\uFFFD\uFFFDo segura de sanitiza\uFFFD\uFFFDo contra XSS', 'Função segura de sanitização contra XSS')

    # RNG/variance terms
    c = c.replace('estrat\uFFFDgias de vari\uFFFDncia \(RNG\)', 'estratégias de variância (RNG)')
    c = c.replace('estrat\uFFFDgias de vari\uFFFDncia', 'estratégias de variância')
    c = c.replace('Conceitos T\uFFFDticos', 'Conceitos Táticos')
    c = c.replace('otimiza\uFFFD\uFFFDo matem\uFFFDtica', 'otimização matemática')
    c = c.replace('experi\uFFFDncia para', 'experiência para')
    c = c.replace('exige certa experi\uFFFDncia', 'exige certa experiência')

    # Pokémon type badge comment
    c = c.replace('Badge de Tipo Pok\uFFFDmon', 'Badge de Tipo Pokémon')
    c = c.replace('Bot\uFFFDo de A\uFFFD\uFFFDo', 'Botão de Ação')
    c = c.replace('bot\uFFFDo de a\uFFFD\uFFFDo', 'botão de ação')
    c = c.replace('ESTILOS DO POK\uFFFDLOG', 'ESTILOS DO POKÉLOG')
    c = c.replace('Efeito Pok\uFFFDbola \(\uFFFDcone Animado\)', 'Efeito Pokébola (Ícone Animado)')
    c = c.replace('Informa\uFFFD\uFFFDes do Boss', 'Informações do Boss')
    c = c.replace('NOVA Anima\uFFFD\uFFFDo: Efeito Pulsa\uFFFD\uFFFDo Chamativo', 'NOVA Animação: Efeito Pulsação Chamativo')
    c = c.replace('Pok\uFFFDbola Girando no Banner', 'Pokébola Girando no Banner')
    c = c.replace('Separador t\uFFFDpico', 'Separador típico')
    c = c.replace('T\uFFFDtulo do Alerta \(Efeito de Texto\)', 'Título do Alerta (Efeito de Texto)')

    # More changelog notes
    c = c.replace('Descubra como esta plataforma otimiza a Gest\uFFFDo', 'Descubra como esta plataforma otimiza a Gestão')
    c = c.replace('Os dados s\uFFFDo encriptados', 'Os dados são encriptados')
    c = c.replace('Os dados ficam retidos estritamente', 'Os dados ficam retidos estritamente')  # fine
    c = c.replace('Gest\uFFFDo Integr', 'Gestão Integr')
    c = c.replace('Painel de controlo centraliz', 'Painel de controlo centraliz')  # fine
    c = c.replace('Automatiza\uFFFD\uFFFD', 'Automatização')
    # Already handled above but some specific ones:
    c = c.replace('Painel de fluxo de caixa que', 'Painel de fluxo de caixa que')  # fine
    c = c.replace('Mapeamento interativo das 24', 'Mapeamento interativo das 24')  # fine
    c = c.replace('Estimula\uFFFD\uFFFDo visual \(pulsa\uFFFD\uFFFDes\)', 'Estimulação visual (pulsações)')
    c = c.replace('T\uFFFDticas F2P \(An', 'Táticas F2P (An')
    c = c.replace('para n\uFFFD', 'para não')
    c = c.replace('Conex\uFFFDo em tempo real', 'Conexão em tempo real')
    c = c.replace('ADMIN -->', 'ADMIN -->')  # fine
    c = c.replace('Controle total do sistema, dados, an\uFFFDncios e configura\uFFFD\uFFFDes.',
                  'Controle total do sistema, dados, anúncios e configurações.')
    c = c.replace('Acompanhe em tempo real as \uFFFDltimas atualiza\uFFFD\uFFFDes diretas do jogo',
                  'Acompanhe em tempo real as últimas atualizações diretas do jogo')
    c = c.replace('\uFFFDltimas atualiza\uFFFD\uFFFDes PXG', 'Últimas atualizações PXG')
    c = c.replace('Atualiza\uFFFD\uFFFDo v1.3.', 'Atualização v1.3.')
    c = c.replace('VERS\uFFFDO 1.3.', 'VERSÃO 1.3.')
    c = c.replace('Atualiza\uFFFD\uFFFDo Melhoria Combate', 'Atualização Melhoria Combate')

    # obs section
    c = c.replace('\uFFFD Observa\uFFFD\uFFFDo T\uFFFDt', '⚠ Observação Tít')  # the '??' bullet before "Observação"
    # Actually those observation headers showed as '? Observa...' which is single ? = single emoji
    # Let me handle them differently - they were in spans with specific classes
    c = c.replace('font-black text-red-400">? Observa\uFFFD\uFFFDo T\uFFFDt',
                  'font-black text-red-400">\u26a0 Observação Tít')
    c = c.replace('font-black text-yellow-400">? Observa\uFFFD\uFFFDo',
                  'font-black text-yellow-400">\u26a0 Observação')

    # Generic remaining patterns
    c = c.replace('Food Alternativo', 'Food Alternativo')  # fine
    c = c.replace('Held Item Padroniz\uFFFDdo', 'Held Item Padronizado')
    c = c.replace('padroniz\uFFFDdo', 'padronizado')
    c = c.replace('desenvolvidas e validada', 'desenvolvidas e validada')  # fine

    # Mês / dia strings
    c = c.replace('finMonth: "M\uFFFDs"', 'finMonth: "Mês"')
    c = c.replace('finMonth: \'M\uFFFDs\'', "finMonth: 'Mês'")

    # "Sem conteúdo" patterns
    c = c.replace("Sem conte\uFFFDdo.", "Sem conteúdo.")
    c = c.replace("nenhum an\uFFFDncio ativo", "nenhum anúncio ativo")
    c = c.replace("Nenhum an\uFFFDncio ativo", "Nenhum anúncio ativo")

    # Handle remaining single-FFFD cases with more specificity
    c = c.replace('Onda suave e agrad\uFFFDvel', 'Onda suave e agradável')
    c = c.replace('\uFFFDudio bloqueado pelo navegador', 'Áudio bloqueado pelo navegador')
    c = c.replace('at\uFFFD intera\uFFFD\uFFFDo do utilizador', 'até interação do utilizador')
    c = c.replace('Pr\uFFFDx. Evento:', 'Próx. Evento:')
    c = c.replace('pr\uFFFDximo', 'próximo')
    c = c.replace('Pr\uFFFDximo', 'Próximo')
    c = c.replace('\uFFFDs', 'às')  # às horas → "às"... careful with this one
    # More specific:
    c = c.replace(' \uFFFDs ', ' às ')
    c = c.replace('\uFFFDs ${hh}:', 'às ${hh}:')

    # Music/audio
    c = c.replace("osc.type = 'sine'; // Onda suave e agrad\uFFFDvel",
                  "osc.type = 'sine'; // Onda suave e agradável")

    # Pokélog section
    c = c.replace('Pok\uFFFDlog Oficial Integrado', 'Pokélog Oficial Integrado')

    # Restore original ' ã ' (ã alone)
    c = c.replace(' \uFFFD ', ' ã ')  # be careful: might match wrong things

    # Final cleanup - protect known patterns
    # (none needed)

    return c


# Read, fix, write each file
files = [
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\index.html',
    r'c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html',
]

for filepath in files:
    if not os.path.exists(filepath):
        print(f'SKIP (not found): {filepath}')
        continue
    
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Decode with replacement for any remaining invalid bytes
    content = raw.decode('utf-8', errors='replace')
    original_len = len(content)
    fffd_before = content.count('\ufffd')
    qq_before = content.count('??')
    
    # Apply fixes
    content = fix_content(content)
    
    fffd_after = content.count('\ufffd')
    qq_after = content.count('??')
    
    # Write as UTF-8 without BOM
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    
    print(f'Fixed: {filepath}')
    print(f'  U+FFFD: {fffd_before} → {fffd_after} (fixed {fffd_before - fffd_after})')
    print(f'  "??": {qq_before} → {qq_after} (fixed {qq_before - qq_after})')
    if fffd_after > 0:
        print(f'  WARNING: {fffd_after} U+FFFD still remaining')
    if qq_after > 0:
        print(f'  WARNING: {qq_after} "??" still remaining')
    print()
