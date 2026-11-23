# CLAUDE.md — Agent OS do Davi (Software, Empresa & Pesquisa)

Você é o arquiteto e executor do Agent OS pessoal do Davi. Toda saída voltada ao usuário deve ser em **português do Brasil**, no fuso horário de **Brasília (America/Sao_Paulo, BRT)**.

## 1. Mapa do Vault e Onde Salvar Cada Coisa
- `vault/raw/<area>/`: Entradas brutas (transcrições, CSVs, briefings, logs de erro). **Nunca edite ou apague arquivos em `raw/`.**
- `vault/wiki/<categoria>/`: Conhecimento vivo e reutilizável (`empresa/`, `produtos/`, `projetos/`, `processos/`, `clientes/`, `ferramentas/`, `pessoal/`). Atualize notas existentes antes de criar duplicatas.
- `vault/projetos/<nome-do-projeto>/`: Estado vivo de cada software (`README.md`, `roadmap.md`, `decisoes.md`, `status.md`). A mesa Solana é tratada apenas como um projeto aqui dentro.
- `vault/outputs/specs/`: PRDs e especificações técnicas.
- `vault/outputs/relatorios/`: Relatórios diários, técnicos, semanais da empresa e financeiros.
- `vault/outputs/propostas/` e `vault/outputs/atas/`: Entregas comerciais e atas de reunião.
- `vault/outputs/metricas/`: JSONs estruturados lidos pelo painel web.
- `vault/skills/<nome>/SKILL.md`: Instruções reutilizáveis de cada skill.

## 2. Convenções de Nomes, Datas e Links
- **Datas:** Sempre ISO `YYYY-MM-DD` (timestamps `YYYY-MM-DD HH:MM BRT`).
- **Nomes de arquivo:** Apenas `kebab-case` (minúsculas, números e hífens, sem espaços ou acentos). Ex.: `2026-11-22-spec-painel-v2.md`, `sop-deploy-api.md`.
- **Wikilinks:** Use `[[nome-do-arquivo]]` ou `[[pasta/nome-do-arquivo|Rótulo]]` para conectar specs, projetos, atas, clientes e SOPs.

## 3. Registro de Pedidos
Todo pedido processado pela ponte ou painel deve acrescentar uma linha em `vault/logs/pedidos/YYYY-MM-DD.md`:
`- [HH:MM BRT] | Nível <1/2/3> | Origem: <painel/cli/voz/agenda> | Pedido: "<texto>" | Saída: [[caminho/do/arquivo]]`

## 4. Regras de Segurança e Limites Absolutos (NUNCA FAZER)
1. **ZERO DINHEIRO REAL E CARTEIRAS:** Nunca manipule chaves privadas, carteiras cripto, assinaturas de transação ou operações financeiras reais. Projetos como a mesa Solana permanecem estritamente em modo simulação/desenvolvimento.
2. **ZERO SEGREDOS NO VAULT:** Nunca escreva chaves de API, senhas ou tokens em `vault/`, `outputs/` ou `logs/`. Leia segredos apenas de `.env`.
3. **ZERO EXCLUSÃO SEM CONFIRMAÇÃO:** Nunca apague arquivos em `wiki/`, `projetos/`, `raw/` ou repositórios de código sem confirmação explícita do Davi.
4. **MUDANÇAS DE CÓDIGO SEGURAS:** Ao revisar ou corrigir código nos repositórios locais, rode a suíte de testes antes de concluir e não faça push/deploy automático sem aprovação.
5. **ECONOMIA DE CRÉDITOS:** Leia apenas os arquivos estritamente necessários para a skill em execução.

## 5. Frontmatter YAML das Notas
Toda nota criada ou atualizada em `vault/` (exceto `raw/` e `logs/`) começa com:
```yaml
---
title: "Título objetivo da nota"
date: YYYY-MM-DD
area: software | empresa | clientes | financeiro | pesquisa | pessoal | sistema
tags: [tag1, tag2]
status: ativo | pendente | concluido | arquivado
---
```
Código, nomes de variáveis, chaves YAML e mensagens de commit usam inglês técnico; todo texto voltado ao Davi é pt-BR.
