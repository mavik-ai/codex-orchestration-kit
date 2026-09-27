# Decisões arquiteturais

As decisões abaixo estão aceitas para esta versão. O status diferencia contrato,
controle nativo e política de prompt; nenhum deles substitui evidência de execução.

## ADR-001 — Usar o runtime nativo

**Motivação:** resolver distribuição de trabalho sem manter outro orquestrador.
**Decisão:** TOML, instruções e instalador Python com biblioteca padrão.
**Alternativas:** scheduler próprio, MCP coordenador ou dependência de framework.
**Desvantagem:** comportamento e recursos dependem da versão/interface do Codex.
**Aplicação:** testes locais de arquivos e validação manual da configuração ativa;
não existe motor independente para impor o fluxo. **Status:** aceita.

## ADR-002 — Delegação seletiva e limitada

**Motivação:** reduzir contexto desnecessário sem transferir toda tarefa pequena.
**Decisão:** Astra `low` coordena/revisa; Sol `medium` implementa; Luna `high`
investiga. Até dois filhos, ownership separado, sem recursão e contexto novo
quando suportado. Após uma correção sem sucesso, reavaliar com o coordenador.
**Alternativas:** delegar sempre, herdar todo histórico ou aumentar concorrência.
**Desvantagem:** pacotes incompletos exigem esclarecimento e a revisão tem custo.
**Aplicação:** concorrência no runtime; demais regras em prompts e revisão.
IDs personalizados são permitidos, sem garantia de acesso. **Status:** aceita;
eficácia comparativa ainda não demonstrada.

## ADR-003 — Perfil opt-in com limite de isolamento explícito

**Motivação:** preservar a configuração existente e permitir reversão.
**Decisão:** arquivo complementar, papéis e bloco identificado em `AGENTS.md`;
prévia por padrão, backup antes de aplicar, restauração protegida contra divergência.
**Alternativas:** substituir `config.toml` ou editar silenciosamente plugins.
**Desvantagem:** o carregamento direto por `codex -p orchestration` tem como
referência suportada o CLI 0.157.1; clientes anteriores não são suportados.
Papéis e instruções valem no home, inclusive fora do perfil. **Aplicação:** testes
do instalador e home separado quando isolamento for necessário. **Status:** aceita.

## ADR-004 — Um processo de entrega, técnicas opcionais

**Motivação:** evitar processos simultâneos disputando estado e aprovações.
**Decisão:** respeitar o lifecycle existente. MAVIK pode conduzir contrato e
entrega; [Superpowers](https://github.com/obra/superpowers) pode apoiar debugging,
TDD e revisão. Nenhum é dependência obrigatória do kit.
**Alternativas:** instalar um conjunto completo de frameworks por padrão.
**Desvantagem:** cada projeto precisa declarar qual mecanismo mantém seu estado.
**Aplicação:** preservar contratos existentes, sem baixar, copiar, instalar ou
desativar terceiros. [GSD](https://github.com/gsd-build/get-shit-done) foi redundante
no ambiente original já organizado por MAVIK; isso não demonstra inferioridade
universal. Os links atribuem referências, não redistribuem conteúdo.
**Status:** aceita.

## ADR-005 — Medir resultado aceito

**Motivação:** tokens de um coordenador isolado podem ocultar trabalho dos filhos.
**Decisão:** comparar qualidade, tempo, tentativas e uso deduplicado por modelo;
manter custo e quota separados. **Alternativa:** promover um único contador ou
piloto como economia comprovada. **Desvantagem:** telemetria ambígua impede alguns
totais e exige repetir tarefas. **Aplicação:** protocolo e limites de inferência
em [EVALUATION.md](EVALUATION.md). **Status:** aceita.
