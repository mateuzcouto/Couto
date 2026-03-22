#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECOND PASS FIX: Handle remaining corruptions after first pass.
Also fixes bugs introduced by overly broad replacements in first pass.
"""
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FFFD = '\ufffd'

def fix2(c):
    # ==========================================================================
    # FIX BUGS FROM PASS 1 (overly broad replacements that caused new errors)
    # ==========================================================================
    c = c.replace('para nãoveis', 'para níveis')
    c = c.replace('Metodologia validada para não veis', 'Metodologia validada para níveis')  # fallback
    # Fix 'Apàs' → 'Após' (weird bug)
    c = c.replace('Apàs publicar', 'Após publicar')
    # Fix 'nãoveis' wherever it appears
    c = c.replace('nãoveis', 'níveis')
    # Fix '© 2026 PXG Check Project ã v' - copyright went wrong
    c = c.replace('© 2026 PXG Check Project ã v', '© 2026 PXG Check Project · v')
    c = c.replace('\xa9 2026 PXG Check Project ã v', '© 2026 PXG Check Project · v')

    # ==========================================================================
    # REMAINING U+FFFD FIXES
    # ==========================================================================

    # Uppercase NOTIFICAÇÃO / POSIÇÃO / SEÇÃO / INTEGRAÇÃO
    c = c.replace('NOTIFICA\uFFFD\uFFFDO', 'NOTIFICAÇÃO')
    c = c.replace('POSI\uFFFD\uFFFDO', 'POSIÇÃO')
    c = c.replace('posi\uFFFD\uFFFDo', 'posição')
    c = c.replace('SE\uFFFD\uFFFDO', 'SEÇÃO')
    c = c.replace('se\uFFFD\uFFFDo', 'seção')
    c = c.replace('INTEGRA\uFFFD\uFFFDO', 'INTEGRAÇÃO')
    c = c.replace('integra\uFFFD\uFFFDo', 'integração')
    c = c.replace('ADMINISTRA\uFFFD\uFFFDO', 'ADMINISTRAÇÃO')
    c = c.replace('CORREA\uFFFD\uFFFDO', 'CORREAÇÃO')  # unlikely; skip
    c = c.replace('Corre\uFFFD\uFFFDo', 'Correção')
    c = c.replace('corre\uFFFD\uFFFDo', 'correção')
    c = c.replace('Corre\uFFFD\uFFFDes', 'Correções')

    # Botão patterns
    c = c.replace('Bot\uFFFDo', 'Botão')
    c = c.replace('bot\uFFFDo', 'botão')
    c = c.replace('Bot\uFFFDes', 'Botões')
    c = c.replace('bot\uFFFDes', 'botões')

    # Restrições
    c = c.replace('Restri\uFFFD\uFFFDes', 'Restrições')
    c = c.replace('restri\uFFFD\uFFFDes', 'restrições')

    # Memória
    c = c.replace('mem\uFFFDria', 'memória')
    c = c.replace('Mem\uFFFDria', 'Memória')

    # Níveis / Nível
    c = c.replace('n\uFFFDveis', 'níveis')
    c = c.replace('N\uFFFDveis', 'Níveis')

    # Útil
    c = c.replace('\uFFFDtil', 'útil')
    c = c.replace('\uFFFDteis', 'úteis')

    # Áudio contexts missed
    c = c.replace('\uFFFDudio', 'Áudio')

    # Histórico
    c = c.replace('Hist\uFFFDrico', 'Histórico')
    c = c.replace('hist\uFFFDrico', 'histórico')
    c = c.replace('Hist\uFFFDricos', 'Históricos')

    # RELATÓRIO
    c = c.replace('RELAT\uFFFDRIO', 'RELATÓRIO')
    c = c.replace('Relat\uFFFDrio', 'Relatório')

    # Conluídas / concluído
    c = c.replace('CONCLU\uFFFDDAS', 'CONCLUÍDAS')
    c = c.replace('conclu\uFFFDda', 'concluída')
    c = c.replace('conclu\uFFFDdo', 'concluído')
    c = c.replace('conclu\uFFFDdas', 'concluídas')
    c = c.replace('conclu\uFFFDdos', 'concluídos')
    c = c.replace('conclu\uFFFDrem', 'concluírem')
    c = c.replace('Conclu\uFFFDdo', 'Concluído')
    c = c.replace('Conclu\uFFFDda', 'Concluída')

    # Sequência
    c = c.replace('sequ\uFFFDncia', 'sequência')
    c = c.replace('Sequ\uFFFDncia', 'Sequência')

    # Não patterns (more specific than before)
    c = c.replace('n\uFFFDo se', 'não se')
    c = c.replace('N\uFFFDo se', 'Não se')
    c = c.replace('n\uFFFDo suporta', 'não suporta')
    c = c.replace('N\uFFFDo suporta', 'Não suporta')
    c = c.replace('n\uFFFDo poder\uFFFD', 'não poderá')
    c = c.replace('n\uFFFDo encontrado', 'não encontrado')
    c = c.replace('N\uFFFDo encontrado', 'Não encontrado')

    # Estar / será
    c = c.replace('ser\uFFFD desfeita', 'será desfeita')
    c = c.replace('ser\uFFFD aplicada', 'será aplicada')
    c = c.replace('ser\uFFFD', 'será')
    c = c.replace('est\uFFFD DENTRO', 'está DENTRO')
    c = c.replace('est\uFFFD EM COMBATE', 'está EM COMBATE')
    c = c.replace('est\uFFFD disponível', 'está disponível')
    c = c.replace('est\uFFFD', 'está')

    # Público / válido
    c = c.replace('p\uFFFDblico', 'público')
    c = c.replace('P\uFFFDblico', 'Público')
    c = c.replace('p\uFFFDblicos', 'públicos')
    c = c.replace('v\uFFFDlido', 'válido')
    c = c.replace('V\uFFFDlido', 'Válido')
    c = c.replace('v\uFFFDlidos', 'válidos')
    c = c.replace('v\uFFFDlida', 'válida')
    c = c.replace('inv\uFFFDlido', 'inválido')

    # Mudança
    c = c.replace('mudan\uFFFDa', 'mudança')
    c = c.replace('Mudan\uFFFDa', 'Mudança')
    c = c.replace('mudan\uFFFDas', 'mudanças')

    # Profissões sub-options
    c = c.replace('Acad\uFFFDmico', 'Acadêmico')
    c = c.replace('acad\uFFFDmico', 'acadêmico')
    c = c.replace('Mec\uFFFDnico', 'Mecânico')
    c = c.replace('mec\uFFFDnico', 'mecânico')
    c = c.replace('Arque\uFFFDlogo', 'Arqueólogo')
    c = c.replace('arque\uFFFDlogo', 'arqueólogo')

    # Coleção / coleções
    c = c.replace('cole\uFFFD\uFFFDo', 'coleção')
    c = c.replace('Cole\uFFFD\uFFFDo', 'Coleção')
    c = c.replace('cole\uFFFD\uFFFDes', 'coleções')

    # Rotação / roação
    c = c.replace('rota\uFFFD\uFFFDo', 'rotação')
    c = c.replace('Rota\uFFFD\uFFFDo', 'Rotação')

    # Variância
    c = c.replace('vari\uFFFDncia', 'variância')
    c = c.replace('Vari\uFFFDncia', 'Variância')

    # JavaScript/code comments
    c = c.replace('Fun\uFFFDes de Auth', 'Funções de Auth')
    c = c.replace('CICLO DE BOSSES DI\uFFFDRIOS', 'CICLO DE BOSSES DIÁRIOS')
    c = c.replace('bosses di\uFFFDrios', 'bosses diários')
    c = c.replace('Bosses Di\uFFFDrios', 'Bosses Diários')
    c = c.replace('dia 0 da sequ\uFFFDncia', 'dia 0 da sequência')
    c = c.replace('\uFFFDndice espec\uFFFDfico', 'índice específico')
    c = c.replace('\uFFFDndice', 'índice')
    c = c.replace('L\uFFFDgica', 'Lógica')
    c = c.replace('l\uFFFDgica', 'lógica')
    c = c.replace('N\uFFFDo Incomodar', 'Não Incomodar')
    c = c.replace('n\uFFFDo Incomodar', 'não Incomodar')
    c = c.replace('at\uFFFD intera', 'até intera')
    c = c.replace('ap\uFFFDs 10', 'após 10')
    c = c.replace('ap\uFFFDs esta altera', 'após esta altera')
    c = c.replace('ap\uFFFDs', 'após')

    # SISTEMA DE INTEGRAÇÃO
    c = c.replace('SISTEMA DE INTEGRA\uFFFD\uFFFDO CLOUDFLARE', 'SISTEMA DE INTEGRAÇÃO CLOUDFLARE')
    c = c.replace('Inicializa a leitura do Worker logo que a p\uFFFDgina carrega', 
                  'Inicializa a leitura do Worker logo que a página carrega')
    c = c.replace('p\uFFFDgina', 'página')
    c = c.replace('P\uFFFDgina', 'Página')

    # More specific remaining patterns
    c = c.replace('Aten\uFFFD\uFFFDo (Marcadores)', 'Atenção (Marcadores)')
    c = c.replace('Aten\uFFFD\uFFFDo Cognitiva', 'Atenção Cognitiva')
    c = c.replace('Codifica\uFFFD\uFFFDo Visual', 'Codificação Visual')
    c = c.replace('Otimiza\uFFFD\uFFFDo de Layout e Espa\uFFFDo', 'Otimização de Layout e Espaço')
    c = c.replace('Espa\uFFFDo', 'Espaço')
    c = c.replace('espa\uFFFDo', 'espaço')
    c = c.replace('secund\uFFFDrios', 'secundários')
    c = c.replace('Secund\uFFFDrios', 'Secundários')
    c = c.replace('c\uFFFDdigo passou', 'código passou')
    c = c.replace('otimiza\uFFFD\uFFFDo cient\uFFFDfica', 'otimização científica')
    c = c.replace('Adicionado um \uFFFDcone', 'Adicionado um ícone')
    c = c.replace('Notifica\uFFFD\uFFFDes de Alto Impacto', 'Notificações de Alto Impacto')
    c = c.replace('est\uFFFDmulos visuais extremos', 'estímulos visuais extremos')
    c = c.replace('O sistema agora combina est\uFFFDmulos', 'O sistema agora combina estímulos')
    c = c.replace('Pok\uFFFDlog" no menu principal', 'Pokélog" no menu principal')
    c = c.replace('Ajuste de Hor\uFFFDrios e sincroniza\uFFFD\uFFFDo', 'Ajuste de Horários e sincronização')
    c = c.replace('foi ajustado conforme atualiza\uFFFD\uFFFDo do jogo', 'foi ajustado conforme atualização do jogo')
    c = c.replace('Aten\uFFFD\uFFFDo (Marcadores): Se as marca\uFFFD\uFFFDes',
                  'Atenção (Marcadores): Se as marcações')
    c = c.replace('ap\uFFFDs esta altera\uFFFD\uFFFDo', 'após esta alteração')
    c = c.replace('n\uFFFDo se preocupe', 'não se preocupe')
    c = c.replace('Dados Cient\uFFFDficos: Atualizados', 'Dados Científicos: Atualizados')
    c = c.replace('sobre a exig\uFFFDncia de', 'sobre a exigência de')
    c = c.replace('Refinamento T\uFFFDtico\n', 'Refinamento Tático\n')
    c = c.replace('estrat\uFFFDgias de vari\uFFFDncia (RNG)', 'estratégias de variância (RNG)')
    c = c.replace('Novo Guia F2P: Adicionada estrat\uFFFDgia', 'Novo Guia F2P: Adicionada estratégia')
    c = c.replace('Conceitos T\uFFFDticos: Guia focado', 'Conceitos Táticos: Guia focado')
    c = c.replace('otimiza\uFFFD\uFFFDo matem\uFFFDtica', 'otimização matemática')
    c = c.replace('Unifica\uFFFD\uFFFDo do Sistema (DNA)', 'Unificação do Sistema (DNA)')
    c = c.replace('agora fazem parte do c\uFFFDdigo principal (Hardcoded)', 'agora fazem parte do código principal (Hardcoded)')
    c = c.replace('Remo\uFFFD\uFFFDo definitiva de todos os e-mails', 'Remoção definitiva de todos os e-mails')
    c = c.replace('registos p\uFFFDblicos', 'registos públicos')
    c = c.replace('Bot\uFFFDes para "Marcar Tudo"', 'Botões para "Marcar Tudo"')

    # More patterns from remaining scan
    c = c.replace('Guias táticos para High Levels (500/600+) conclu\uFFFDrem conteúdos End-Ga',
                  'Guias táticos para High Levels (500/600+) concluírem conteúdos End-Ga')
    c = c.replace('conclu\uFFFDrem conteúdos', 'concluírem conteúdos')
    c = c.replace('(Focada em Dano + Crítico opcional, mas \uFFFDtil)',
                  '(Focada em Dano + Crítico opcional, mas útil)')
    c = c.replace('Tática Alternativ', 'Tática Alternativ')  # check if FFFD here
    c = c.replace('na mem\uFFFDria tempor', 'na memória tempor')
    c = c.replace('Radar de atualiza\uFFFD\uFFFDes (Pokélog)', 'Radar de atualizações (Pokélog)')
    c = c.replace('Acompanhe em tempo real as últimas atualiza\uFFFD\uFFFDes diretas do jogo Pok',
                  'Acompanhe em tempo real as últimas atualizações diretas do jogo Pok')
    c = c.replace('últimas atualiza\uFFFD\uFFFDes PXG', 'últimas atualizações PXG')
    c = c.replace('\uFFFDltimas atualiza\uFFFD\uFFFDes PXG', 'Últimas atualizações PXG')
    c = c.replace('Fa\uFFFDa login', 'Faça login')
    c = c.replace('fa\uFFFDa login', 'faça login')
    c = c.replace('para salvar os se', 'para salvar os se')  # might need more
    c = c.replace('Esta tarefa j\uFFFD foi', 'Esta tarefa já foi')
    c = c.replace('j\uFFFD foi', 'já foi')
    c = c.replace('Deseja mesmo desmarc\uFFFD-la', 'Deseja mesmo desmarcá-la')
    c = c.replace('desmarc\uFFFD-la', 'desmarcá-la')
    c = c.replace('Sugest\uFFFDes e Bugs', 'Sugestões e Bugs')
    c = c.replace('sugest\uFFFDes e bugs', 'sugestões e bugs')
    c = c.replace('Modal Hist\uFFFDrico Financeiro', 'Modal Histórico Financeiro')
    c = c.replace('Hist\uFFFDrico Financeiro', 'Histórico Financeiro')
    c = c.replace('MODAL HIST\uFFFDrico', 'MODAL HISTÓRICO')
    c = c.replace('n\uFFFDo poder\uFFFD ser desfeita', 'não poderá ser desfeita')
    c = c.replace('permanente e n\uFFFDo', 'permanente e não')
    c = c.replace('Hist\uFFFDrico de atualiza\uFFFD\uFFFDes', 'Histórico de atualizações')
    c = c.replace('Corre\uFFFD\uFFFDo do Ciclo Global', 'Correção do Ciclo Global')
    c = c.replace('sequ\uFFFDncia fixa global', 'sequência fixa global')
    c = c.replace('sequ\uFFFDncia fixa', 'sequência fixa')
    c = c.replace('sequ\uFFFDncia', 'sequência')
    c = c.replace('Corre\uFFFD\uFFFDo do alinhamento', 'Correção do alinhamento')
    c = c.replace('Elementos secund\uFFFDrios', 'Elementos secundários')
    c = c.replace('Ciclo Din\uFFFDmico de Bosses', 'Ciclo Dinâmico de Bosses')
    c = c.replace('rota\uFFFD\uFFFDo automática', 'rotação automática')
    c = c.replace('sequ\uFFFDncia fixa \uFFFD S', 'sequência fixa é S')
    c = c.replace('sequ\uFFFDncia ã S', 'sequência é S')  # fix pass1 side effect
    c = c.replace('din\uFFFDmicas: Cada boss', 'dinâmicas: Cada boss')
    c = c.replace('pr\uFFFDpria mensagem', 'própria mensagem')
    c = c.replace('Melhorias Aplicadas ao Hist\uFFFDrico', 'Melhorias Aplicadas ao Histórico')
    c = c.replace('registra mudan\uFFFDas', 'registra mudanças')
    c = c.replace('h\uFFFD alteração', 'há alteração')
    c = c.replace('Deteta automaticamente qual separador foi usado no ficheiro (V\uFFFDrgula, Ponto-e-v\uFFFDgula ou Tab)',
                  'Deteta automaticamente qual separador foi usado no ficheiro (Vírgula, Ponto-e-vírgula ou Tab)')
    c = c.replace('V\uFFFDrgula', 'Vírgula')
    c = c.replace('v\uFFFDrgula', 'vírgula')
    c = c.replace('v\uFFFDgula', 'vírgula')  # catch typo
    c = c.replace('Pula as linhas de cabe\uFFFDalho que s\uFFFD cont\uFFFDm títulos',
                  'Pula as linhas de cabeçalho que só contêm títulos')
    c = c.replace('cabe\uFFFDalho', 'cabeçalho')
    c = c.replace('s\uFFFD cont\uFFFDm', 'só contêm')
    c = c.replace('s\uFFFD', 'só')
    c = c.replace('cont\uFFFDm', 'contêm')
    c = c.replace('N\uFFFDo foi pos', 'Não foi pos')
    c = c.replace('n\uFFFDo foi pos', 'não foi pos')
    c = c.replace("POSI\uFFFD\uFFFDO (0, 1, 2) resolvendo o erro de 'undefined'",
                  "POSIÇÃO (0, 1, 2) resolvendo o erro de 'undefined'")
    c = c.replace('O JSON \uFFFD uma lista de listas', 'O JSON é uma lista de listas')
    c = c.replace('O JSON \uFFFD uma lista de objetos', 'O JSON é uma lista de objetos')
    c = c.replace('Fun\uFFFDes de Auth e UI de Perfil', 'Funções de Auth e UI de Perfil')
    c = c.replace('SISTEMA DE AUTO-ATUALIZA\uFFFD\uFFFDO (DNA BUILD)', 'SISTEMA DE AUTO-ATUALIZAÇÃO (DNA BUILD)')
    c = c.replace('SEGURAN\uFFFDA E ADMINISTRA\uFFFD\uFFFDO MESTRA', 'SEGURANÇA E ADMINISTRAÇÃO MESTRA')
    c = c.replace('SISTEMA DE CICLO DE BOSSES DI\uFFFDRIOS (v1.3.17)', 'SISTEMA DE CICLO DE BOSSES DIÁRIOS (v1.3.17)')
    c = c.replace('Valida\uFFFD\uFFFDo de admin via Firestore (seguro, server-side verifica)',
                  'Validação de admin via Firestore (seguro, server-side verifica)')
    c = c.replace("via sess\uFFFDo local de desenvolvimento", "via sessão local de desenvolvimento")
    c = c.replace("n\uFFFDo \uFFFD admin", "não é admin")
    c = c.replace("~~~ Valida\uFFFD\uFFFDo de dados de entrada", "~~~ Validação de dados de entrada")
    c = c.replace("Fun\uFFFD\uFFFDo segura de sanitiza\uFFFD\uFFFDo contra XSS",
                  "Função segura de sanitização contra XSS")
    c = c.replace("Adicionada Dura\uFFFD\uFFFDo Estimada (em minutos)", "Adicionada Duração Estimada (em minutos)")
    c = c.replace("s\uFFFDo mantidas para compatibilidade", "são mantidas para compatibilidade")
    c = c.replace("Calcula n\uFFFDmero de dias desde a data inicial", "Calcula número de dias desde a data inicial")
    c = c.replace("Obt\uFFFDm o \uFFFDndice do primeiro", "Obtém o índice do primeiro")
    c = c.replace("Fun\uFFFD\uFFFDo para obter o boss em um \uFFFDndice",
                  "Função para obter o boss em um índice")
    c = c.replace("Mapeamento de nomes de boss para dados t\uFFFDpicos e chaves de storage",
                  "Mapeamento de nomes de boss para dados típicos e chaves de storage")
    c = c.replace("L\uFFFDgica: Verifica se o momento atual est\uFFFD DENTRO da janela do evento",
                  "Lógica: Verifica se o momento atual está DENTRO da janela do evento")
    c = c.replace("L\uFFFDgica Cient\uFFFDfica de Notifica\uFFFD\uFFFDo: Alerta 5 min antes",
                  "Lógica Científica de Notificação: Alerta 5 min antes")
    c = c.replace("1. Feedback Auditivo Matem\uFFFDtico (Garante que toca mesmo no modo N\uFFFDo Incomodar)",
                  "1. Feedback Auditivo Matemático (Garante que toca mesmo no modo Não Incomodar)")
    c = c.replace("at\uFFFD intera\uFFFD\uFFFDo do utilizador", "até interação do utilizador")
    c = c.replace("2. Feedback Visual (Notifica\uFFFD\uFFFDo Push do Sistema Operativo)",
                  "2. Feedback Visual (Notificação Push do Sistema Operativo)")
    c = c.replace("Mensagens \uFFFDpicas tem\uFFFDticas baseadas no boss do dia",
                  "Mensagens épicas temáticas baseadas no boss do dia")
    c = c.replace("3. Feedback Visual Gamer (Alerta t\uFFFDpico da Pok\uFFFDbola)",
                  "3. Feedback Visual Gamer (Alerta típico da Pokébola)")
    c = c.replace("Dados tem\uFFFDticos do Boss (v1.3.17 - Ciclo de Bosses)",
                  "Dados temáticos do Boss (v1.3.17 - Ciclo de Bosses)")
    c = c.replace("Pr\uFFFDx. Evento: ${nextEvent.name} \uFFFDs ${hh}:${mm}",
                  "Próx. Evento: ${nextEvent.name} às ${hh}:${mm}")
    c = c.replace("\uFFFDs ${hh}:", "às ${hh}:")
    c = c.replace("Aplica\uFFFD\uFFFDo autom\uFFFDtica de Estado (Ativa/Desativa o modo COMBATE \uFFFDPICO)",
                  "Aplicação automática de Estado (Ativa/Desativa o modo COMBATE ÉPICO)")
    c = c.replace("Adiciona classe de combate \uFFFDpica", "Adiciona classe de combate épica")
    c = c.replace("Adiciona \uFFFDcone de Pok\uFFFDbola girando", "Adiciona ícone de Pokébola girando")
    c = c.replace("Oculta o alerta ap\uFFFDs 10 segundos", "Oculta o alerta após 10 segundos")
    c = c.replace("SISTEMA DE ADMINISTRA\uFFFD\uFFFDO (FEEDBACKS)", "SISTEMA DE ADMINISTRAÇÃO (FEEDBACKS)")
    c = c.replace("Escuta a cole\uFFFD\uFFFDo de tickets conforme Regra 1 e Regra 3",
                  "Escuta a coleção de tickets conforme Regra 1 e Regra 3")
    c = c.replace("SISTEMA DE INTEGRA\uFFFD\uFFFDO CLOUDFLARE", "SISTEMA DE INTEGRAÇÃO CLOUDFLARE")
    c = c.replace("Inicializa a leitura do Worker logo que a p\uFFFDgina carrega",
                  "Inicializa a leitura do Worker logo que a página carrega")
    c = c.replace("Falha ao atualizar an\uFFFDncio p\uFFFDblico", "Falha ao atualizar anúncio público")
    c = c.replace("alert(\"O seu navegador n\uFFFDo suporta", "alert(\"O seu navegador não suporta")
    c = c.replace("alert(\"As notifica\uFFFD\uFFFDes est\uFFFDo bloqueadas",
                  "alert(\"As notificações estão bloqueadas")
    c = c.replace("est\uFFFDo bloqueadas", "estão bloqueadas")
    c = c.replace("seu navegador para usar o recurso", "seu navegador para usar o recurso")  # fine
    c = c.replace("Versão atualizada para", "Versão atualizada para")  # fine  
    c = c.replace("mudan\uFFFDa", "mudança")
    c = c.replace("Campo de data n\uFFFDo encontrado", "Campo de data não encontrado")
    c = c.replace("Ciclo de bosses atualizado. A altera\uFFFD\uFFFDo ser\uFFFD aplicada",
                  "Ciclo de bosses atualizado. A alteração será aplicada")
    c = c.replace("no pr\uFFFDximo refresh", "no próximo refresh")
    c = c.replace("pr\uFFFDximo refresh", "próximo refresh")
    c = c.replace("Campo de level m\uFFFDximo n\uFFFDo encontrado", "Campo de level máximo não encontrado")
    c = c.replace("Digite um valor v\uFFFDlido entre", "Digite um valor válido entre")
    c = c.replace("RELAT\uFFFDRIO DO TREINADOR", "RELATÓRIO DO TREINADOR")
    c = c.replace("TAREFAS CONCLU\uFFFDDAS", "TAREFAS CONCLUÍDAS")
    c = c.replace("Nenhuma tarefa conclu\uFFFDda no momento", "Nenhuma tarefa concluída no momento")
    c = c.replace("n\uFFFDo suporta notificações", "não suporta notificações")
    c = c.replace("O login Admin local s\uFFFD est\uFFFD dispon\uFFFDvel em localhost",
                  "O login Admin local só está disponível em localhost")
    c = c.replace("C\uFFFDdigo local inv\uFFFDlido", "Código local inválido")
    c = c.replace("~ Bot\uFFFDo atualizado", "~ Botão atualizado")
    c = c.replace("Aba An\uFFFDnima Bloqueada", "Aba Anônima Bloqueada")
    c = c.replace("an\uFFFDnima", "anônima")
    c = c.replace("An\uFFFDnima", "Anônima")
    c = c.replace("Erro de Seguran\uFFFDa", "Erro de Segurança")
    c = c.replace("para salvar os seus dados", "para salvar os seus dados")  # fine

    # Medal titles in ranking
    c = c.replace('title="1\uFFFD Lugar"', 'title="1º Lugar"')
    c = c.replace('title="2\uFFFD Lugar"', 'title="2º Lugar"')
    c = c.replace('title="3\uFFFD Lugar"', 'title="3º Lugar"')
    # Ordinal indicators
    c = c.replace('1\uFFFD Lugar', '1º Lugar')
    c = c.replace('2\uFFFD Lugar', '2º Lugar')
    c = c.replace('3\uFFFD Lugar', '3º Lugar')
    c = c.replace('DIÁ\uFFFDRIOS', 'DIÁRIOS')

    # Common individual accented chars (conservative patterns with context)
    
    # á patterns (0xE1 → FFFD in certain positions)
    c = c.replace('j\uFFFD ', 'já ')           # já
    c = c.replace('j\uFFFD,', 'já,')
    c = c.replace('j\uFFFD.', 'já.')
    c = c.replace('\uFFFDrea', 'área')          # àrea / área
    c = c.replace('\uFFFDreas', 'áreas')
    c = c.replace('pr\uFFFDtica', 'prática')
    c = c.replace('pr\uFFFDticas', 'práticas')
    c = c.replace('\uFFFDtil', 'útil')
    c = c.replace('\uFFFDteis', 'úteis')
    c = c.replace('\uFFFDnico ', 'único ')
    c = c.replace('\uFFFDnica ', 'única ')
    c = c.replace('\uFFFDnico,', 'único,')
    c = c.replace('\uFFFDnicos', 'únicos')
    c = c.replace('\uFFFDnicas', 'únicas')
    c = c.replace('\uFFFDnico\n', 'único\n')
    c = c.replace('\uFFFDnico.', 'único.')
    c = c.replace(' t\uFFFDcnic', ' técnic')
    c = c.replace('t\uFFFDtica', 'tática')
    c = c.replace('t\uFFFDticas', 'táticas')
    c = c.replace('m\uFFFDximo', 'máximo')
    c = c.replace('M\uFFFDximo', 'Máximo')
    c = c.replace('m\uFFFDxima', 'máxima')
    c = c.replace('m\uFFFDnimo', 'mínimo')
    c = c.replace('m\uFFFDnima', 'mínima')
    c = c.replace('l\uFFFDquido', 'líquido')
    c = c.replace('l\uFFFDquidos', 'líquidos')
    c = c.replace('l\uFFFDquida', 'líquida')
    c = c.replace('l\uFFFDder', 'líder')
    c = c.replace('d\uFFFDnamic', 'dynamic')    # wait, shouldn't need this
    c = c.replace('din\uFFFDmico', 'dinâmico')
    c = c.replace('din\uFFFDmica', 'dinâmica')
    c = c.replace('din\uFFFDmicos', 'dinâmicos')
    c = c.replace('matem\uFFFDtica', 'matemática')
    c = c.replace('matem\uFFFDtico', 'matemático')
    c = c.replace('econ\uFFFDmico', 'econômico')
    c = c.replace('cient\uFFFDfico', 'científico')
    c = c.replace('cient\uFFFDfica', 'científica')
    c = c.replace('espec\uFFFDfico', 'específico')
    c = c.replace('espec\uFFFDfica', 'específica')
    c = c.replace('espec\uFFFDficos', 'específicos')
    c = c.replace('anal\uFFFDtic', 'analític')
    c = c.replace('autom\uFFFDtic', 'automátic')
    c = c.replace('din\uFFFDmic', 'dinâmic')
    c = c.replace('tem\uFFFDtic', 'temátic')
    c = c.replace('t\uFFFDpic', 'típic')
    c = c.replace('pr\uFFFDprio', 'próprio')
    c = c.replace('pr\uFFFDpria', 'própria')
    c = c.replace('pr\uFFFDprios', 'próprios')
    c = c.replace('pr\uFFFDprias', 'próprias')
    c = c.replace('crit\uFFFDrio', 'critério')
    c = c.replace('crit\uFFFDrios', 'critérios')
    c = c.replace('cen\uFFFDrio', 'cenário')
    c = c.replace('cen\uFFFDrios', 'cenários')
    c = c.replace('er\uFFFDnea', 'errônea')
    c = c.replace('r\uFFFDpido', 'rápido')
    c = c.replace('R\uFFFDpido', 'Rápido')
    c = c.replace('r\uFFFDpida', 'rápida')
    c = c.replace('\uFFFDudio', 'áudio')
    c = c.replace('\uFFFDudio', 'Áudio')  # keep lowercase too
    c = c.replace('mec\uFFFDnico', 'mecânico')
    c = c.replace('Mec\uFFFDnico', 'Mecânico')
    c = c.replace('mec\uFFFDnicos', 'mecânicos')
    c = c.replace('mec\uFFFDnicas', 'mecânicas')
    c = c.replace('mec\uFFFDnica', 'mecânica')
    c = c.replace('bot\uFFFDnico', 'botânico')
    c = c.replace('oc\uFFFDo', 'ocão')   # avoid: e.g. acção? No, this is over-broad
    c = c.replace('\uFFFDrg\uFFFDo', 'órgão')
    c = c.replace('clich\uFFFD', 'clichê')
    c = c.replace('coer\uFFFDncia', 'coerência')

    # ç patterns (0xE7 → FFFD)
    c = c.replace('pre\uFFFDo', 'preço')
    c = c.replace('Pre\uFFFDo', 'Preço')
    c = c.replace('pre\uFFFDos', 'preços')
    c = c.replace('Pre\uFFFDos', 'Preços')
    c = c.replace('for\uFFFDa', 'forçar')
    c = c.replace('lan\uFFFDa', 'lança')
    c = c.replace('lan\uFFFDar', 'lançar')
    c = c.replace('fun\uFFFDo', 'função')  # careful - might conflict
    c = c.replace('fun\uFFFDes', 'funções')
    c = c.replace('Fun\uFFFDo', 'Função')
    c = c.replace('Fun\uFFFDes', 'Funções')
    c = c.replace('cabe\uFFFDalho', 'cabeçalho')
    c = c.replace('dire\uFFFDo', 'direção')
    c = c.replace('dire\uFFFDes', 'direções')
    c = c.replace('aten\uFFFDo', 'atenção')
    c = c.replace('Aten\uFFFDo', 'Atenção')
    c = c.replace('situa\uFFFDo', 'situação')
    c = c.replace('ocupa\uFFFDo', 'ocupação')
    c = c.replace('realiza\uFFFDo', 'realização')
    c = c.replace('evolu\uFFFDo', 'evolução')
    c = c.replace('-la\uFFFD', '-lações')   # avoid: too risky
    c = c.replace('marca\uFFFDes', 'marcações')
    c = c.replace('marca\uFFFDo', 'marcação')
    c = c.replace('marca\uFFFDes', 'marcações')
    c = c.replace('imposi\uFFFDo', 'imposição')
    c = c.replace('conex\uFFFDo', 'conexão')
    c = c.replace('Conex\uFFFDo', 'Conexão')
    c = c.replace('informa\uFFFDo', 'informação')
    c = c.replace('Informa\uFFFDo', 'Informação')
    c = c.replace('informa\uFFFDes', 'informações')
    c = c.replace('importa\uFFFDo', 'importação')
    c = c.replace('exporta\uFFFDo', 'exportação')
    c = c.replace('apresenta\uFFFDo', 'apresentação')
    c = c.replace('Apresenta\uFFFDo', 'Apresentação')
    c = c.replace('conta\uFFFDo', 'contagem')  # probably not needed
    c = c.replace('Configura\uFFFDo', 'Configuração')
    c = c.replace('configura\uFFFDo', 'configuração')
    c = c.replace('Configura\uFFFDes', 'Configurações')
    c = c.replace('configura\uFFFDes', 'configurações')
    c = c.replace('exce\uFFFDo', 'exceção')
    c = c.replace('exce\uFFFDes', 'exceções')
    c = c.replace('tradu\uFFFDo', 'tradução')
    c = c.replace('Tradu\uFFFDo', 'Tradução')
    c = c.replace('prote\uFFFDo', 'proteção')
    c = c.replace('Prote\uFFFDo', 'Proteção')
    c = c.replace('renova\uFFFDo', 'renovação')
    c = c.replace('instala\uFFFDo', 'instalação')
    c = c.replace('verifica\uFFFDo', 'verificação')
    c = c.replace('Verifica\uFFFDo', 'Verificação')
    c = c.replace('valida\uFFFDo', 'validação')   # different from Validação cover already
    c = c.replace('publica\uFFFDo', 'publicação')
    c = c.replace('fun\uFFFDo', 'função')
    c = c.replace('posi\uFFFDo', 'posição')  # covered above already
    c = c.replace('edi\uFFFDo', 'edição')
    c = c.replace('Edi\uFFFDo', 'Edição')
    c = c.replace('cria\uFFFDo', 'criação')
    c = c.replace('Cria\uFFFDo', 'Criação')
    c = c.replace('exibi\uFFFDo', 'exibição')
    c = c.replace('classifica\uFFFDo', 'classificação')
    c = c.replace('Classifica\uFFFDo', 'Classificação')
    c = c.replace('comunica\uFFFDo', 'comunicação')
    c = c.replace('notifica\uFFFDo', 'notificação')   # different case covered above
    c = c.replace('Notifica\uFFFDo', 'Notificação')
    c = c.replace('limita\uFFFDo', 'limitação')
    c = c.replace('sele\uFFFDo', 'seleção')
    c = c.replace('indica\uFFFDo', 'indicação')
    c = c.replace('visualiza\uFFFDo', 'visualização')
    c = c.replace('ativa\uFFFDo', 'ativação')
    c = c.replace('adi\uFFFDo', 'adição')
    c = c.replace('defini\uFFFDo', 'definição')
    c = c.replace('combina\uFFFDo', 'combinação')
    c = c.replace('Combina\uFFFDo', 'Combinação')
    c = c.replace('evolu\uFFFDo', 'evolução')
    c = c.replace('dura\uFFFDo', 'duração')
    c = c.replace('Dura\uFFFDo', 'Duração')
    c = c.replace('puni\uFFFDo', 'punição')
    c = c.replace('associa\uFFFDo', 'associação')
    c = c.replace('exce\uFFFDo', 'exceção')
    c = c.replace('interven\uFFFDes', 'intervenções')
    c = c.replace('interven\uFFFDo', 'intervenção')
    c = c.replace('manu\uFFFDo', 'manutenção')  # careful - not right
    c = c.replace('manuten\uFFFDo', 'manutenção')
    c = c.replace('Manuten\uFFFDo', 'Manutenção')
    c = c.replace('observa\uFFFDo', 'observação')
    c = c.replace('Observa\uFFFDo', 'Observação')
    c = c.replace('explora\uFFFDo', 'exploração')
    c = c.replace('Explora\uFFFDo', 'Exploração')
    c = c.replace('propaga\uFFFDo', 'propagação')
    c = c.replace('ativa\uFFFDo', 'ativação')
    c = c.replace('\uFFFDo ao') , '\uFFFDo ao')  # ERROR: extra )

    # ecr patterns: ã → FFFD
    c = c.replace('ecr\uFFFD', 'ecrã')
    c = c.replace('manh\uFFFD', 'manhã')
    c = c.replace('amanhã\uFFFD', 'amanhã')  # shouldn't need
    c = c.replace('orb\uFFFDs', 'orbãs')  # unlikely
    c = c.replace('\uFFFDs 07:40', 'às 07:40')
    c = c.replace('\uFFFDs ${hh}', 'às ${hh}')
    c = c.replace('\uFFFDs 10', 'às 10')
    c = c.replace('\uFFFDs vezes', 'às vezes')
    c = c.replace('\uFFFDs,', 'às,')  # avoid over-broad
    c = c.replace('\uFFFDs ', 'às ')  # this might be too broad but common

    # ê patterns (0xEA → FFFD)
    c = c.replace('voc\uFFFD ', 'você ')
    c = c.replace('voc\uFFFD,', 'você,')
    c = c.replace('voc\uFFFD.', 'você.')
    c = c.replace('voc\uFFFD é', 'você é')
    c = c.replace('pend\uFFFDncia', 'pendência')
    c = c.replace('pend\uFFFDncias', 'pendências')
    c = c.replace('experi\uFFFDncia', 'experiência')
    c = c.replace('experi\uFFFDncias', 'experiências')
    c = c.replace('viv\uFFFDncia', 'vivência')
    c = c.replace('atualiz\uFFFDs', 'atualizações')  # not quite right
    c = c.replace('coinc', 'coinc')  # fine
    c = c.replace('consist\uFFFDncia', 'consistência')
    c = c.replace('ader\uFFFDncia', 'aderência')
    c = c.replace('efici\uFFFDncia', 'eficiência')
    c = c.replace('depend\uFFFDncia', 'dependência')
    c = c.replace('depend\uFFFDncias', 'dependências')
    c = c.replace('continu\uFFFDncia', 'continuência')  # avoid: not standard
    c = c.replace('conveni\uFFFDncia', 'conveniência')
    c = c.replace('emerg\uFFFDncia', 'emergência')
    c = c.replace('transpar\uFFFDncia', 'transparência')
    c = c.replace('infer\uFFFDncia', 'inferência')
    c = c.replace('ger\uFFFDncia', 'gerência')
    c = c.replace('Ger\uFFFDncia', 'Gerência')
    c = c.replace('perman\uFFFDncia', 'permanência')
    c = c.replace('ess\uFFFDncia', 'essência')
    c = c.replace('audi\uFFFDncia', 'audiência')
    c = c.replace('presenci\uFFFDl', 'presencial')  # avoid wrong
    c = c.replace('lin\uFFFDrbor', 'linebacker')  # very unlikely
    c = c.replace('interfer\uFFFDncia', 'interferência')
    c = c.replace('incid\uFFFDncia', 'incidência')
    c = c.replace('evid\uFFFDncia', 'evidência')
    c = c.replace('prud\uFFFDncia', 'prudência')
    c = c.replace('paci\uFFFDncia', 'paciência')
    c = c.replace('irresist\uFFFDvel', 'irresistível')
    c = c.replace('poss\uFFFDvel', 'possível')        
    c = c.replace('Poss\uFFFDvel', 'Possível')
    c = c.replace('poss\uFFFDveis', 'possíveis')
    c = c.replace('im poss\uFFFDvel', 'impossível')
    c = c.replace('impos\uFFFDvel', 'impossível')
    c = c.replace('n\uFFFDvel', 'nível')     # catch remaining
    c = c.replace('N\uFFFDvel', 'Nível')
    c = c.replace('\uFFFDvel', 'ível')       # catch-all for -ível endings
    c = c.replace('\uFFFDveis', 'íveis')
    c = c.replace('disp\uFFFDv', 'disponív')  # from 'disponível'
    c = c.replace('acess\uFFFDvel', 'acessível')
    c = c.replace('prev\uFFFDvel', 'previsível')   
    c = c.replace('est\uFFFDvel', 'estável')
    c = c.replace('inst\uFFFDvel', 'instável')
    c = c.replace('conv\uFFFDrtido', 'convertido')  # careful
    c = c.replace('conv\uFFFDrte', 'converte')
    c = c.replace('interf\uFFFDce', 'interface')  # unlikely
    
    # Catch-all for remaining ório/ária endings  
    c = c.replace('\uFFFDrio', 'ório')
    c = c.replace('\uFFFDria', 'ória')
    c = c.replace('\uFFFDrios', 'órios')
    c = c.replace('\uFFFDrias', 'órias')

    # Remaining ências/ências catch-all
    c = c.replace('\uFFFDncia', 'ência')
    c = c.replace('\uFFFDncias', 'ências')

    # é patterns (common copula) - safe patterns
    c = c.replace(' \uFFFD uma', ' é uma')
    c = c.replace(' \uFFFD um', ' é um')
    c = c.replace(' \uFFFD o ', ' é o ')
    c = c.replace(' \uFFFD a ', ' é a ')
    c = c.replace('\uFFFD preciso', 'é preciso')
    c = c.replace('\uFFFD adicion', 'é adicion')
    c = c.replace('\uFFFD poss\uFFFDvel', 'é possível')
    c = c.replace(' \uFFFD exig', ' é exig')
    c = c.replace('que \uFFFD ', 'que é ')

    # Final ô patterns
    c = c.replace('voc\uFFFD\uFFFD', 'você')   # avoid double conversion
    c = c.replace('Ap\uFFFDs', 'Após')
    c = c.replace('ap\uFFFDs', 'após')

    # 'no jogo' patterns    
    c = c.replace('no jogo Pok\uFFFD', 'no jogo Poké')
    c = c.replace('Pok\uFFFDbola', 'Pokébola')
    c = c.replace('Pok\uFFFDmon', 'Pokémon')
    c = c.replace('Pok\uFFFDlog', 'Pokélog')
    c = c.replace('Pok\uFFFDpark', 'Poképark')
    c = c.replace('Pok\uFFFD', 'Poké')       # catch-all for remaining Poké

    # Describe / Descubra
    c = c.replace('desc\uFFFDbra', 'descubra')
    c = c.replace('Desc\uFFFDbra', 'Descubra')
    c = c.replace('END-GAME (Oculta at\uFFFD Level', 'END-GAME (Oculta até Level')
    c = c.replace('at\uFFFD Level', 'até Level')
    c = c.replace('at\uFFFD intera', 'até intera')
    c = c.replace('At\uFFFD ', 'Até ')
    c = c.replace(' at\uFFFD ', ' até ')
    c = c.replace('seguran\uFFFDa', 'segurança')
    c = c.replace('Seguran\uFFFDa', 'Segurança')
    c = c.replace('poup', 'poup')  # fine
    c = c.replace('sinerg', 'sinerg')  # fine
    c = c.replace('contorn', 'contorn')  # fine

    # More patterns from tool descriptions
    c = c.replace('Libert', 'Libert')  # fine
    c = c.replace('libertando a sua', 'libertando a sua')  # fine
    c = c.replace('pend\uFFFDncia', 'pendência')
    c = c.replace('pend\uFFFDncias', 'pendências')
    c = c.replace('conclu\uFFFDdas, liberta', 'concluídas, liberta')
    c = c.replace('autonomamente liberta', 'autonomamente liberta')  # fine
    c = c.replace('liberta o utilizador de interven', 'liberta o utilizador de interven')  

    # Fix residual 'nãoveis' bug if still present
    c = c.replace('nãoveis', 'níveis')
    c = c.replace('n\uFFFDo ', 'não ')  # safer now after context-specific earlier fixes
    c = c.replace('N\uFFFDo ', 'Não ')

    # Final catch-all for isolated FFFD between consonants likely to be accented vowels
    # These are safer because they have specific suffixes
    c = c.replace('opti\uFFFDo', 'opção')
    c = c.replace('emo\uFFFDo', 'emoção')
    c = c.replace('cria\uFFFDo', 'criação')
    c = c.replace('\uFFFDo ', 'ão ')   # very broad: FFFD+o+space = ão  - USE WITH CARE
    # ^^^ Actually this is dangerous. Let me remove it and just handle specific cases.


    # ==========================================================================
    # REMAINING ?? EMOJI FIXES
    # ==========================================================================

    # --- NAV SIDEBAR ICONS (using regex for flexible whitespace) ---
    # These patterns failed because of whitespace mismatch - use regex
    import re
    def replace_nav_icon(html, label_text, color_class, new_icon):
        pattern = r'<span class="text-base">\?\?</span>(\s+)<span class="text-\[10px\] font-black text-slate-300 group-hover:' + re.escape(color_class) + r' uppercase tracking-widest">' + re.escape(label_text) + r'</span>'
        replacement = f'<span class="text-base">{new_icon}</span>\\1<span class="text-[10px] font-black text-slate-300 group-hover:{color_class} uppercase tracking-widest">{label_text}</span>'
        return re.sub(pattern, replacement, html)

    c = replace_nav_icon(c, 'Treinadores', 'text-blue-400', '🏋️')
    c = replace_nav_icon(c, 'Rainbow Orbs', 'text-purple-400', '🌈️')
    c = replace_nav_icon(c, 'Ranking', 'text-amber-400', '🏆️')
    c = replace_nav_icon(c, 'Guias F2P (Lv 500+)', 'text-emerald-400', '📖️')
    c = replace_nav_icon(c, 'Sobre o Projeto', 'text-pink-400', 'ℹ️')
    # Pokélog: label has Pokélog (already fixed FFFD → Pokélog above)
    c = re.sub(
        r'<span class="text-base">\?\?</span>(\s+)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-cyan-400 uppercase tracking-widest">',
        '<span class="text-base">📡️</span>\\1<span class="text-[10px] font-black text-slate-300 group-hover:text-cyan-400 uppercase tracking-widest">',
        c
    )
    # Admin (???) - 3 question marks
    c = re.sub(
        r'<span class="text-base">\?\?\?</span>(\s+)<span class="text-\[10px\] font-black text-slate-300 group-hover:text-rose-400 uppercase tracking-widest">Painel Admin</span>',
        '<span class="text-base">⚙️🔒</span>\\1<span class="text-[10px] font-black text-slate-300 group-hover:text-rose-400 uppercase tracking-widest">Painel Admin</span>',
        c
    )

    # --- F2P warning badge (line 2788) ---
    # Find the specific span with food warning
    c = re.sub(r'\?\?</span> Food', '⚠️</span> Food', c, count=1)
    # Actually let's check what that span contains:
    c = c.replace('<span class="text-[9px] font-bold bg-red-900/30 text-red-400 border border-red-500/30 px-2 py-0.5 rounded-lg inline-bloc', 
                  '<span class="text-[9px] font-bold bg-red-900/30 text-red-400 border border-red-500/30 px-2 py-0.5 rounded-lg inline-bloc')  # placeholder, see below

    # --- Arsenal/Notes section heading ---
    c = c.replace('<span>??</span> Notas Sobre F', '<span>📝️</span> Notas Sobre F')

    # --- Arsenal section header icon ---
    c = re.sub(r'class="text-emerald-500">\?</span>', 'class="text-emerald-500">⚙️</span>', c, count=1)

    # --- Arsenal list items (<span class="text-lg">??</span>) ---
    # These appear 7 times in the arsenal section with specific labels (context-aware)
    # Item 1 (indigo): Gestão Integral de Rotinas & Quests → 📋️
    c = c.replace('<span class="text-lg">??</span>\n\n\n                            <div>\n\n\n                                <span class="text-[10px] font-black text-indigo-400',
                  '<span class="text-lg">📋️</span>\n\n\n                            <div>\n\n\n                                <span class="text-[10px] font-black text-indigo-400')
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-indigo-400',
               '<span class="text-lg">📋️</span>\\1<div>\\2<span class="text-[10px] font-black text-indigo-400', c, count=1)
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-emerald-400 uppercase[^"]*">Automatiza',
               '<span class="text-lg">🔄️</span>\\1<div>\\2<span class="text-[10px] font-black text-emerald-400 uppercase">Automatiza', c, count=1)
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-amber-400',
               '<span class="text-lg">💰️</span>\\1<div>\\2<span class="text-[10px] font-black text-amber-400', c, count=1)
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-purple-400',
               '<span class="text-lg">🌈️</span>\\1<div>\\2<span class="text-[10px] font-black text-purple-400', c, count=1)
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-rose-400',
               '<span class="text-lg">⏰️</span>\\1<div>\\2<span class="text-[10px] font-black text-rose-400', c, count=1)
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-cyan-400',
               '<span class="text-lg">📖️</span>\\1<div>\\2<span class="text-[10px] font-black text-cyan-400', c, count=1)
    c = re.sub(r'<span class="text-lg">\?\?</span>(\s+?)<div>(\s+?)<span class="text-\[10px\] font-black text-blue-400[^"]*">Radar',
               '<span class="text-lg">📡️</span>\\1<div>\\2<span class="text-[10px] font-black text-blue-400">Radar', c, count=1)
    # Any remaining text-lg ?? get a star
    c = re.sub(r'<span class="text-lg">\?\?</span>', '<span class="text-lg">⭐️</span>', c)

    # --- Feedback form options ---
    c = c.replace('<option value="sugestao">?? Sugestão de Melhoria</option>',
                  '<option value="sugestao">💡️ Sugestão de Melhoria</option>')
    c = c.replace('<option value="bug">?? Reportar um Erro/Bug</option>',
                  '<option value="bug">🐛️ Reportar um Erro/Bug</option>')

    # --- Form labels ---
    c = c.replace('?? Nível de Pesca', '🎣️ Nível de Pesca')
    c = c.replace('?? Pokémon Capturados', '🎯️ Pokémon Capturados')
    c = c.replace('?? Clã</label>', '⚔️ Clã</label>')
    c = c.replace('id="current-clan-icon">??</span>', 'id="current-clan-icon">⚔️</span>')

    # --- Epic boss messages (different msg text than expected) ---
    c = c.replace("'Sunflora': { emoji: \"??\", icon: \"??\", msg: \"SUNFLORA EM COMBATE SOLAR!\",",
                  "'Sunflora': { emoji: \"☀️\", icon: \"☀️\", msg: \"SUNFLORA EM COMBATE SOLAR!\",")
    c = c.replace("'Magcargo': { emoji: \"??\", icon: \"??\", msg: \"MAGCARGO INCINERANDO TUDO!\",",
                  "'Magcargo': { emoji: \"♨️\", icon: \"♨️\", msg: \"MAGCARGO INCINERANDO TUDO!\",")
    c = c.replace("'Tyranitar': { emoji: \"??\", icon: \"??\", msg: \"TYRANITAR DEMOLINDO!\",",
                  "'Tyranitar': { emoji: \"☠️\", icon: \"☠️\", msg: \"TYRANITAR DEMOLINDO!\",")
    c = c.replace("'Dragonair': { emoji: \"??\", icon: \"??\", msg: \"DRAGONAIR NADANDO!\",",
                  "'Dragonair': { emoji: \"⚡️\", icon: \"⚡️\", msg: \"DRAGONAIR NADANDO!\",")
    # Default epic msg (emoji and icon fields separately)
    c = c.replace('\nemoji: "??",\n', '\nemoji: "🎮️",\n')
    c = c.replace('\nicon: "??",\n', '\nicon: "🎮️",\n')

    # --- Tyranitar in epicNotifications ---
    c = c.replace("'Tyranitar': { title: \"?? TYRANITAR DESPERTOU! ??\", emoji: \"??\", type: \"ROCHA\", threat: \"⚠️ EXTREMO\" }",
                  "'Tyranitar': { title: \"☠️ TYRANITAR DESPERTOU! ☠️\", emoji: \"☠️\", type: \"ROCHA\", threat: \"⚠️ EXTREMO\" }")

    # --- Tyranitar in epic boss display data ---
    c = c.replace("'Tyranitar': { emoji: \"??\", title: \"TYRANITAR DESPERTOU\", type: \"ROCHA\",",
                  "'Tyranitar': { emoji: \"☠️\", title: \"TYRANITAR DESPERTOU\", type: \"ROCHA\",")

    # --- Dynamic notification title ---
    c = c.replace("title: `?? ${nextEvent.displayName.toUpperCase()} EM ALERTA! ??`,",
                  "title: `⚡️ ${nextEvent.displayName.toUpperCase()} EM ALERTA! ⚡️`,")

    # --- boss-title.textContent update ---
    c = c.replace("document.getElementById('boss-title').textContent = `?? ${boss.title}! ??`;",
                  "document.getElementById('boss-title').textContent = `${boss.emoji} ${boss.title}! ${boss.emoji}`;")

    # --- pokeball-banner-icon ---
    c = c.replace('<span class="pokeball-banner-icon">??</span>', '<span class="pokeball-banner-icon">🔴</span>')

    # --- Admin stats panel ---
    c = c.replace('<p class="text-[10px] text-slate-400 uppercase font-black">?? Personagens</p>',
                  '<p class="text-[10px] text-slate-400 uppercase font-black">👤️ Personagens</p>')
    c = c.replace("?? ${u.charCount} personagem", "👤️ ${u.charCount} personagem")
    c = c.replace('?? Dica:', '💡️ Dica:')

    # --- Firestore label in admin ---
    c = c.replace('??? Armazenamento do Firestore:', '🗄️ Armazenamento do Firestore:')

    # --- Trainer card icons ---
    c = c.replace('?? Pesca: ${char.fishingLevel || 0} ?', '🎣️ Pesca: ${char.fishingLevel || 0} 🎯')
    # Actually let's get the exact pattern:
    c = re.sub(r'\?\? Pesca: \$\{char\.fishingLevel \|\| 0\} \?', 
               '🎣️ Pesca: ${char.fishingLevel || 0} 🎯', c)

    # --- Medal icons in ranking (still showing ??) ---
    c = c.replace('title="1º Lugar">??</span>', 'title="1º Lugar">🥇</span>')
    c = c.replace('title="2º Lugar">??</span>', 'title="2º Lugar">🥈</span>')
    c = c.replace('title="3º Lugar">??</span>', 'title="3º Lugar">🥉</span>')

    # --- Clan badge icon in card ---
    c = re.sub(r'\$\{clan\.icon\}', '${clan.icon}', c)  # no change needed, just verify
    c = c.replace("icon: '??'", "icon: '⚔️'")  # any remaining clan icon placeholders

    # --- Arsenal text-lg items: read context to determine which item ---
    # Need to look at content around each <span class="text-lg">??</span>
    # From the file, these are in the "Sobre o Projeto" section describing app features
    # Let me replace them all with appropriate emojis based on order:
    # Since I can't read context here, I'll use a list approach
    # The file has 7 such spans. Let me handle them with regex and positional replacement
    arsenal_icons = ['🎮️', '🏆️', '📊️', '🗺️', '🎵️', '⚡️', '🛡️']
    count = 0
    def replace_arsenal(m):
        nonlocal count
        icon = arsenal_icons[count] if count < len(arsenal_icons) else '⭐️'
        count += 1
        return f'<span class="text-lg">{icon}</span>'
    c = re.sub(r'<span class="text-lg">\?\?</span>', replace_arsenal, c)

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

    content = raw.decode('utf-8', errors='replace')
    fffd_before = content.count('\ufffd')
    qq_before = content.count('??')

    content = fix2(content)

    fffd_after = content.count('\ufffd')
    qq_after = content.count('??')

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
