# Integrações e responsabilidades

O kit funciona com Codex sem MAVIK, Superpowers ou GSD. O usuário escolhe o
processo do projeto; o kit define como distribuir trabalho e validar entrega.
Nenhum desses projetos é instalado, copiado, atualizado ou removido pelo script.

## MAVIK: processo principal quando já existe

No ambiente que originou o kit, MAVIK gerencia discovery, arquitetura, contrato,
specs e estado persistente. Isso evita usar a conversa como banco de decisões.
Se o projeto já possui `.mavik`, siga seu AGENTS e control plane, incluindo
aprovações, limites e gates. Não escreva estado gerenciado manualmente.

Sem MAVIK, mantenha o mesmo contrato em issue, SPEC e documentação existente.
Não é necessário gerar um framework só para usar os papéis do kit. A integração
é uma convenção de instruções; não é uma API validada ou dependência empacotada.

## Superpowers: práticas técnicas

[Superpowers](https://github.com/obra/superpowers) oferece workflows de debugging,
TDD, planejamento e revisão. No arranjo original, usamos essas práticas como
apoio: um plano aprovado pelo processo do projeto não precisa de nova entrevista
ou outro plano equivalente. As instruções do usuário e as regras do repositório
continuam definindo autorização e prioridade.

Instale separadamente conforme a documentação do projeto, se desejar. O kit não
redistribui skills nem presume que estejam disponíveis. Sem o plugin, critérios
de aceite, testes e revisão continuam sendo requisitos do fluxo.

## GSD: desativação não é uma instalação deste kit

[GSD](https://github.com/gsd-build/get-shit-done) cobre planejamento, fases e
continuidade. No ambiente original já havia um processo MAVIK para isso; por
esse motivo foi desativado ali para reduzir sobreposição, não por uma conclusão
universal de inferioridade.

O kit **não desativa GSD de outra pessoa**. O template apenas orienta a não
acioná-lo automaticamente por tamanho do projeto. Se já houver missão GSD,
preserve `.planning/` e decida conscientemente qual processo conduzirá a entrega.

Se escolher desativá-lo no seu ambiente, faça backup e use controles suportados
pelo seu cliente. Uma referência de skill em `skills.config` pode depender de
versão e path. No CLI 0.157.1 observado, o path completo até `SKILL.md` foi
necessário; usar só a pasta não retirou a skill do catálogo. Atualizações podem
mudar esse comportamento. Não copie paths da máquina de outra pessoa.

## GitHub

A política organiza issue → branch → PR → CI/revisão → merge. O kit não contém
bot, token, GitHub App ou processo de auto-merge. Quem executa é o Codex, usando
ferramentas e autorização do usuário. Configure branch protection/rulesets no
repositório para impor checks no servidor; instruções não substituem proteção.

## Atribuição

Este repositório contém configuração, código e documentação próprios sob MIT.
Os nomes Codex/OpenAI, MAVIK, Superpowers e GSD identificam integrações ou fontes;
não indicam endosso da OpenAI nem licenciamento de terceiros por este projeto.
Os projetos externos conservam suas licenças e requisitos próprios.
