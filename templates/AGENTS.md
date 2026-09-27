<!-- codex-orchestration-kit:begin -->
## Codex Orchestration Kit

- Use o processo e o estado persistente do projeto. Se MAVIK estiver instalado,
  ele conduz discovery, arquitetura, contrato, specs e entrega. Sem MAVIK, use
  os documentos existentes e critérios de aceite explícitos; não o instale
  automaticamente. Superpowers, quando disponível, apoia debugging, TDD,
  revisão e verificação sem repetir decisões/planos já aprovados. Não acione
  GSD automaticamente apenas pelo tamanho do projeto.
- Tarefa pequena e clara: execute diretamente. Para trabalho complexo, o
  coordenador decide e revisa; use `luna_explorer` em investigação delimitada e
  `sol_worker` na implementação. No máximo dois subagentes simultâneos, sem
  delegação recursiva. Use contexto novo (`fork_turns="none"` quando disponível).
- Cada pacote contém objetivo, evidências, arquivos sob responsabilidade,
  restrições, critérios de aceite e gates. Nunca atribua escritas concorrentes
  nos mesmos arquivos. Reutilize o agente para continuação relacionada e
  evidências existentes em vez de repetir investigação.
- O executor retorna arquivos, verificações/resultados e riscos. O coordenador
  confere o diff e gates, sem repetir verificações válidas sem motivo. Após uma
  tentativa de correção que não resolve o problema, reavalie escopo e modelo.
- Uma task independente, uma issue, uma branch/worktree e um PR. Critérios de
  aceite antes do código; SPEC e TDD conforme contrato/risco do projeto. Testes
  de regressão para bugs e lógica relevante; gates locais antes da publicação.
- Uma autorização explícita no fluxo ativo para "até o fim", "até merge" ou
  "merge automático" cobre issue, branch, commit, push, PR, acompanhamento e
  correções do CI, revisão e merge daquele escopo, sem reconfirmação rotineira.
  Sem essa autorização, não presuma permissão para publicação ou merge.
- Merge requer checks obrigatórios verdes no HEAD atual, revisão sem bloqueios
  e regras do repositório atendidas. Não contorne proteções nem trate CI ausente,
  pendente ou indisponível como sucesso. Confirme o merge remoto, registre
  evidência e só então inicie outra task independente da base atualizada.
- Deploy de produção, release, pagamentos/aumento de gastos, force push e dados
  reais destrutivos continuam exigindo autorização específica. Autorização de
  uma tarefa não é autorização permanente. Preserve segredos e mudanças alheias.
- Meça tempo até resultado aceito, uso do coordenador e filhos, retrabalho e
  qualidade. Não confunda tokens totais, tokens de modelo forte, preço e quota.
  Não afirme economia sem comparação equivalente nem invente preços.
<!-- codex-orchestration-kit:end -->
