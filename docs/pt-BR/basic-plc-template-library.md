# Instruções e descrição dos templates de PLC

Este documento deve ser usado em conjunto com `templates/plc/` para gerar estruturas genéricas de programas PLC. Os templates abrangem SCL, redes de chamada LAD, tabela de variáveis, UDT, Global DB, FC, FB e DB de interface HMI.

## Conteúdo abrangido

| Categoria | Conteúdo |
|---|---|
| Lógica booleana | `AND`, `OR`, `NOT`, atribuição, retenção, reset |
| Ramificações | `IF / ELSIF / ELSE`, `CASE` |
| Temporização | Estrutura de chamada `TON`, bit de conclusão do atraso |
| Contagem | Detecção de flanco de subida, acumulação, reset, alcance do valor predefinido |
| Aritmética | Adição, subtração, multiplicação, divisão, erro, valor absoluto |
| Comparação | `=`, `<>`, `>`, `>=`, `<`, `<=` |
| Limitação | `LIMIT`, verificação de faixa |
| Conversão de tipos | `INT_TO_DINT`, `DINT_TO_REAL`, `REAL_TO_DINT`, `BOOL_TO_DINT` |
| Loops | `FOR` |
| Estruturas de dados | Tabela de tags, UDT, Global DB, DB de interface HMI |
| LAD | Receitas de redes de chamada `BuildFlgNetCallXml` e exemplos XML validados |

## Ordem de importação recomendada

```text
tagtable_basic_signals.json          (PlcBuildAndImport, tagtable)
udt_basic_status.json                (PlcBuildAndImport, udt)
db_basic_status.json                 (PlcBuildAndImport, globaldb)
db_hmi_interface.json                (PlcBuildAndImport, globaldb)
lad-recipes/lad_call_recipes.json    (BuildFlgNetCallXml)
scl-examples/FC_InstructionGallery.scl   (importação de SCL externo)
scl-examples/FC_BasicScaleLimit.scl      (importação de SCL externo)
scl-examples/FC_MathCompareDemo.scl      (importação de SCL externo)
scl-examples/FB_BasicLatch.scl           (importação de SCL externo)
scl-examples/FB_TimerCounterDemo.scl     (importação de SCL externo)
scl-examples/FB_StepSequenceDemo.scl     (importação de SCL externo)
```

> **FC/FB devem sempre usar SCL externo, não DSL.** A DSL de `PlcBuildAndImport(kind=fc|fb)` aceita apenas nomes de variáveis simples em `condition`/`source`; ela não consegue interpretar expressões como `Setpoint - Actual`, `Disable OR FaultLatch`, `ABS(...)` ou `CASE` (a compilação gera o erro `Tag not defined`). Portanto, FC/FB que contenham expressões aritméticas, comparações, funções ou `CASE` devem ser convertidos para fontes SCL nativas em `scl-examples/*.scl` e importados por meio de `ImportPlcExternalSource` + `GenerateBlocksFromExternalSource`. Os arquivos antigos `plcbuild-json/fc_*.json` e `fb_*.json` foram descontinuados (foram mantidos e marcados como `_deprecated`; não use mais sua forma de expressão).

Cada arquivo em `plcbuild-json/*.json` (somente `tagtable`/`udt`/`globaldb`) contém:

```json
{
  "kind": "globaldb",
  "tool": "PlcBuildAndImport",
  "json": {}
}
```

Ao chamar a ferramenta, serialize o campo `json` como uma string e passe-o a `PlcBuildAndImport`. Arquivos `.scl` de FC/FB são importados diretamente como fontes externas e não precisam ser serializados.

## Validação

- Execute primeiro `dryRun=true` para todos os templates.
- Após a importação real, execute `CompileAndDiagnosePlc`.
- Salve o projeto somente depois que o número de erros de compilação for 0.
- As variáveis HMI devem estar vinculadas a uma tag do PLC ou a um membro de `DB_HMI_Interface`.
- Use redes de chamada LAD para organizar as relações entre chamadas; não escreva manualmente árvores de redes complexas.

## Leitura adicional

- **`docs/plc-network-patterns-expanded.md`**: segmentação em várias redes, regras para posicionamento de temporizadores/flancos e divisão de responsabilidades entre SCL e LAD; use-o para transformar trechos de programa de “nível demonstrativo” em “nível de engenharia”.
