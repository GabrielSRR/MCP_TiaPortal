# Registro de alterações

## [2.5.2] - 2026-08-25 - Correção da listagem de tabelas de variáveis (#22) e monitor sem iniciar o TIA

### Correções

- **`GetPlcTagTables` sempre retornava uma lista vazia** ([#22](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP/issues/22)). A composição já era `PlcTagTableComposition`, mas o código procurava novamente uma propriedade `.TagTables`. Isso fazia qualquer projeto S7-1200/1500 retornar `{"items":[],"success":true}`. Corrigido e validado em um projeto real com 7 PLCs: cada PLC passou a listar de 1 a 6 tabelas e a exportação gera XML utilizável.
- Tabelas dentro de grupos de usuário agora também são listadas/exportadas. O formato `Grupo/Tabela` é aceito, inclusive com barra invertida.
- Falhas de enumeração não são mais apresentadas como “nenhuma tabela”; erros de container e de exportação agora são diferenciados e os nomes disponíveis são informados.

### vci-watch

- O monitor não inicia mais o TIA Portal sozinho. Processos com `-bootstrapper=` são ignorados; antes de `Connect`, `ListPortalProcessProjects` confirma se existe um projeto ao qual anexar.
- Instâncias headless remanescentes são encerradas na rodada seguinte, após validação da linha de comando completa e do PID salvo em `watch.state.json`.
- A correção de espera regressiva da versão 2.5.1 também foi incorporada ao branch público.

### Consistência de versão

`Validate-Bundle.ps1` agora confirma que o primeiro item do CHANGELOG, `AssemblyVersion` em `TiaMcpServer.csproj` e `bundleVersion`/`packageName` em `manifest/package-manifest.json` são compatíveis.

## [2.5.1] - 2026-08-23 - Correção da espera regressiva do vci-watch

Corrigido o problema em que um estado inválido persistente era tratado como falha temporária e repetido continuamente. Blocos não compilados permaneciam `Unequal` e cada exportação falhava com `The block is inconsistent`, mantendo o TIA ocupado.

- Adicionado `pendingCompileCooldownMinutes` (padrão: 30 minutos), suspenso até que o diretório do projeto mude.
- Adicionado `minFullCheckMinutes` (padrão: 10 minutos).
- Recomenda-se intervalo de 5 minutos na tarefa agendada.
- As sete situações da tabela de decisão foram testadas, incluindo um sentinel de falha obrigatória.

## [2.5.0] - 2026-08-20 - Controle de versão do projeto TIA com VCI

A interface de controle de versão da V21 mapeia o projeto binário para uma pasta com arquivos de texto por objeto, permitindo diff, revisão e rollback sem clicar na interface do TIA.

```text
1) CreateVersionControlWorkspace(workspaceName="git", folderPath="D:\repos\my-plc")
2) ConnectProjectToWorkspace(dryRun=false)
3) SyncVersionControlWorkspace(direction="ProjectToWorkspace", dryRun=false)
   git add -A && git commit
```

### Novidades

- Incluído o conjunto VCI: `CreateVersionControlWorkspace`, `ConnectProjectToWorkspace`, `GetVersionControlWorkspaces`, `GetVersionControlStatus` e `SyncVersionControlWorkspace`.
- Incluído `tools/vci-watch/`, que compila, exporta, grava o CHANGELOG e executa `git commit` automaticamente, sem abrir ou escrever no projeto.
- Exportação `ProjectToWorkspace` é gratuita; restauração `WorkspaceToProject` exige Pro.

### Correções

- `GetVersionControlStatus` agora retorna `CompareState` (`Equal`, `Unequal`, `WorkspaceFileMissing`, `Unknown`) em vez do nome do tipo.
- Objetos `Equal` são ignorados durante a sincronização para evitar o erro do Openness ao sincronizar um mapeamento já igual.

## [2.3.1] - 2026-07-25 - Menor barreira para usuários de git clone e perfil lite

- Scripts e comandos detectam automaticamente tanto o layout do pacote Release quanto o layout de clone Git (`runtime\v21`).
- `tia config` usa `TIA_MCP_PROFILE=lite` por padrão; `config --full` habilita todas as ferramentas.
- O perfil lite passou a incluir as ferramentas do fluxo principal: `ImportFromDocuments`, `GenerateBlocksFromExternalSource`, `GetBlocks`, `GetBlocksWithHierarchy`, `GetBlockInfo`, `ExportAsDocuments` e `GoOffline`.
- README, navegação de documentos, `doctor` e caminhos dos executáveis foram alinhados.

## [2.3.0] - 2026-07-04 - `DescribeBlockLogic`

Incluída a ferramenta `DescribeBlockLogic(softwarePath, blockPath)`, que reconstrói redes LAD como expressões legíveis, mostra contatos em série/paralelo, bobinas, MOVE, comparações e temporizadores, e marca contatos ligados a constantes como `⟨恒断·禁用本行⟩` (linha permanentemente desligada). A ferramenta é somente leitura e está disponível também no perfil lite.

## [2.2.9] - 2026-07-04 - Importação de documentos mais robusta

- Caminhos de grupos aninhados agora são validados explicitamente; não resolvê-los não redireciona silenciosamente o bloco para a raiz.
- Erros reais de importação são propagados com contexto.
- Exportações e importações informam claramente inconsistência, grupo inexistente e bloqueio por know-how.
- Mantida a numeração e a posição dos blocos.

## [2.2.8] - 2026-07-03

- Melhorias de diagnóstico, importação/exportação textual e validação de blocos.
- Ajustes de documentação e dos fluxos de compilação.

## [2.2.0] - 2026-06-17 - Download V21 e seleção de interface PG/PC

- Corrigida a conversão V21 de `ConfigurationTargetInterface` para `IConfiguration`.
- Corrigida a opção `StopAll` durante o download.
- Em PCs com várias placas de rede, as rotas são classificadas pela proximidade do IP da CPU, priorizando a mesma rede IPv4 `/24`.
- `DownloadToPlc` aceita `pgPcInterface` e `targetIpAddress`; falhas exibem todas as rotas candidatas.
- `CheckDownloadReadiness` retorna `meta.downloadRoutes` em modo somente leitura.

## [2.1.0] - 2026-06-10

- Aprimoramentos de HMI Unified, sincronização de tags PLC/HMI, validações offline e mensagens de erro.
- Melhorias na resolução de caminhos e no diagnóstico de conexões.

## [2.0.0] - 2026-06-02 - CLI declarativa

O mesmo executável passou a funcionar como serviço MCP e como CLI. Qualquer IA pode gerar uma spec YAML/JSON e qualquer engenheiro pode criar ou alterar um projeto com um comando.

### CLI `tia`

- `tia gen <spec.yaml|json>` gera o projeto; `--dry-run` valida offline e `--json` retorna saída de máquina.
- `tia patch <spec.yaml|json>` faz upsert incremental em projeto existente.
- `tia compile`, `describe`, `export`, `import`, `prewarm`, `schema`, `version` e `help`.
- Códigos de saída: 0 = sucesso, 1 = etapas com falha, 2 = erro.
- YAML e JSON são aceitos; YAML é convertido com inferência de tipos.
- Adicionados `tia.cmd` (V21) e `tia-v20.cmd` (V20), suporte a caminhos relativos e resolução automática de `__BUNDLE__`.

## [1.0.0] - 2026-06-02

- Inicialização headless padrão reduzida de aproximadamente 200–340 s para 10–28 s.
- `scripts/prewarm_tia.py` mantém uma instância headless e reduz conexões seguintes para aproximadamente 0,8–1 s.
- Incluído `ScaffoldProject`, que cria hardware, UDTs, DBs, tags, fontes SCL, LAD, HMI, compila e salva em uma chamada.
- Incluídos templates `scaffold_spec_start_stop.json` e `scaffold_spec_motor.json`.
- Melhorias na descoberta automática do software HMI, na conexão e na validação de leitura após importação.
- Redução do número de ferramentas de 184 para 180.

## [0.0.40] - 2026-06-02

- Templates SCL, UDT e DB receberam comentários e lógica mais completa.
- Binários Release foram removidos do rastreamento Git e passaram a ser distribuídos por GitHub Release.

## [0.0.39] - 2026-06-01 - Geração pública com prioridade à estabilidade

- `PlcBuildAndImport` passou a retornar `CapabilityDecision`, `CapabilityWarnings` e `RecommendedNextActions`.
- Expressões SCL complexas são direcionadas para fontes `.scl/.s7dcl` externas.
- `ApplyUnifiedHmiScreenDesignJson` usa `strict=true` por padrão.
- `EnsureUnifiedHmiTag` valida a leitura posterior da vinculação por padrão.

## [0.0.38] - 2026-05-31

- `StructuredTextXmlBuilder` agora falha rapidamente ao receber expressões em campos destinados a identificadores simples.
- FCs/FBs com expressões, `CASE` ou `TON` foram transferidos para fontes SCL externas.
- Adicionados BOM UTF-8 e validações de templates, símbolos PLC e layout HMI.

## [0.0.31] - 2026-05-29

- Transporte HTTP corrigido: leitura/escrita síncrona do corpo e timeout de 30 s.
- Testado ponta a ponta com `curl`: `initialize`, `notifications/initialized` e `tools/call Bootstrap`.
- Executáveis V20 e V21 reconstruídos sem erros.

## [0.0.30] - 2026-05-28

- Corrigida a importação no V20, que rejeitava XML com `engineering version="V21"`.
- A versão de engenharia agora é normalizada no limite de importação sem alterar o arquivo original.

## [0.0.29] - 2026-05-26

- Pacote completo com executáveis V20/V21 e dependências.
- Publicado o Release [v0.0.29](https://github.com/bulaofen0036-coder/TIA_MCP_260514/releases/tag/v0.0.29).
- Diagnósticos de compilação agora retornam detalhes folha com `Path` e `Description`.

## [0.0.28] - 2026-05-26 - Suporte V20 + V21

- Criado `TiaMcpServer.V20.csproj`; V20 e V21 usam executáveis separados.
- Adicionado `--tia-portal-location`.
- Adicionados aliases textuais para exportação/importação S7DCL/SCL.
- Validação real de exportação e importação em V20 e V21.

## [0.0.27] - 2026-05-09 - Auditoria de estabilidade e operações online

- Adicionado `CompareSoftwareToOnline`.
- `GoOnline` e `DownloadToPlc` passaram a aceitar senha.
- Resolvidos serviços online/download em CPUs 1200/1500 aninhadas.
- Eliminadas falhas silenciosas em caminhos críticos.
- Cobertura de categorias das ferramentas normalizada.

## [0.0.19] - 2026-05-08

- Adicionado transporte HTTP.
- Corrigados comentários de `Logging` e typo “Narketplace” → “Marketplace”.

## [0.0.16] - 2025-09-02

- Adicionadas importação/exportação em documentos V20+.
- Verificações de versão, preflight de `.s7res` e melhorias de mensagens.

## [0.0.15] - 2025-08-30

- Prompts aprimorados.
- Tarefas longas executadas de forma assíncrona.

## [0.0.14] - 2025-08-18

- Melhor estrutura de árvore e novo `GetSoftwareTree()`.
- Correções gerais.

## [0.0.13] - 2025-08-14

- Logging integrado e prompts adicionados.

## [0.0.12] - 2025-08-07

- Correção do caminho de exportação.

## [0.0.11] - 2025-08-07

- Estrutura do projeto formatada como bloco Markdown.

## [0.0.10] - 2025-08-07

- Respostas das ferramentas aprimoradas.

## [0.0.9] - 2025-08-04

- Exportação de blocos e tipos com `preservePath`.
- Novas ferramentas e atributos nas informações retornadas.

## [0.0.8] - 2025-08-01

- Respostas JSON-RPC aprimoradas e dependências atualizadas.

## [0.0.7] - 2025-07-18

- Novo `GetState()` e correção dos valores retornados.

## [0.0.6] - 2025-07-16

- Código adaptado à nova API do TIA Portal.
- PLC software passou a retornar apenas blocos OB/FB/FC/DB e tipos UDT.
- Filtros regex e importação de blocos/tipos adicionados.

## [0.0.5] - 2025-07-11

- Resolução do PLC por `softwarePath`, inclusive em grupos/subgrupos.
- Nova ferramenta para recuperar a estrutura do projeto como texto.
- Nova ferramenta para compilar o software PLC.

## [0.0.4] - 2025-06-30

- Abertura de sessões locais ou projetos conforme a extensão do arquivo.

## [0.0.3] - 2025-06-23

- Publicação no Visual Studio Code Marketplace.
