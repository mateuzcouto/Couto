# PXG Check

Projeto estatico HTML/CSS/JS com Firebase e foco em seguranca, performance e manutencao.

## Estrutura Atual
- `index.html`: shell principal com referencias externas e metadados de seguranca
- `src/styles.css`: estilos da aplicacao (externalizado)
- `src/app.js`: logica principal do app (externalizado)
- `src/analytics.js`: bootstrap do Google Analytics (externalizado)
- `_headers`: headers de seguranca/cache para deploy estatico (Cloudflare/Netlify)
- `.github/copilot-instructions.md`: checklist de setup

## Hardening Aplicado
- CSP ativa sem `unsafe-inline` em `script-src`
- `Referrer-Policy` restritiva
- eventos inline removidos do HTML (`onclick`, `oninput`, `onchange`, `onerror`)
- event delegation por `data-action` no JS
- wrappers seguros de `localStorage` e parse JSON
- sanitizacao para conteudo dinamico renderizado
- debounce para buscas
- lazy load de orbs

## Deploy (Checklist Rapido)
1. Publicar a raiz do projeto como site estatico.
2. Garantir que o host respeita o arquivo `_headers`.
3. Confirmar que `https://www.gstatic.com` e Firebase endpoints estao liberados na CSP.
4. Revisar regras do Firestore/Auth para bloquear abusos de escrita publica.
5. Validar no navegador de producao:
	- login Google
	- leitura/escrita de personagens
	- carregamento de Orbs e Pokelog
	- envio de feedback

## Observacao de Infra
- O arquivo `_headers` adiciona politicas de seguranca e cache no servidor.
- Se o provedor nao suportar `_headers`, replique as mesmas diretivas na configuracao do host/CDN.

## Firestore Rules (Aplicar Agora)
Arquivos criados:
- `firestore.rules`
- `firebase.json`

Passo a passo no Firebase Console:
1. Acesse Firebase Console > Build > Firestore Database > Rules.
2. Abra o arquivo `firestore.rules` deste projeto.
3. Copie todo o conteudo e cole na aba Rules do console.
4. Clique em Publish.
5. Teste no app:
	- usuario logado/anonimo deve conseguir CRUD apenas dos proprios personagens
	- feedback deve aceitar apenas `type` = `sugestao` ou `bug`
	- feedback com texto menor que 8 ou maior que 1000 deve falhar
	- leitura/exclusao de feedbacks deve ficar restrita ao admin com email `mateuscouto27@gmail.com`
