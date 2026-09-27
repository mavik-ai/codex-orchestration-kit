# Contribuir

Comece por uma issue com problema, comportamento esperado e evidência. Uma
entrega independente usa uma branch e um PR; não agrupe features sem relação.
Atualize a documentação e CHANGELOG.md junto da implementação.

## Ambiente e gates

Python 3.11+; nenhuma dependência de execução ou teste além da biblioteca padrão.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
```

Use TDD para comportamento novo ou correções do instalador: observe a falha antes
da implementação e execute os gates completos após a correção. Testes usam
`TemporaryDirectory`; nunca a configuração pessoal do desenvolvedor. Modelos,
API, GitHub e autenticação não devem ser chamados pelos testes.

## Revisão e merge

Use Conventional Commits e `Closes #N` no PR. Descreva problema, resultado,
validação, compatibilidade e riscos. A revisão precisa avaliar preservação de
arquivos, symlinks, rollback e limites das afirmações sobre modelos/custos.
CI verde e autorização ativa são requisitos de merge. Não usar bypass/admin.

Ajuste pequeno de documentação não precisa de teste artificial: checker de links
e revisão são suficientes. Mudanças em formatos de manifesto ou instalação
precisam de testes de migração/recusa e reversão antes da publicação.

## Documentação e evidências

Português do Brasil é o idioma principal. Explique decisões por motivação,
alternativas, custos e limites. Não transforme observação local em garantia
universal. Para modelos/Codex, cite documentação oficial e versão observada.

Nunca envie auth.json, logs de sessões, IDs privados, dumps, tokens ou cópias de
configuração pessoal. Exemplos devem ser sintéticos; mantenha só dados agregados
revisados. O kit não redistribui código ou skills de terceiros.
