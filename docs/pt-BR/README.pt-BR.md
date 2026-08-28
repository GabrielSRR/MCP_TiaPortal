# Navegação da documentação (comece aqui se for iniciante)

> Só quer colocar para funcionar? Volte ao [`README.md`](../README.md) da raiz do repositório e siga “⚡ Início mais rápido (3 passos)”; não é necessário ler nenhum arquivo deste diretório.
> Esta página orienta quem **quer entender um pouco mais**: escolha uma seção de acordo com sua função; não é preciso ler tudo.

## Sou engenheiro e quero gerar/modificar o projeto sem programar (rota CLI)

1. [`CLI_quickstart.md`](CLI_quickstart.md) — todos os subcomandos e códigos de saída de `tia gen / patch / compile / doctor`
2. [`AI_spec_prompt.md`](AI_spec_prompt.md) — copie para qualquer IA e obtenha uma spec que pode ser usada diretamente com `tia gen`
3. Use diretamente os templates: `../templates/project-blueprints/` (duas specs prontas para partida/parada e motor)

## Quero conectar um cliente de IA (Cursor / Claude / VS Code, rota MCP)

1. Seção “Passos iniciais” do README da raiz — clique duas vezes em `配置MCP.bat` para registrar os quatro hosts de uma vez
2. [`使用说明与介绍.md`](使用说明与介绍.md) — locais dos arquivos de configuração dos clientes, configuração manual e perguntas frequentes
3. [`mcp-ide-and-tool-visibility.md`](mcp-ide-and-tool-visibility.md) — por que podem faltar ferramentas no IDE (cache/limite do cliente, não redução do pacote)

## Sou a IA que conduz este MCP / quero consultar padrões de código

1. `../tools/tiaportal-mcp/skill/SKILL.md` — **especificação principal** (níveis de ferramentas, armadilhas de parâmetros e limites LAD/SCL)
2. [`scl-instruction-library.md`](scl-instruction-library.md) / [`lad-instruction-library.md`](lad-instruction-library.md) — bibliotecas de templates de instruções
3. [`full-project-generation-runbook.md`](full-project-generation-runbook.md) — processo manual em várias etapas (prefira `ScaffoldProject` para execução em uma etapa; este é o caminho de contingência para diagnóstico passo a passo)
4. [`hmi-plc-tag-binding-and-addressing.md`](hmi-plc-tag-binding-and-addressing.md) / [`hmi-connection-driver-matrix.md`](hmi-connection-driver-matrix.md) / [`HMI_Unified_画面生成规范与模板.md`](HMI_Unified_画面生成规范与模板.md) — conjunto de três documentos HMI
5. [`在线实时读值_使用指南.md`](在线实时读值_使用指南.md) — monitoramento online somente leitura

## Estou solucionando problemas

1. Execute primeiro `tia.cmd doctor` (`--fix` adiciona automaticamente o grupo de usuários Openness)
2. [`../手册/error-model.md`](../手册/error-model.md) — descrição dos formatos de erro
3. [`../手册/openness-limitations.md`](../手册/openness-limitations.md) — o que o Openness **não consegue fazer** (não insista nessas operações)

## Referências e índices (para pesquisa; não é preciso ler tudo)

- [`tool-capability-matrix.md`](tool-capability-matrix.md) — matriz completa de capacidades das ferramentas (snapshot estático; em runtime, vale `tools/list`)
- [`../manifest/tools-list.json`](../manifest/tools-list.json) — snapshot da lista de ferramentas
- [`basic-plc-template-library.md`](basic-plc-template-library.md) / [`plc-network-patterns-expanded.md`](plc-network-patterns-expanded.md) / [`optional-reference-materials.md`](optional-reference-materials.md)
- [`../手册/TIA_NL_INTENT_RECIPES.md`](../手册/TIA_NL_INTENT_RECIPES.md) — índice de linguagem natural → sequência de ferramentas
- [`server-maturity-roadmap.md`](server-maturity-roadmap.md) / [`verify-low-barrier-features.md`](verify-low-barrier-features.md) — roadmap e registros de validação

> Nota histórica: `../手册/quickstart.md` e o README da raiz têm conteúdo repetido; **prevalece o README da raiz**.
