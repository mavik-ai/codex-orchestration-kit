# Fluxo de trabalho

O contrato do projeto vem antes do roteamento entre modelos. Leia `AGENTS.md`,
a issue, a SPEC e o mecanismo de estado existente; confirme diretório, branch,
HEAD e alterações locais. Não recrie discovery ou aprovações já registrados.
MAVIK é uma integração opcional: onde existir, use seu control plane; este kit
não instala um novo lifecycle por conta própria.

## Da issue ao pacote

Uma tarefa independente corresponde a uma issue, branch e PR. Defina critérios
de aceite antes do código e use uma SPEC proporcional ao risco. Uma correção
pequena pode ter critérios curtos; autenticação, dados e instalação reversível
exigem invariantes e casos de falha explícitos.

Execute diretamente trabalho pequeno e claro. Delegue quando investigação ou
implementação puderem ser delimitadas com ganho plausível. Um pacote deve trazer:

- Objetivo observável e contexto mínimo, incluindo comportamento atual.
- Arquivos sob responsabilidade exclusiva e interfaces que deve preservar.
- Restrições, critérios de aceite, comandos de validação e evidência esperada.
- Aviso de trabalho concorrente: preservar alterações alheias e não delegar.

Luna responde a uma pergunta específica de leitura. Sol recebe implementação
com ownership definido. Não distribua o mesmo arquivo para dois executores.
Prefira contexto novo e reutilize o agente para continuação da mesma tarefa.
Se houver falha, permita uma tentativa de correção; depois reavalie causa,
escopo, contexto ou modelo. Isso evita repetir instruções sem informação nova.

## Implementação, revisão e autorização

Para bug ou lógica relevante, reproduza a falha, crie o menor teste de regressão
útil, aplique a correção e verifique o comportamento. TDD não exige uma suíte
artificial para uma mudança textual trivial. Técnicas do Superpowers são
opcionais e não devem abrir um segundo ciclo de aprovação equivalente.

O executor devolve arquivos alterados, comandos/resultados e riscos. O
coordenador lê o diff, verifica critérios e roda gates ausentes ou justificados
por mudanças novas. Não repete toda investigação já sustentada por evidências.
Uma mensagem de sucesso do filho não substitui revisão.

Commit, push, PR e merge dependem de autorização ativa explícita. Uma autorização
“até o fim” ou “até merge” cobre essas etapas naquele escopo; não precisa ser
solicitada novamente a cada comando. Sem ela, prepare o resultado local e
apresente o ponto de entrega. Deploy em produção, gastos e dados destrutivos
permanecem autorizações separadas.

Quando autorizada a entrega completa, siga: gates locais → commit → push → PR →
CI no HEAD atual → revisão sem pendências impeditivas → merge → confirmação
remota e registro no mecanismo do projeto. CI pendente ou bloqueado por
infraestrutura não é verde. Uma alteração após CI exige verificar o novo HEAD.
Só inicie a próxima tarefa independente após concluir a atual e atualizar a base.

Neste repositório os gates são:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
```

Registre separadamente validação local, CI hospedado, execução real de modelos e
produção. Instalar arquivos e passar `doctor` não homologa nenhuma dessas últimas
camadas. Em uma retomada, use os artefatos persistentes para decidir a próxima
etapa, preservando o trabalho que já passou pelos gates.
