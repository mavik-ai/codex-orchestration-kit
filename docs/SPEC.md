# SPEC-001 — Kit público de orquestração

Status: contrato aprovado pelo pedido de publicação; issue #1.

## Objetivo

Distribuir o modelo de trabalho Astra/Sol/Luna como configuração opt-in do Codex,
com documentação técnica, sem copiar o ambiente privado que originou o piloto.

## Contrato

- Python 3.11+ e biblioteca padrão; nenhuma chamada de modelo pelo instalador.
- CLI: `python3 scripts/kit.py install --home PATH [--apply]`, `doctor --home PATH`,
  `restore --home PATH --backup PATH [--apply]`.
- install suporta `--coordinator`, `--worker`, `--explorer` para IDs de modelos;
  padrões gpt-6-astra, gpt-6-sol e gpt-6-luna. Não assumir acesso por conta.
- Destinos: orchestration.config.toml, agents/sol-worker.toml,
  agents/luna-explorer.toml, bloco delimitado em AGENTS.md.
- Perfil nomeado: `codex -p orchestration`; não sobrescrever config.toml,
  auth.json, sessões, regras ou plugins. Papéis e AGENTS são visíveis no mesmo
  CODEX_HOME mesmo sem selecionar perfil; documentar esse limite.
- Sem --apply, somente prévia, sem criar diretórios ou backups.
- Validar TOML e paths antes de escrever; recusar symlinks nos destinos e
  diretórios ancestrais controlados para não alterar outros perfis sem intenção.
- Backup privado com manifesto antes de alterações; restaurar conteúdo original
  ou ausência original, recusando divergência posterior por hash e path inseguro.
- Reaplicação idêntica é no-op. Erros não devem deixar instalação parcialmente
  aplicada sem rollback ou diagnóstico recuperável.
- doctor verifica arquivos/markers/modelos/limites locais; não promete acesso a
  modelos nem validação de execução real.
- Templates de instruções distinguem política de linguagem natural de limites
  impostos pelo runtime. Até dois filhos; sem recursão por instrução.
- Exemplos e dados públicos não contêm caminhos de usuário nem IDs de sessão.

## Gates

Testes de round-trip, preservação, dry-run, idempotência, divergência posterior,
paths/symlinks, JSON/TOML, links Markdown locais e conteúdo público. CI Linux e
macOS com Python 3.11/3.12. Revisão e CI do HEAD antes do merge.

## Fora do escopo

Instalar terceiros; desativar GSD de outra pessoa; autenticar provedores;
configurar gastos; executar benchmark pago automaticamente; deploy de produto;
construir scheduler/MCP/daemon ou garantir poupança de tokens.
