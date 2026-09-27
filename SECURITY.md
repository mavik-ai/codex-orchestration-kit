# Segurança

O instalador manipula arquivos locais de configuração. Execute apenas código
revisado de uma origem confiável, sem sudo. Faça a prévia e escolha o CODEX_HOME
correto. O kit não gerencia login, credenciais, permissões de apps ou pagamentos.

## Limites

- Modelos, plugins, servidores MCP e repositórios podem introduzir instruções
  adicionais. Uma política em Markdown não é um isolamento de segurança.
- A leitura somente do investigador usa sandbox nativo; proteção efetiva depende
  do runtime/ambiente. Para o executor, o kit preserva a política de permissões
  existente, sem conceder `danger-full-access` ou bypass.
- Arquivos de papéis e AGENTS têm alcance por CODEX_HOME. Use homes separados
  quando precisar isolar políticas; não compartilhe auth.json ou sessões.
- Backups podem conter instruções privadas preexistentes. Mantenha-os locais,
  com acesso restrito; nunca os publique em issues ou PRs.
- O restore aceita apenas seu próprio manifesto e paths dentro do home escolhido,
  recusa links simbólicos e mudanças posteriores nos destinos. Não restaure um
  manifesto de outra pessoa nem mova backups manualmente.
- Os testes/CI não executam modelos e não precisam de secrets. O checker textual
  ajuda a detectar exposições comuns, mas não substitui revisão humana.

## Relatar vulnerabilidades

Não publique segredos ou exploração de ambientes reais em issues. Se o GitHub
oferecer “Report a vulnerability” na aba Security, use o canal privado. Se não
estiver disponível, abra uma issue solicitando contato privado, sem detalhes
sensíveis; o mantenedor combinará um canal antes de receber a evidência.

Versões: projeto inicial sem release estável. Correções serão publicadas primeiro
na branch main com testes de regressão e changelog. Não há SLA de resposta.
