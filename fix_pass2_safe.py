#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

FFFD = "\ufffd"


def apply_fixes(text: str) -> str:
    # Focused textual repairs (safe and explicit)
    replacements = [
        ("Bot�o", "Botão"),
        ("NOTIFICA��O", "NOTIFICAÇÃO"),
        ("j�", "já"),
        ("tamb�m", "também"),
        ("Por�m", "Porém"),
        ("n�o", "não"),
        ("N�o", "Não"),
        ("conclu�das", "concluídas"),
        ("conclu�da", "concluída"),
        ("conclu�rem", "concluírem"),
        ("pend�ncias", "pendências"),
        ("interven��es", "intervenções"),
        ("Restri��es", "Restrições"),
        ("l�quidos", "líquidos"),
        ("�reas", "áreas"),
        ("est�tuas", "estátuas"),
        ("execu��o", "execução"),
        ("padr�es", "padrões"),
        ("�udio", "áudio"),
        ("mec�nicos", "mecânicos"),
        ("depend�ncia", "dependência"),
        ("coer�ncia", "coerência"),
        ("pre�os", "preços"),
        ("atualiza��es", "atualizações"),
        ("�nico", "único"),
        ("cor �nica", "cor única"),
        ("�til", "útil"),
        ("ecr�", "ecrã"),
        ("ecràs", "ecrãs"),
        ("se��o", "seção"),
        ("SE��O", "SEÇÃO"),
        ("DI�RIOS", "DIÁRIOS"),
        ("V�rgula", "Vírgula"),
        ("v�rgula", "vírgula"),
        ("s� cont�m", "só contêm"),
        ("s� est�", "só está"),
        ("h� ", "há "),
        ("at�", "até"),
        ("nãoveis", "níveis"),
        ("Apàs", "Após"),
        ("Ap\ufffds", "Após"),
        ("ap\ufffds", "após"),
        ("In�cio", "Início"),
        ("p\ufffdgina", "página"),
        ("P\ufffdgina", "Página"),
        ("p\ufffdblico", "público"),
        ("p\ufffdblicos", "públicos"),
        ("v\ufffdlido", "válido"),
        ("inv\ufffdlido", "inválido"),
        ("conlu\ufffdrem", "concluírem"),
        ("sequ\ufffdncia", "sequência"),
        ("pr\ufffdpria", "própria"),
        ("vari\ufffdncia", "variância"),
        ("mem\ufffdria", "memória"),
        ("tempor\ufffdria", "temporária"),
        ("\ufffdudio din\ufffdmico", "áudio dinâmico"),
        ("Sobreviv�ncia", "Sobrevivência"),
        ("m�o", "mão"),
        ("telem�vel", "telemóvel"),
        ("telem�veis", "telemóveis"),
        ("hist�rico", "histórico"),
        ("irrevers�vel", "irreversível"),
        ("relat�rios", "relatórios"),
        ("Pok�XGames", "PokéXGames"),
        ("Fa�a", "Faça"),
        ("poder�", "poderá"),
        ("acess�-los", "acessá-los"),
        ("desmarc�-la", "desmarcá-la"),
        ("C�es", "Cães"),
        ("ã permanente", "é permanente"),
        ("ã blindado", "é blindado"),
        ("exibi��o", "exibição"),
        ("pok�ball", "pokéball"),
        ("mant�m", "mantém"),
        ("Din�micas", "Dinâmicas"),
        ("descri��es", "descrições"),
        ("neuroci�ncia", "neurociência"),
        ("perif�rica", "periférica"),
        ("c�rebro", "cérebro"),
        ("espa�os", "espaços"),
        ("desnecess�rios", "desnecessários"),
        ("come�ar", "começar"),
        ("� 2026 PXG Check Project ã v", "© 2026 PXG Check Project · v"),
        ("N�o foi possível", "Não foi possível"),
        ("POSI��O", "POSIÇÃO"),
        ("CONCLU�DO", "CONCLUÍDO"),
        ("regi�o", "região"),
        ("espec�fico", "específico"),
        ("L�gica", "Lógica"),
        ("Dispon�veis", "Disponíveis"),
        ("mudan�a", "mudança"),
        ("ser�", "será"),
        ("An�nima", "Anônima"),
        ("INTEGRA��O", "INTEGRAÇÃO"),
        ("Corre\ufffd\ufffdo", "Correção"),
        ("Hist\ufffdrico", "Histórico"),
        ("RELAT\ufffdRIO", "RELATÓRIO"),
        ("CONCLU\ufffdDAS", "CONCLUÍDAS"),
        ("Sugest\ufffdes", "Sugestões"),
        ("Espa\ufffdo", "Espaço"),
        ("secund\ufffdrios", "secundários"),
        ("mudan\ufffdas", "mudanças"),
        ("cont\ufffdnua", "contínua"),
        ("\ufffdndice", "índice"),
        ("est\ufffd DENTRO", "está DENTRO"),
        ("est\ufffd EM COMBATE", "está EM COMBATE"),
        ("n\ufffdo encontrado", "não encontrado"),
        ("n\ufffdo suporta", "não suporta"),
        ("est\ufffdo bloqueadas", "estão bloqueadas"),
        ("Acad\ufffdmico", "Acadêmico"),
        ("Mec\ufffdnico", "Mecânico"),
        ("Arque\ufffdlogo", "Arqueólogo"),
        ("NOTIFICA\ufffd\ufffdo", "NOTIFICAÇÃO"),
        ("Fun\ufffd\ufffdes", "Funções"),
        ("INTEGRA\ufffd\ufffdo", "INTEGRAÇÃO"),
        ("Pok\ufffdlog", "Pokélog"),
        ("Pok\ufffdbola", "Pokébola"),
        ("Pok\ufffdmon", "Pokémon"),
        ("1� Lugar", "1º Lugar"),
        ("2� Lugar", "2º Lugar"),
        ("3� Lugar", "3º Lugar"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    # Navigation icons
    text = text.replace('<span class="text-[10px] font-black text-slate-300 group-hover:text-blue-400 uppercase tracking-widest">Treinadores</span>',
                        '<span class="text-[10px] font-black text-slate-300 group-hover:text-blue-400 uppercase tracking-widest">Treinadores</span>')
    text = re.sub(
        r'<span class="text-base">\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-blue-400 uppercase tracking-widest">Treinadores</span>',
        r'<span class="text-base">🏋️</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-blue-400 uppercase tracking-widest">Treinadores</span>',
        text,
    )
    text = re.sub(
        r'<span class="text-base">\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-purple-400 uppercase tracking-widest">Rainbow Orbs</span>',
        r'<span class="text-base">🌈️</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-purple-400 uppercase tracking-widest">Rainbow Orbs</span>',
        text,
    )
    text = re.sub(
        r'<span class="text-base">\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-amber-400 uppercase tracking-widest">Ranking</span>',
        r'<span class="text-base">🏆️</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-amber-400 uppercase tracking-widest">Ranking</span>',
        text,
    )
    text = re.sub(
        r'<span class="text-base">\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-emerald-400 uppercase tracking-widest">Guias F2P \(Lv 500\+\)</span>',
        r'<span class="text-base">📖️</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-emerald-400 uppercase tracking-widest">Guias F2P (Lv 500+)</span>',
        text,
    )
    text = re.sub(
        r'<span class="text-base">\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-cyan-400 uppercase tracking-widest">Pokélog</span>',
        r'<span class="text-base">📡️</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-cyan-400 uppercase tracking-widest">Pokélog</span>',
        text,
    )
    text = re.sub(
        r'<span class="text-base">\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-pink-400 uppercase tracking-widest">Sobre o Projeto</span>',
        r'<span class="text-base">ℹ️</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-pink-400 uppercase tracking-widest">Sobre o Projeto</span>',
        text,
    )
    text = re.sub(
        r'<span class="text-base">\?\?\?</span>(\s*)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-rose-400 uppercase tracking-widest">Painel Admin</span>',
        r'<span class="text-base">⚙️🔒</span>\1<span class="text-[10px] font-black text-slate-300 group-hover:text-rose-400 uppercase tracking-widest">Painel Admin</span>',
        text,
    )

    # Arsenal and notes icons
    text = text.replace('<h3 class="text-sm font-black text-blue-300 uppercase italic mb-3 flex items-center gap-2"><span>??</span> Notas Sobre Food e Held Item</h3>',
                        '<h3 class="text-sm font-black text-blue-300 uppercase italic mb-3 flex items-center gap-2"><span>📝️</span> Notas Sobre Food e Held Item</h3>')
    text = text.replace('<h3 class="text-sm font-black text-white uppercase italic mb-4 flex items-center gap-2"><span class="text-emerald-500">??</span> Arsenal de Otimização</h3>',
                        '<h3 class="text-sm font-black text-white uppercase italic mb-4 flex items-center gap-2"><span class="text-emerald-500">⚙️</span> Arsenal de Otimização</h3>')
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-indigo-400)', r'<span class="text-lg">📋️</span>\1', text, count=1)
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-emerald-400)', r'<span class="text-lg">🔄️</span>\1', text, count=1)
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-amber-400)', r'<span class="text-lg">💰️</span>\1', text, count=1)
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-purple-400)', r'<span class="text-lg">🌈️</span>\1', text, count=1)
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-rose-400)', r'<span class="text-lg">⏰️</span>\1', text, count=1)
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-cyan-400)', r'<span class="text-lg">📖️</span>\1', text, count=1)
    text = re.sub(r'<span class="text-lg">\?\?</span>(\s*<div>\s*<span class="text-\[10px\] font-black text-blue-400)', r'<span class="text-lg">📡️</span>\1', text, count=1)

    # Forms
    text = text.replace('<option value="sugestao">?? Sugestão de Melhoria</option>', '<option value="sugestao">💡️ Sugestão de Melhoria</option>')
    text = text.replace('<option value="bug">?? Reportar um Erro/Bug</option>', '<option value="bug">🐛️ Reportar um Erro/Bug</option>')
    text = text.replace('>?? Nível de Pesca<', '>🎣️ Nível de Pesca<')
    text = text.replace('>?? Pokémon Capturados<', '>🎯️ Pokémon Capturados<')
    text = text.replace('>?? Clã</label>', '>⚔️ Clã</label>')
    text = text.replace('id="current-clan-icon">??</span>', 'id="current-clan-icon">⚔️</span>')

    # Boss/messages blocks
    text = text.replace("'Sunflora': { emoji: \"??\", icon: \"??\", msg: \"SUNFLORA EM COMBATE SOLAR!\",", "'Sunflora': { emoji: \"☀️\", icon: \"☀️\", msg: \"SUNFLORA EM COMBATE SOLAR!\",")
    text = text.replace("'Magcargo': { emoji: \"??\", icon: \"??\", msg: \"MAGCARGO INCINERANDO TUDO!\",", "'Magcargo': { emoji: \"♨️\", icon: \"♨️\", msg: \"MAGCARGO INCINERANDO TUDO!\",")
    text = text.replace("'Tyranitar': { emoji: \"??\", icon: \"??\", msg: \"TYRANITAR DEMOLINDO!\",", "'Tyranitar': { emoji: \"☠️\", icon: \"☠️\", msg: \"TYRANITAR DEMOLINDO!\",")
    text = text.replace("'Dragonair': { emoji: \"??\", icon: \"??\", msg: \"DRAGONAIR NADANDO!\",", "'Dragonair': { emoji: \"⚡️\", icon: \"⚡️\", msg: \"DRAGONAIR NADANDO!\",")
    text = text.replace('emoji: "??",\n\n\n\n                icon: "??",', 'emoji: "🎮️",\n\n\n\n                icon: "🎮️",')
    text = text.replace("'Tyranitar': { title: \"?? TYRANITAR DESPERTOU! ??\", emoji: \"??\", type: \"ROCHA\", threat: \"⚠️ EXTREMO\" }", "'Tyranitar': { title: \"☠️ TYRANITAR DESPERTOU! ☠️\", emoji: \"☠️\", type: \"ROCHA\", threat: \"⚠️ EXTREMO\" }")
    text = text.replace('title: `?? ${nextEvent.displayName.toUpperCase()} EM ALERTA! ??`,', 'title: `⚠️ ${nextEvent.displayName.toUpperCase()} EM ALERTA! ⚠️`,')
    text = text.replace('emoji: "??",\n\n\n\n                        title: `${nextEvent.displayName.toUpperCase()} EM ALERTA`,', 'emoji: "🎮️",\n\n\n\n                        title: `${nextEvent.displayName.toUpperCase()} EM ALERTA`,')
    text = text.replace("document.getElementById('boss-title').textContent = `?? ${boss.title}! ??`;", "document.getElementById('boss-title').textContent = `⚠️ ${boss.title}! ⚠️`;")

    # Admin/content/ranking/trainer card icons
    text = text.replace('>?? Food e Berries bloqueados</span>', '>⚠️ Food e Berries bloqueados</span>')
    text = text.replace('\\n\\n?? PREPARE-SE SEMPRE!`;', '\\n\\n⚔️⚔️ PREPARE-SE SEMPRE!`;')
    text = text.replace("'Tyranitar': { emoji: \"??\", title: \"TYRANITAR DESPERTOU\", type: \"ROCHA\", typeBadge: \"pokemon-type-rock\", threat: \"⚠️ EXTREMO\" },", "'Tyranitar': { emoji: \"☠️\", title: \"TYRANITAR DESPERTOU\", type: \"ROCHA\", typeBadge: \"pokemon-type-rock\", threat: \"⚠️ EXTREMO\" },")
    text = text.replace("${fb.type === 'bug' ? '?? Bug' : '?? Sugestão'}", "${fb.type === 'bug' ? '🐛️ Bug' : '💡️ Sugestão'}")
    text = text.replace('title="?? Clã ${clan.name}"', 'title="⚔️ Clã ${clan.name}"')
    text = text.replace('title="Exportar Dados">???</button>', 'title="Exportar Dados">📤️</button>')
    text = text.replace('<span class="pokeball-banner-icon">??</span>', '<span class="pokeball-banner-icon">🔴</span>')
    text = text.replace('>?? Personagens</p>', '>👥️ Personagens</p>')
    text = text.replace('>?? ${u.charCount} personagem${u.charCount !== 1 ? \'s\' : \'\'}</p>', '>👤️ ${u.charCount} personagem${u.charCount !== 1 ? \'s\' : \'\'}</p>')
    text = text.replace('<p class="font-black mb-1">?? Dica:</p>', '<p class="font-black mb-1">💡️ Dica:</p>')
    text = text.replace('>??? Armazenamento do Firestore:</p>', '>🗄️ Armazenamento do Firestore:</p>')
    text = text.replace('title="1º Lugar">??</span>', 'title="1º Lugar">🥇</span>')
    text = text.replace('title="2º Lugar">??</span>', 'title="2º Lugar">🥈</span>')
    text = text.replace('title="3º Lugar">??</span>', 'title="3º Lugar">🥉</span>')
    text = text.replace('>?? Pesca: ${char.fishingLevel || 0} ? ~~ ${char.pokemonCaught || 0}</p>', '>🎣️ Pesca: ${char.fishingLevel || 0} 🎯 ~~ ${char.pokemonCaught || 0}</p>')
    text = text.replace('>?? ${t.resetAt}: ${getNextAvailableText(cat, task.at)}</span>', '>⏰️ ${t.resetAt}: ${getNextAvailableText(cat, task.at)}</span>')
    text = text.replace('| ?? Clã: ${char.clan.toUpperCase()}', '| ⚔️ Clã: ${char.clan.toUpperCase()}')
    text = text.replace('title="Exportar Dados">??</button>', 'title="Exportar Dados">📤️</button>')
    text = text.replace('title="Editar Configurações">??</button>', 'title="Editar Configurações">✏️</button>')
    text = text.replace('title="Histórico">??</button>', 'title="Histórico">🕓️</button>')
    text = text.replace('title="${tStrings.finSet}">??</button>', 'title="${tStrings.finSet}">💵️</button>')

    # One remaining generic arsenal icon in src
    text = text.replace('<span class="text-lg">??</span>', '<span class="text-lg">⭐️</span>')

    return text


def process(path: str):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        data = f.read()
    before_fffd = data.count(FFFD)
    before_qq = data.count("??")

    data = apply_fixes(data)

    after_fffd = data.count(FFFD)
    after_qq = data.count("??")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(data)

    print(path)
    print(f"  U+FFFD: {before_fffd} -> {after_fffd}")
    print(f"  ??: {before_qq} -> {after_qq}")


if __name__ == "__main__":
    files = ["index.html", os.path.join("src", "index.html")]
    for file in files:
        if os.path.exists(file):
            process(file)
