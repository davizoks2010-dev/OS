# Agent OS

Sistema operacional pessoal do Davi: vault Markdown (Obsidian) + roteador de 3 níveis + painel local + automações no Windows.

## Instalação (Windows)
```powershell
git clone <url-do-repo-privado> C:\Users\Davi\AgentOS
cd C:\Users\Davi\AgentOS
copy .env.example .env   # preencha os valores
```
No Obsidian: **Abrir pasta como cofre** → `C:\Users\Davi\AgentOS\vault`.

## Estrutura
- `CLAUDE.md` — regras globais (lidas pelo Claude Code)
- `vault/` — raw, wiki, projetos, outputs, logs, skills
- `system/` — router, bridge, panel, voice

Construção por blocos; veja o histórico de commits.
