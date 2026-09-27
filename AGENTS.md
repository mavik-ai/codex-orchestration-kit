# Trabalhar neste repositório

Este repositório distribui configuração e instruções de orquestração; não contém
um runtime de modelos nem cópias de frameworks externos. Python 3.11+, stdlib.

- Leia README.md, docs/SPEC.md e CONTRIBUTING.md antes de editar.
- Uma issue, branch e PR por entrega. Preserve mudanças alheias.
- Teste instalação/reversão em diretórios temporários, nunca no Codex real.
- Não execute modelos, rede ou credenciais nos testes. Não publique logs privados.
- Use TDD para instalação, preservação de arquivos e rollback.
- Gates: `python3 -m unittest discover -s tests -v` e
  `python3 scripts/check_repo.py`.
- Documente comportamento e limitações; não prometa economia sem evidência.
- Use subagentes apenas para partes delimitadas, no máximo dois, sem recursão.
  Workers possuem arquivos separados. Coordenador revisa diff, gates e CI.
- Este kit é autônomo: não instalar control plane MAVIK neste repositório apenas
  por referência à integração; a issue e SPEC são seu contrato desta entrega.
