# Manual de execução para geração completa do projeto

Este manual descreve o processo completo para gerar um projeto PLC + WinCC Unified a partir de um projeto vazio. Todos os arquivos estão incluídos no pacote de entrega.

## Zero. Autoverificação do pacote de entrega (recomendado)

Execute na raiz do pacote (não é necessário iniciar o TIA):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Validate-Bundle.ps1
```

Somente depois de concluir essa etapa conecte-se ao MCP; `-Strict` é opcional.

## Arquivos de entrada

| Arquivo | Finalidade |
|---|---|
| `tools/tiaportal-mcp/skill/SKILL.md` | Regras de chamada das ferramentas |
| `templates/project-blueprints/full_plc_hmi_project.json` | Blueprint do projeto |
| `templates/plc/README.md` | Índice dos templates de PLC |
| `templates/hmi/README.md` | Índice dos templates de HMI |
| `docs/basic-plc-template-library.md` | Descrição das instruções do PLC |
| `docs/HMI_Unified_画面生成规范与模板.md` | Especificação das telas HMI |
| `docs/hmi-plc-tag-binding-and-addressing.md` | Símbolos/endereços absolutos HMI↔PLC e solução de problemas de textos em vermelho |
| `docs/mcp-ide-and-tool-visibility.md` | MCP independente do IDE; fonte oficial da lista de ferramentas |
| `docs/optional-reference-materials.md` | Uso em conjunto com o projeto de referência do repositório |
| `docs/plc-network-patterns-expanded.md` | Formas ampliadas de escrever redes e instruções PLC |

## Um. Verificação do ambiente

```text
Bootstrap
Connect
GetState
```

Itens verificados:

- O TIA Portal pode ser conectado.
- O usuário possui permissões do Openness.
- A PublicAPI é compatível com a versão do TIA.
- A sessão atual não possui erros pendentes.

## Dois. Criação do projeto e do hardware

```text
CreateProject
AddDeviceWithFallback
AddHardwareCatalogDeviceWithProbe
ConnectDeviceNodesToProfinetSubnet
GetProjectTree
ValidateAutomationContext
```

Requisitos:

- As instâncias de CPU e HMI foram criadas com sucesso.
- A conexão PROFINET possui evidência de leitura posterior.
- `PLC software path`, `HMI software path` e o nome do PLC vêm de `GetProjectTree`.

## Três. Geração do PLC

Ordem de importação:

```text
tagtable
udt
globaldb
fc
fb
ladRecipe
externalSclExample
compile
```

Origem dos templates:

```text
templates/plc/plcbuild-json/*.json
templates/plc/lad-recipes/lad_call_recipes.json
templates/plc/scl-examples/FC_InstructionGallery.scl
```

Requisitos de execução:

1. Execute primeiro `PlcBuildAndImport(dryRun=true)` para cada template `plcbuild-json`.
2. Somente após a aprovação do dry run execute `dryRun=false`.
3. Após a importação real, execute `CompileAndDiagnosePlc`.
4. Prossiga para a geração da HMI somente quando houver 0 erros de compilação.

## Quatro. Geração da HMI

Telas:

```text
Overview
Dashboard
ControlStrip
Parameters
Trend
TagDiagnostics
Events
```

Ordem de execução:

```text
GetHmiProgramInfo
EnsureUnifiedHmiConnection
EnsureUnifiedHmiTagTable
EnsureUnifiedHmiTag
EnsureUnifiedHmiScreen
ApplyUnifiedHmiScreenDesignJson
BindUnifiedHmiTagDynamization
EnsureUnifiedHmiButtonAction
```

Requisitos:

- A conexão HMI deve usar o nó real do software PLC retornado por `GetProjectTree`, sem escrever manualmente o nome exibido na árvore. A ferramenta deduz o driver S7-1200/1500/300/400 pelo `TypeIdentifier` do dispositivo PLC e preenche `Partner`, `Station` e `Node`.
- Conforme o blueprint `tags[]`, as HMI Tags devem receber `plcTag` e `address` simultaneamente: `plcTag` é usado para a descrição simbólica e os diagnósticos de leitura; `address` vincula ao endereço absoluto padrão de acesso do `DB_HMI_Interface` (por exemplo, `%DB200.DBX0.0`).
- `DB_HMI_Interface` deve ser importado e compilado antes, mantendo `MemoryLayout=Standard` e `dbNumber=200`; caso contrário, as variáveis HMI não se conectarão de forma estável aos dados internos do PLC.
- O tamanho da tela deve ser igual ao do template.
- As ações dos botões devem usar `Down` / `Up`.
- Execute as vinculações de dinamização depois de criar os controles.

## Cinco. Validação

É obrigatório atender aos seguintes critérios:

- `GetProjectTree` consegue ler o PLC e a HMI.
- O PLC tem 0 erros de compilação.
- A tela HMI foi criada com sucesso.
- A leitura da conexão HMI mostra `CommunicationDriver` compatível com a série real do PLC; `Partner`/`Station`/`Node` deve conter pelo menos um valor real de PLC/interface PN que possa ser interpretado.
- A leitura da HMI Tag mostra `Connection=HMI_Connection_1`, e `Address` ou `LogicalAddress` é igual ao endereço `%DB200...` do blueprint.
- `ApplyUnifiedHmiScreenDesignJson` não apresenta falhas sem explicação.
- A ação do botão passa no `SyntaxCheck`.
- A vinculação de dinamização retorna sucesso ou pode ser lida posteriormente.
- `SaveProject` é executado com sucesso.

## Seis. Tratamento de falhas

| Sintoma | Tratamento |
|---|---|
| Não foi encontrado o software path | Execute `GetProjectTree` novamente; não tente adivinhar o caminho |
| Falha na importação do PLC | Volte à saída do dry run e verifique o XML gerado e o tipo de importação |
| Controle HMI não encontrado | Primeiro aplique o template da tela; depois vincule ações e dinamizações |
| HMI Tag em vermelho | Verifique a conexão, o símbolo do PLC, os membros do DB e o estado da compilação |
| Erro de compilação | Exporte os diagnósticos e corrija o template do PLC ou a ordem de importação |
