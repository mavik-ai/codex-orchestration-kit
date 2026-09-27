# Codex Orchestration Kit

[![CI](https://github.com/mavik-ai/codex-orchestration-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/mavik-ai/codex-orchestration-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Coordenação Astra, implementação Sol e investigação Luna — com contexto
 delimitado, instalação reversível e entrega baseada em evidências.**

Um kit de configuração e instruções para os subagentes nativos do Codex. Não é
um novo runtime, scheduler, servidor MCP ou ferramenta de auto-merge. Funciona
sem copiar seus projetos, credenciais ou histórico e sem instalar frameworks.
Documentação principal em português do Brasil.

> **Economia não é garantida.** No piloto inicial de uma tarefa pequena, Astra
> sozinho foi mais rápido que a equipe. O kit prefere execução direta em tarefas
> simples e reserva delegação para trabalho cujo escopo justifique coordenação.
> [Veja os dados e as limitações](docs/EVALUATION.md).

## Por que existe

Delegar tudo aumenta coordenação, pode duplicar contexto e criar conflito de
edição. Concentrar tudo no modelo mais forte também pode ser desnecessário.
Este kit torna explícitos os critérios para escolher entre as duas opções:

| Papel | Configuração inicial | Responsabilidade |
|---|---|---|
| Coordenador | `gpt-6-astra`, esforço `low` | Definir escopo, resolver decisões materiais e revisar a entrega |
| `sol_worker` | `gpt-6-sol`, esforço `medium` | Implementar ou depurar uma tarefa com arquivos definidos |
| `luna_explorer` | `gpt-6-luna`, esforço `high`, somente leitura | Investigar uma pergunta delimitada e devolver evidências |

Os IDs são configuráveis e dependem de acesso na sua conta. Esforço de raciocínio
é uma configuração inicial, não prova de capacidade nem garantia de menor custo.
Há no máximo **dois filhos**, além do coordenador. Sem delegação recursiva por
instrução; limite de concorrência pelo runtime.

## Início rápido

Requisitos: Git, Python **3.11+**, Codex CLI compatível com o formato de perfis da
versão **0.157.1** e acesso aos modelos escolhidos. O instalador funciona offline;
o uso posterior do Codex exige sua própria autenticação e pode consumir quota.

```sh
git clone https://github.com/mavik-ai/codex-orchestration-kit.git
cd codex-orchestration-kit

# Home dedicado evita interferir em outras sessões/perfis.
export KIT_CODEX_HOME="$HOME/.codex-orchestration"

# Primeiro: apenas prévia. Nenhum arquivo é criado.
python3 scripts/kit.py install --home "$KIT_CODEX_HOME"

# Aplicar e guardar o caminho do backup mostrado.
python3 scripts/kit.py install --home "$KIT_CODEX_HOME" --apply
python3 scripts/kit.py doctor --home "$KIT_CODEX_HOME"

# Autenticação separada, realizada pelo próprio Codex.
CODEX_HOME="$KIT_CODEX_HOME" codex login
CODEX_HOME="$KIT_CODEX_HOME" codex -p orchestration
```

Abra uma sessão nova depois de instalar. A versão observada carrega
`orchestration.config.toml` usando `-p orchestration`; **não é necessário copiar
seu conteúdo para config.toml**. Clientes antigos podem usar formatos diferentes:
consulte [compatibilidade e operação](docs/OPERATIONS.md).

### Outros modelos

```sh
python3 scripts/kit.py install --home "$KIT_CODEX_HOME" \
  --coordinator SEU_MODELO_COORDENADOR \
  --worker SEU_MODELO_EXECUTOR \
  --explorer SEU_MODELO_INVESTIGADOR
```

Inspecione a prévia e repita com `--apply` para gravar. Substituir IDs não valida
compatibilidade com esforços `low/medium/high` nem acesso real; verifique no
Codex. Os nomes dos papéis permanecem `sol_worker` e `luna_explorer` por serem
referências estáveis da política, mesmo que os modelos sejam substituídos.

## O que é instalado

```text
CODEX_HOME/
├── orchestration.config.toml       # perfil selecionado por -p orchestration
├── agents/
│   ├── sol-worker.toml             # executor
│   └── luna-explorer.toml          # investigador somente leitura
├── AGENTS.md                      # somente um bloco gerenciado pelo kit
└── .orchestration-kit/backups/     # originais e hashes para reversão
```

O instalador preserva `config.toml`, autenticação, sessões, plugins e instruções
fora do bloco gerenciado. Arquivos de papéis com os mesmos nomes são substituídos
com backup. A prévia lista os destinos; revise também os [templates](templates).

**Limite importante:** o perfil de modelo é opt-in, mas `agents/` e `AGENTS.md`
têm alcance no CODEX_HOME, inclusive em sessões sem `-p orchestration`. Para
isolamento completo, use um home dedicado. Destinos com symlinks são recusados;
o kit não segue silenciosamente links para configurações compartilhadas.

## Como usar

Pedido pequeno: descreva a correção e deixe o agente executar diretamente.
Pedido complexo: forneça objetivo e critérios de aceite; a política solicita
investigação e implementação delimitadas quando úteis.

Exemplo de autorização do ciclo completo:

> Implemente a correção da issue N. Está autorizado seguir até o merge: branch,
> testes, commit, push, PR, CI verde no HEAD atual e revisão. Não faça deploy.

A autorização vale para aquele escopo, sem reconfirmar as etapas já autorizadas.
Não dispensa checks ou proteções. O kit não concede credenciais nem executa
merge sozinho. [Fluxo e fronteiras de autorização](docs/WORKFLOW.md).

## Documentação

| Documento | O que você encontra |
|---|---|
| [Arquitetura](docs/ARCHITECTURE.md) | Componentes, fluxo, contexto e limites reais de enforcement |
| [Decisões técnicas](docs/DECISIONS.md) | Motivação, alternativas e trade-offs das escolhas |
| [Operação](docs/OPERATIONS.md) | Instalação, perfis, diagnóstico, atualização e reversão |
| [Fluxo de entrega](docs/WORKFLOW.md) | Discovery, SDD/TDD, issue, branch, CI e merge |
| [Integrações](docs/INTEGRATIONS.md) | MAVIK, Superpowers, GSD e GitHub sem dependências implícitas |
| [Avaliação](docs/EVALUATION.md) | Dados do piloto, metodologia e o que ainda não foi provado |
| [Segurança](SECURITY.md) | Credenciais, backups, permissões e relato de vulnerabilidades |
| [Especificação](docs/SPEC.md) | Contrato testável da primeira entrega |
| [Contribuição](CONTRIBUTING.md) | Desenvolvimento, testes e revisão |
| [Changelog](CHANGELOG.md) | Histórico das mudanças |

## Desenvolvimento

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
```

Os testes usam diretórios temporários e não chamam modelos nem precisam de
credenciais. CI executa Linux/macOS e Python 3.11/3.12. O checker verifica links
locais, templates TOML e padrões comuns de conteúdo privado; não é auditoria
exaustiva de segurança. Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença e independência

[MIT](LICENSE). Este projeto não é um produto oficial da OpenAI. MAVIK,
Superpowers e GSD são integrações opcionais, não são redistribuídos e mantêm suas
próprias licenças. O kit pode ser usado sem qualquer um deles.
