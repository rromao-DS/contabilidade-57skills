# 57 Skills de Contabilidade para o Claude

57 skills para escritórios contábeis brasileiros, convertidas dos 57 subagentes originais (pasta do Google Drive) para o formato de **skill** do Claude.

## Como instalar no Claude

1. Baixe os zips de [`dist/`](dist/) (um por skill, ex.: `01-apuracao-simples-nacional.zip`).
2. No Claude: **Settings → Customize → Skills → "+" → Upload a skill** e envie o zip.
3. Repita para as skills que quiser usar.

Cada zip tem a estrutura exigida: `<nome>/SKILL.md`, com frontmatter YAML contendo apenas `name` e `description`.

## Estrutura do repositório

- `dist/` — 57 zips prontos para upload.
- `skills/<nome>/SKILL.md` — fonte de cada skill.
- `tools/convert_agent_to_skill.py` — converte um subagente (`.md` com `tools`/`model`) em skill.
- `tools/validate_skills.py` — valida os zips: `SKILL.md` presente, YAML válido, só `name` e `description`, `name` igual à pasta, descrição de até 1024 caracteres, sem nomes duplicados.
- `tools/short_descriptions.json` + `tools/apply_short_descriptions.py` — descrições resumidas para as 20 skills cujo texto original passava de 1024 caracteres. O texto original completo foi preservado no início do corpo de cada `SKILL.md`.

## Mudanças em relação aos agentes originais

- Removidos os campos `tools` e `model` do frontmatter (específicos de subagente).
- Removido `COMO-INSTALAR.md` (instruções de instalação de agentes).
- `name` normalizado para minúsculas e hífens, igual ao nome da pasta.
- Referências do tipo "chame 11-holerite" nas descrições resumidas passaram a usar o nome da skill (`holerite`).

## Avisos

Os resultados são rascunhos; o contador responsável deve revisar e assumir a responsabilidade técnica (CRC, Resolução CFC 1.546/2024). Licença original: uso permitido para clientes ASV Digital / Bravy; não redistribuir sem autorização.
