# Extensão do programa PLC: padrões de redes e instruções

Esta página complementa `docs/basic-plc-template-library.md` e `tools/tiaportal-mcp/skill/SKILL.md` (LAD §9–11, SCL §10) com **estruturas de rede comuns** e **direções para instruções avançadas**, facilitando ampliar “trechos de programa” em `PlcBuildAndImport` / `ImportBlock` / SCL externo sem acumular repetições sem utilidade.

## 1. LAD: padrão recomendado de divisão de redes

| Seção da rede | Conteúdo típico | Instruções sugeridas |
|---|---|---|
| Habilitação e intertravamento | Parada de emergência, modo e permissões | Contatos em série → `Coil` / `SCoil` / `RCoil` |
| Valores analógicos/limitação | Setpoint, limites superior e inferior | `Gt`/`Lt`/`Move`/`Add`/`Sub`/`Mul`/`Div` |
| Temporização e flancos | Debounce e pulsos | **TON/TOF/TP** somente em **FB.Static** ou **DB global** (consulte SKILL: não colocar em FC.Temp com F-CPU) |
| Cadeia de comparações | Vários limiares | Combinação de `Eq`/`Ne`/`Ge`/`Le` + bloco OR `O` |
| Conversão de tipos | Inteiro↔real | `Convert` (`SrcType/DestType`) |

**Sugestão de extensão**: com base nos `MCPVerify_FC_LAD*.xml` existentes, **copie-renomeie-altere os operandos** por rede para acrescentar redes independentes de “retenção de alarme”, “contador de horas de operação” e “matriz de intertravamento”, com uma única responsabilidade por rede.

## 2. SCL: DSL de `PlcBuildAndImport` e o que está “fora da DSL”

- A DSL oferece suporte a: `assignment`, `if`/`else`/`endif`, `line` (token livre) e `elsif` (condição como **um único Bool**).
- **Não oferece suporte** a: `FOR`/`WHILE`/`CASE` etc. Use **`.scl` externo + ImportPlcExternalSource + Generate** ou escreva no TIA e depois use `ExportBlock`.

**Sugestão de extensão**: divida o processo em vários **FCs** — `FC_AlarmLatch`, `FC_ScaleReal`, `FC_Ramp`… — com 30–80 linhas de SCL cada, e chame-os sequencialmente no OB/Main. Isso facilita compilação e download em comparação com uma lógica gigante em um único FC.

## 3. Uso em conjunto com o projeto de referência (`reference`)

Abra `reference\Siemens Standard Template V5_V21\*.ap21` etc. no TIA e pesquise:

- usos de blocos como `TON`, `CTU`, `MOVE`, `SEL`, `LIMIT`, `NORM_X` e `SCALE_X`;
- alarmes multilíngues e estruturas de DB de interfaces de objetos tecnológicos.

Alinhar os **nomes dos membros do DB de interface** com `templates/plc/plcbuild-json/db_hmi_interface.json` reduz ambiguidades de símbolos na vinculação HMI.

## 4. Blocos existentes no blueprint e incrementos sugeridos

| Existente (`templates/plc/plcbuild-json`) | Direção de incremento |
|---|---|
| `fb_timer_counter_demo` | Adicionar **cascata de CTU** e fazer o valor predefinido vir do DB HMI |
| `fb_step_sequence_demo` | Adicionar **etapa intertravada**, etapa com timeout e etapa de alarme |
| `fc_math_compare_demo` | Adicionar **cadeia de comparações Real** + modo de banda morta `ABS` (implementado em SCL) |

Os incrementos específicos em JSON dependem do processo do projeto; esta página define apenas os princípios de **estrutura e seleção de instruções**, evitando gerar, em nome da automação, um “bloco único” de milhares de linhas impossível de manter.
