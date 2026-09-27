# Avaliação e limites da evidência

Há um piloto real privado, executado em **2026-09-26**, com **Codex CLI 0.157.1
no macOS**. Três modos resolveram o mesmo fixture de bug em slug; cada resultado
passou nos mesmos **21 checks ocultos**. Trata-se de uma execução por modo,
não de uma estimativa confiável da distribuição de desempenho.

| Modo | Tempo observado (s) | Input | Cached input | Output | Checks |
| --- | ---: | ---: | ---: | ---: | ---: |
| Astra sozinho | 60.874 | 195479 | 142080 | 1099 | 21/21 |
| Sol sozinho | 70.161 | 425933 | 382208 | 1597 | 21/21 |
| Orquestrado, contador do pai | 97.735 | 399173 | 358400 | 1049 | 21/21 |
| Filho observado separadamente | — | 337748 | 292864 | 1718 | — |

Foi confirmado um filho Sol com `fork_turns="none"`. A tarefa era pequena e a
orquestração foi forçada deliberadamente para observar seu overhead, contrariando
a política normal de execução direta. Os tempos observados favorecem execução
individual nesse caso; não permitem concluir que qualquer modo vencerá em
problemas maiores, nem estimar economia de assinatura.

Não está confirmado se o contador do pai inclui uso do filho. Portanto, **não
some essas linhas para produzir um total orquestrado**. Cached input é uma
parcela da entrada, não uma quantidade adicional a somar. Não acrescente tokens
de raciocínio a output se já estiverem incluídos. Comparações financeiras exigem
semântica comprovada dos contadores, preços aplicáveis e modalidade de cobrança;
quota da assinatura é outra métrica. Nenhum valor de custo ou economia é inferido
aqui.

## Protocolo manual reproduzível

1. Prepare fixtures versionados e independentes de credenciais, com estado inicial
   idêntico por modo. Separe tarefas pequenas, investigação ampla, implementação
   delimitada e mudanças que exigem coordenação. Defina aceite e checks ocultos
   antes de executar; não permita ao agente ler esses checks.
2. Compare Astra sozinho, Sol sozinho e política orquestrada. Registre versões,
   IDs efetivos, esforço, permissões, plugins, instruções e contexto fornecido.
   Use ambientes equivalentes; diferencie a política normal da delegação forçada.
3. Execute repetições por categoria, alternando a ordem. Registre estado de cache
   conhecido e fatores não controlados. Não escolha apenas a melhor execução.
4. Meça tempo desde a entrega da tarefa até resultado aceito, incluindo revisão,
   correções e testes. Conte tentativas, intervenções humanas, falhas e regressões,
   além de aprovação funcional e respeito ao escopo.
5. Colete uso do coordenador e dos filhos em registros locais. Identifique a
   relação pai/filho e a semântica cumulativa ou incremental antes de deduplicar.
   Separe uso Astra, demais modelos e total conhecido; mantenha campos ambíguos
   como desconhecidos. Não some snapshots cumulativos nem subtotais sobrepostos.
6. Publique agregados por categoria, dispersão e quantidade de amostras. Remova
   credenciais, caminhos locais, IDs de sessão, conversas e logs brutos. Declare
   limitações e preserve evidências privadas para auditoria autorizada.

Este protocolo permite novas comparações controladas. **Não reconstrói exatamente
o piloto privado:** seu ambiente de plugins e contexto não é distribuído. O kit
não promete neste momento um harness público de benchmark nem executa chamadas
pagas automaticamente. Os gates do instalador verificam segurança e integridade
da configuração; sua aprovação não demonstra melhor desempenho dos agentes.
