# Instalação, validação e reversão

## Compatibilidade

O baseline observado é Codex CLI 0.157.1. Nessa versão, `codex --help` descreve
`--profile` como uma camada `$CODEX_HOME/<nome>.config.toml`. O kit grava o perfil
`orchestration.config.toml`, carregado por `codex -p orchestration`.

Não convertimos silenciosamente para formatos antigos nem prometemos suporte
a todos os clientes desktop/IDE. Confira a versão e o help do seu cliente.
Se ele não reconhecer o perfil, use uma versão compatível antes de aplicar.
A [referência oficial](https://learn.chatgpt.com/docs/config-file/config-reference)
pode evoluir; o comportamento local testado é registrado separadamente.

Python 3.11+ é necessário por `tomllib`. Testes automatizados cobrem Linux e
macOS em Python 3.11/3.12. Windows não é alvo validado nesta primeira entrega.
Modelos e esforços precisam ser suportados pela conta e pelo runtime.

## Escolher o home

Recomendamos um home dedicado, como `$HOME/.codex-orchestration`. O argumento
`--home` é obrigatório para evitar alterar a instalação errada por acidente.
Não copie `auth.json`: autentique o home escolhido com `codex login`.

Se quiser instalar em um home existente, a prévia mostra quatro destinos e os
backups permitem restaurar os originais. O perfil principal `config.toml` não é
editado; arquivos de papéis de mesmo nome serão substituídos após backup.

O instalador recusa symlinks nos destinos e ancestrais, inclusive AGENTS.md
compartilhado. Escolha um home físico dedicado. Em macOS, caminhos como `/tmp`
podem ser symlinks; testes resolvem o diretório temporário físico. A recusa é
intencional para não alterar outro perfil ao seguir um link.

## Instalar e verificar

```sh
export KIT_CODEX_HOME="$HOME/.codex-orchestration"
python3 scripts/kit.py install --home "$KIT_CODEX_HOME"
python3 scripts/kit.py install --home "$KIT_CODEX_HOME" --apply
python3 scripts/kit.py doctor --home "$KIT_CODEX_HOME"
CODEX_HOME="$KIT_CODEX_HOME" codex --strict-config --help
CODEX_HOME="$KIT_CODEX_HOME" codex -p orchestration
```

`doctor` faz verificações estáticas locais. Ele não autentica, não chama modelos
e não certifica capacidade do modelo ou que um filho realmente executou.
`--strict-config --help` é uma verificação suplementar; isoladamente não prova
acesso a modelos nem comportamento da sessão. Não combine `--strict-config`
com `codex debug`: a versão observada recusa essa combinação.

Para inspecionar o contexto sem chamar modelos, a versão observada oferece
`codex debug prompt-input`. A saída pode conter instruções privadas: não publique
os logs. O catálogo de skills não prova a descoberta/execução dos agentes.

Para prova de execução, abra uma sessão nova e solicite uma investigação
inofensiva a `luna_explorer` ou um trabalho descartável a `sol_worker`. Inspecione
a atividade e a identidade efetiva do filho; a afirmação do agente não substitui
metadados. Isso consome uso normal do Codex e não é parte dos testes automáticos.

## Atualizar

Revise as mudanças do repositório, faça `git pull --ff-only` no seu checkout limpo
e execute novamente a prévia/install. Conteúdo já idêntico é no-op, sem outro
backup. Mudanças geram um novo backup antes da aplicação.

A atualização substitui os dois arquivos de papéis e o perfil; para customizar
IDs use as opções do instalador. Edições manuais nesses três arquivos devem ser
reconciliadas antes de reaplicar. AGENTS preserva bytes fora dos marcadores.

Não há daemon de atualização nem download automático. Mudança de versão do Codex
ou dos modelos exige revalidar o fluxo e, quando relevante, repetir o piloto.

## Reverter

A aplicação imprime `Backup: ...`. Guarde o caminho. Use o backup mais recente
correspondente à instalação que deseja desfazer:

```sh
python3 scripts/kit.py restore --home "$KIT_CODEX_HOME" \
  --backup "$KIT_CODEX_HOME/.orchestration-kit/backups/ID_DO_BACKUP"
python3 scripts/kit.py restore --home "$KIT_CODEX_HOME" \
  --backup "$KIT_CODEX_HOME/.orchestration-kit/backups/ID_DO_BACKUP" --apply
```

Sem `--apply`, a reversão é só prévia. O script valida home, allowlist dos destinos,
symlinks e hashes atuais antes de restaurar. Recupera bytes/modos originais;
remove somente arquivos que não existiam antes. Backups e diretórios podem
permanecer para auditoria; não são removidos recursivamente.

Se houver edições posteriores, a reversão é recusada para não destruí-las.
Compare manualmente o conteúdo com o manifesto privado e reconcilie o que deseja
preservar; não altere hashes para forçar a restauração. Atualizações sucessivas
podem ser desfeitas do backup mais recente ao mais antigo, respeitando os hashes.

Gravações são atômicas por arquivo e erros normais tentam restaurar a transação.
Uma interrupção abrupta do processo/energia ainda pode deixar estado parcial:
preserve o backup e compare os quatro destinos antes de continuar. Não execute
dois instaladores ao mesmo tempo no mesmo home; não há lock de concorrência.

## Diagnóstico

| Sintoma | Ação |
|---|---|
| `tomllib` não encontrado | Use Python 3.11 ou superior |
| Symlink recusado | Use home físico dedicado; não remova links pessoais às cegas |
| Markers inválidos em AGENTS | Reconcile o par begin/end; preserve instruções existentes |
| Modelo não disponível | Escolha ID autorizado e esforço suportado; não invente aliases |
| Perfil não reconhecido | Confira versão/help; formato de versões antigas não é suportado |
| Agente não delega | Confira sessão nova, papel e política; tarefas simples devem ser diretas |
| GSD continua instalado | Esperado: o kit não remove plugins/skills de terceiros |
| Restore recusa alterações | Preserve mudanças novas e reconcilie o backup manualmente |

## Limite entre configuração e garantia

Concorrência e sandbox são capacidades do runtime. Critérios de delegação,
contexto novo, uma tentativa de correção e continuidade até merge são instruções.
O kit não é um motor determinístico de workflow. Use gates externos (testes,
checks, regras de branch) para tornar requisitos críticos verificáveis.
