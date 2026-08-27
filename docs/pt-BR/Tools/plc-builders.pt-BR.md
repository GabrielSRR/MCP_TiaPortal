# Ferramentas MCP de builders PLC

ID do documento: `plc-builders`

Este é o contrato estável das ferramentas de geração de XML PLC expostas pelo servidor TIA MCP. Todas foram projetadas para os formatos XML do TIA Portal V21:

- ferramentas de construção são offline e retornam somente strings XML;
- `PlcBuildAndImport` usa `dryRun=true` por padrão: gera XML, grava um arquivo temporário, classifica-o e retorna um plano de importação;
- gravações reais no TIA ocorrem apenas com `dryRun=false`, depois de resolver `softwarePath` e grupos por `GetProjectTree`/`ValidateAutomationContext`;
- importar não comprova compilação; mantenha `compileAfter=true`, salvo motivo específico;
- não use endereços ou membros DB presumidos para integração HMI/PLC; use símbolos exportados ou um mapeamento explícito.

## Seleção de ferramentas

Use builders offline quando precisar de XML para revisão, relatórios ou importação posterior:

| Ferramenta | Escopo | Grava no projeto |
|---|---|---|
| `BuildPlcUdtXml` | UDT / `SW.Types.PlcStruct` | Não |
| `BuildPlcTagTableXml` | Tabela de tags / `SW.Tags.PlcTagTable` | Não |
| `BuildPlcGlobalDbXml` | Global DB / `SW.Blocks.GlobalDB` | Não |
| `BuildStructuredTextXml` | Fragmento SCL `StructuredText/v4` | Não |
| `BuildFlgNetCallXml` | Rede de chamada FC LAD `FlgNet/v5` | Não |
| `ComposePlcFcBlockXml` | XML de bloco FC SCL | Não |
| `ComposePlcFbBlockXml` | XML de bloco FB SCL, sem DB de instância | Não |

Use `PlcBuildAndImport` para gerar e preparar o caminho de importação em uma única chamada:

| Modo | Comportamento |
|---|---|
| `dryRun=true` | Gera XML, grava arquivo temporário, classifica e retorna objetos descobertos; não conecta nem grava no TIA. |
| `dryRun=false` | Gera XML, grava arquivo temporário, importa conforme o tipo e pode compilar; exige projeto conectado e caminhos verificados. |

## BuildPlcUdtXml

Entrada:

```json
{
  "members": [
    { "name": "FaultActive", "datatype": "Bool", "externalWritable": true, "commentZhCn": "故障激活" },
    { "name": "FaultCode", "datatype": "Int", "commentZhCn": "故障代码" }
  ]
}
```

`members[]` deve conter pelo menos um membro; cada membro exige `name` e `datatype` (por exemplo, `Bool`, `Int`, `Real` ou `"MyUDT"`). `externalWritable` e `commentZhCn`/`comment` são opcionais.

## BuildPlcTagTableXml

Entrada:

```json
{
  "tableName": "StartStop",
  "tags": [
    { "name": "StartPB", "dataTypeName": "Bool", "logicalAddress": "%I0.0" },
    { "name": "RunOut", "dataTypeName": "Bool", "logicalAddress": "%Q0.0" }
  ]
}
```

Aliases: `tableName`→`name`, `dataTypeName`→`datatype`/`dataType`, `logicalAddress`→`address`. Cada tag exige nome, tipo e endereço lógico absoluto iniciado por `%`.

## BuildPlcGlobalDbXml

Use `dbName` (ou `name`), `dbNumber` (ou `number`) e `staticMembers` (ou `members`). Cada membro pode ter `name`, `datatype`, `externalWritable`, `commentZhCn` e `startValue`.

## BuildStructuredTextXml

Entrada:

```json
{
  "operations": [
    { "op": "if", "condition": "Start" },
    { "op": "assignment", "target": "Run", "value": "TRUE", "indent": 2 },
    { "op": "else" },
    { "op": "assignment", "target": "Run", "value": "FALSE", "indent": 2 },
    { "op": "endif" }
  ]
}
```

Operações: `if`/`ifheader` (`IF ... THEN`), `else`, `endif`/`end_if` (`END_IF;`), `assignment`/`assign` (`target := value;`), `token`, `blank` e `newline`. Use `innerOnly=true` ao incorporar o resultado em `ComposePlcFcBlockXml`.

## BuildFlgNetCallXml

`callName` (ou `name`) define a chamada. Variáveis globais usam `symbolPath[]` ou `symbol`/`path`/`plcTag` pontilhado; constantes usam `sourceKind=constant` e `value`; `section` normalmente é `Input` ou `Output`.

```json
{
  "callName": "Limit_Protect",
  "parameters": [
    { "name": "Current_Location", "section": "Input", "dataType": "Real", "symbol": "DB_Axis.Actual.Position" },
    { "name": "Enable", "section": "Input", "dataType": "Bool", "sourceKind": "constant", "value": "1" },
    { "name": "Fault", "section": "Output", "dataType": "Bool", "symbolPath": ["DB_Axis", "Fault"] }
  ]
}
```

## ComposePlcFcBlockXml / ComposePlcFbBlockXml

Defina `blockName`/`name`, `blockNumber`/`number`, interfaces e `structuredText.operations[]` ou `structuredTextInnerXml`. Para FB, as seções são `inputs[]`, `outputs[]`, `inouts[]`/`inOuts[]`, `statics[]`/`staticMembers[]` e `temps[]`/`tempMembers[]`. O builder de FB não cria DB de instância: importe, compile e crie/regere DBs por fluxo verificado separado.

## PlcBuildAndImport

Fluxo real:

1. `Connect`
2. `GetProjectTree`
3. `ValidateAutomationContext`
4. Resolva `softwarePath` e o grupo-alvo.
5. Execute `PlcBuildAndImport(..., dryRun=true)` e inspecione `WrittenFiles`/`Discovered*`.
6. Execute `dryRun=false, compileAfter=true`.
7. Verifique `Failed` e `Compile.ErrorCount`.
8. Salve somente após compilação e leitura posterior bem-sucedidas.

Tipos suportados:

| `kind` | XML classificado | Importação |
|---|---|---|
| `udt` | `SW.Types.PlcStruct` | `ImportType` |
| `tagtable` | `SW.Tags.PlcTagTable` | `ImportPlcTagTable` |
| `globaldb` | `SW.Blocks.GlobalDB` | `ImportBlock` |
| `fc` | `SW.Blocks.FC` | `ImportBlock` |
| `fb` | `SW.Blocks.FB` | `ImportBlock` |

Ainda não suportados pelo builder de uma etapa: `ob`, `instanceDb` e edição parcial de redes. Para esses artefatos, use as ferramentas explícitas de importação com exports TIA verificados.
