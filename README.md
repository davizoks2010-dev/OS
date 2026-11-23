# Agent OS

Sistema operacional pessoal do Davi, focado em produção de software e sistemas, gestão de empresa e criação de negócios: vault Markdown (Obsidian) + roteador de 3 níveis (regras locais → API em nuvem → Claude Code headless) + painel FastAPI local + automações no Agendador de Tarefas do Windows. **Nenhuma IA roda localmente.**

## Requisitos
Windows 10/11, Python 3.11+, Git, Obsidian, Claude Code (`claude login` com assinatura Pro/Max), ~4 GB de RAM livres e internet.

## Instalação (PowerShell)
```powershell
git clone <url-do-repo-privado> C:\Users\Davi\AgentOS
cd C:\Users\Davi\AgentOS
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env      # preencha GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
.venv\Scripts\python -m system.config   # confere a configuração (não mostra segredos)
```
No Obsidian: **Abrir pasta como cofre** → `C:\Users\Davi\AgentOS\vault`.

## Estrutura
- `CLAUDE.md` — regras globais lidas pelo Claude Code
- `vault/` — `raw/`, `wiki/` (inclui `negocios/`), `projetos/`, `outputs/` (inclui `metricas/*.json`), `logs/`, `skills/`
- `system/` — `config.py`, `bridge/` (coleta, Telegram, custos, agendamentos), `router/` (3 níveis), `panel/` (FastAPI)

## Status da construção
- [x] Bloco 1 — Vault + CLAUDE.md + configuração base
- [ ] Bloco 2 — Coletor local + 3 primeiras skills + skill-creator
- [ ] Bloco 3 — Automações + Telegram + controle de custo
- [ ] Bloco 4 — Roteador de 3 níveis
- [ ] Bloco 5 — Painel web (8 abas)
- [ ] Bloco 6 — 13 skills restantes + validação ponta a ponta

## Catálogo de skills (20)
| Pilar | Skills |
|---|---|
| Software e sistemas | ideia-para-spec, status-dos-projetos, planejar-sprint, criar-projeto, revisar-codigo, gerar-testes, triagem-de-bugs, documentar-projeto, changelog-e-release |
| Gestão de empresa | revisao-semanal-da-empresa, ata-de-reuniao, proposta-para-cliente, controle-financeiro, criar-sop |
| Criação de negócios | **validar-ideia-de-negocio**, **modelo-de-negocio**, **analise-de-mercado** |
| Pesquisa e rotina | video-para-sistema, resumo-da-manha |
| Sistema | skill-creator |
