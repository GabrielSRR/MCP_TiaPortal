# Matriz de capacidades das ferramentas MCP

Este documento foi gerado estaticamente a partir dos `[McpServerTool]` do código-fonte. Em runtime, a referência final continua sendo `tools/list`.

- Data de geração: 2026-06-09 18:20:55
- Quantidade de ferramentas: 189

## Níveis de acesso

| Nível | Significado |
|---|---|
| L0 | Orientação, diagnóstico e relatórios; não altera o projeto |
| L1 | Operações principais de portal, projeto, hardware e PLC |
| L2 | Operações especializadas, reflexão, HMI, builders, alarmes e monitoramento |

## L0

| Ferramenta | Descrição |
|---|---|
| `Bootstrap` | Primeira ferramenta a ser chamada por qualquer IA. Retorna versão do TIA, status do grupo Openness, estado atual de conexão/projeto, próxima ferramenta recomendada, catálogo L0/L1 e limitações conhecidas. Não conecta ao TIA. |
| `RunCapabilitySelfTest` | Executa um autoteste somente leitura de prontidão do MCP/TIA, incluindo grupo Openness, conexão, processos visíveis e, opcionalmente, árvore do projeto. |
| `RunOnlineMonitoringSafetySelfTest` | Valida estaticamente as proteções do monitoramento online, sem conexão, escrita, força ou alteração de watch tables. |
| `GetState` | Retorna estado da conexão, projeto aberto e sessão aberta. |
| `GenerateAcceptanceReport` | Gera relatório de aceitação Markdown/JSON do ambiente MCP/TIA sem alterar o projeto. |
| `GenerateErrorReport` | Gera relatório padronizado de erro Markdown/JSON; somente grava arquivos de relatório. |

## L1

### Diagnóstico

| Ferramenta | Descrição |
|---|---|
| `ValidateAutomationContext` | Faz o preflight do projeto atual: dispositivos, softwares, caminhos esperados de PLC/HMI e árvore do projeto. |

### Hardware e projeto

| Ferramenta | Descrição |
|---|---|
| `ConnectDeviceNodesToProfinetSubnet` | Configura a rede PROFINET entre dois dispositivos e retorna evidência de leitura posterior. |
| `GetDevices` | Lista dispositivos de hardware e seus atributos. |
| `AddDeviceWithFallback` | Adiciona dispositivo Siemens pesquisando o catálogo instalado e tentando versões alternativas. |
| `SearchHardwareCatalog` | Pesquisa o catálogo de hardware por MLFB, família, dispositivo ou descrição. |
| `OpenProject` | Abre um projeto `.apXX` ou sessão `.alsXX`. |
| `AttachToOpenProject` | Conecta o MCP a um projeto já aberto pelo nome. |
| `CreateProject` | Cria e abre um projeto TIA vazio. |
| `ScaffoldProject` | Gera um projeto completo a partir de uma spec JSON, incluindo PLC, HMI opcional, blocos, tags, telas, compilação e salvamento. Use `dryRun=true` primeiro. |
| `SaveProject` | Salva o projeto ou sessão atual. |
| `CloseProject` | Fecha o projeto; alterações não salvas são perdidas. |
| `GetProjectTree` | Retorna a árvore completa de dispositivos e softwares; use-a primeiro para descobrir caminhos exatos. |

### PLC online

| Ferramenta | Descrição |
|---|---|
| `GetOnlineState` | Lê o estado de conexão do PLC sem alterá-lo. |
| `GoOnline` | Conecta o TIA Portal ao PLC físico. |
| `GoOffline` | Desconecta a sessão online do PLC. |
| `CheckDownloadReadiness` | Verifica se o PLC está pronto para receber download, sem realizar o download. |
| `DownloadToPlc` | Faz download do programa compilado para a CPU física; altera o comportamento em operação e exige confirmação de segurança. |

### PLC software

| Ferramenta | Descrição |
|---|---|
| `GetSoftwareInfo` | Retorna propriedades do software PLC. |
| `PlcBuildAndImport` | Principal ferramenta para criar/importar UDT, tabela de tags, GlobalDB, FC ou FB a partir de JSON; use dry run primeiro. |
| `ImportPlcTagTable` | Importa uma tabela de tags PLC XML. |
| `WritePlcSclSourceFile` | Grava uma fonte SCL externa UTF-8 com BOM no disco; não conecta nem importa. |
| `CompileSoftware` | Compila todos os blocos do software PLC. |
| `CompileAndDiagnosePlc` | Compila e retorna erros/avisos estruturados com caminho e descrição. |

## L2

### Hardware

Inclui `GetDeviceInfo`, `GetDeviceItemInfo`, `GetDeviceItemTree`, `GetDeviceItemNetworkInfo`, `SetDeviceItemAttribute`, `PlanHardwareNetworkConfiguration`, `EnsureSubnet`, `AttachDeviceNodeToSubnet`, `SetCpuCommonSettings`, sondas de conexões HMI, `AddDevice`, `SearchInstalledGsdDevices`, `AddGsdDeviceWithProbe` e `AddHardwareCatalogDeviceWithProbe`. Essas ferramentas leem, validam ou configuram hardware conforme os pré-requisitos descritos em suas assinaturas.

### HMI

Inclui `GetHmiProgramInfo`, ferramentas de descrição/listagem/exportação/importação de telas, tags e conexões, além dos builders e validadores Classic/Basic. As ferramentas Unified incluem `EnsureUnifiedHmiScreen`, `EnsureUnifiedHmiTagTable`, `EnsureUnifiedHmiTag`, `EnsureUnifiedHmiConnection`, `EnsureUnifiedHmiScreenItem`, `ApplyUnifiedHmiScreenDesignJson`, `ApplyUnifiedHmiTheme`, `ApplyUnifiedHmiLayout`, dinamizações e ações seguras de botões.

### HMI-Library

`ProbeGlobalLibrary`, `ImportMasterCopyFromGlobalLibrary`, `AnalyzeGlobalLibraryPackage`, `PlanGlobalLibraryTemplateReuse`, `AnalyzeHmiTemplateReference` e `AnalyzeUnifiedHmiTemplateLayout` permitem inspecionar bibliotecas/templates, planejar reutilização e validar layouts; as ferramentas offline não modificam projetos.

### Online-Monitoring

Inclui `ProbePlcMonitorOnlineCapabilities`, `ReadPlcWatchTableCurrentValuesReadOnly`, `PlanOnlineReadOnlyMonitoring`, `PlanOnlineReadOnlyDataProvider`, `ProbeS7CpuIdentity`, `ReadPlcLiveValuesS7`, `SamplePlcLiveValuesS7`, `ReadPlcLiveValuesOpcUa`, `GetPlcRunStateS7`, `MonitorWatchTableLiveS7`, `TraceTagCause` e `TraceTagCauseLive`. São ferramentas de leitura/planejamento; não escrevem nem usam força.

### PLC-Alarms

`ExportAlarmClasses`, `ImportAlarmClasses`, `ExportAlarmTextLists`, `ImportAlarmTextLists` e `ExportAlarmInstanceTexts` exportam/importam classes e textos de alarmes. Compile após importações.

### PLC-Builders

`BuildPlcUdtXml`, `BuildPlcTagTableXml`, `BuildPlcGlobalDbXml`, `BuildStructuredTextXml`, `BuildFlgNetCallXml`, `ComposePlcFcBlockXml`, `ComposePlcFbBlockXml`, `ComposePlcLadFcBlockXml` e `BuildPlcSymbolManifestFromXmlPath` geram XML/manifests offline. Builders LAD têm escopo restrito; para lógica geral, prefira S7DCL/SCL.

### PLC-Software

Inclui ferramentas de blocos, tipos, grupos, fontes externas, exportação/importação XML ou documentos SIMATIC SD, referências cruzadas, watch tables, tecnologia e semeadura a partir de referência: `GetSoftwareTree`, `GetBlocks`, `GetBlocksWithHierarchy`, `GetBlockInfo`, `ExportBlock`, `ExportBlocks`, `ExportAsDocuments`, `ExportBlocksAsDocuments`, `ImportBlock`, `ImportBlocksFromDirectory`, `ImportFromDocuments`, `ImportBlocksFromDocuments`, `ImportPlcProgramFromDirectory`, `RepairAndReimportBlock`, `GetTypes`, `GetTypeInfo`, `ExportType`, `ExportTypes`, `ImportType`, `GetPlcExternalSources`, `ImportPlcExternalSource`, `DeletePlcExternalSource`, `GenerateBlocksFromExternalSource`, `GetPlcTagTables`, `ExportPlcTagTable`, `ImportPlcTagTablesFromDirectory`, `GetPlcWatchTables`, `ExportPlcWatchTable`, `ExportPlcWatchTablesToDirectory`, `GetCrossReferences`, `GetTechnologyObjects`, `ExportTechnologyObject`, `ExportTechnologyObjectsToDirectory`, `ImportTechnologyObject`, `ImportTechnologyObjectsFromDirectory` e `SeedProjectFromReference`.

### PLC-Online e OPC UA

`GetPlcForceTables`, `SetWatchTableModifyValue` e `CompareSoftwareToOnline` cobrem tabelas de força, modificações condicionais e comparação offline/online. `GetOpcUaConfig`, `SetOpcUaInterfaceEnabled`, `ExportOpcUaInterface` e `ImportOpcUaInterface` auditam e configuram interfaces OPC UA; alterações exigem download para a CPU.

### Reflexão e relatórios

`DescribeObject`, `DescribeObjectProperty`, `GetObjectProperty`, `ListObjectChildren`, `InvokeObject`, `DescribeService` e `InvokeService` expõem APIs públicas via reflexão. `SaveAsProject` salva uma cópia com novo nome. Ferramentas de relatórios incluem `BuildReleaseDiagnosticReport`, `BuildReleaseRunbook`, `BuildReleaseManifest` e `RebuildReleaseHandoffArtifacts`.

### Validação

`RunOfflineReleaseValidationSuite`, `RunV2PlanCompletionAudit` e `RunHmiTemplatePlcSyncPrecheckSuite` executam validações offline de release, planos e sincronização de templates HMI com símbolos PLC.

> Os nomes e parâmetros efetivamente disponíveis podem variar conforme o executável carregado. Para a lista autoritativa em runtime, sempre use `tools/list`.
