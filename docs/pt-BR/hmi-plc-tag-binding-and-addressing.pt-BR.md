# Vinculação de variáveis HMI ↔ PLC (endereços absolutos por padrão)

Este pacote usa **endereços absolutos** para estabelecer a interconexão de variáveis entre o WinCC Unified e o PLC. Motivos:
- após a entrega, o **endereço absoluto é único, legível e verificável**;
- na automação MCP / Openness, a **interconexão simbólica** sofre influência de acesso otimizado, driver de comunicação e resolução de nomes, entre outros; a probabilidade de textos em vermelho é maior;
- endereços absolutos exigem um DB global do PLC com **acesso não otimizado**, de acordo com a prática usual de entrega da equipe.

## 1. Pré-requisitos

| Item | Valor |
|---|---|
| DB de interface HMI | Nome: `DB_HMI_Interface`, número: `200`, **`MemoryLayout = Standard` (não otimizado)** |
| Layout de bytes | Consulte a seção `absoluteLayout` de `templates/plc/plcbuild-json/db_hmi_interface.json` |
| Driver de comunicação | Consulte `docs/hmi-connection-driver-matrix.md` |
| Sub-rede | A porta PN do PLC e a porta PN da HMI estão na mesma sub-rede PROFINET |
| Compilação | 0 erros de compilação no PLC e 0 erros de compilação na HMI |

## 1.1 `EnsureUnifiedHmiTag` do MCP e o símbolo `DB_…` (falha de implementação corrigida)

Se `plcTag` receber um **símbolo** como **`DB_HMI_Interface.CmdEnable`** (nome do bloco iniciado por letra), versões antigas do `TiaMcpServer` tratavam incorretamente “qualquer string iniciada por `DB`” como endereço absoluto. Assim, o modo de acesso era definido como **Absolute** e todo o símbolo era colocado no campo **Address**, **sem correspondência com a tabela de símbolos do PLC**; o resultado era texto em vermelho ou valor que não atualizava.

Regra correta: um **símbolo** tem o formato `DB_MyBlock.Member`; um **endereço absoluto** tem o formato `%DB200.DBX0.0` ou `DB200.DBX0.0` (`DB` seguido imediatamente por números). A verificação foi corrigida em `Portal.cs` → `BindUnifiedHmiTagToPlcSymbol`; use o `TiaMcpServer.exe` **recém-compilado**.

## 2. Lista de endereços absolutos (de acordo com o blueprint)

| HMI Tag | Tipo de dados | Endereço absoluto |
|---|---|---|
| `HMI_CmdEnable` | Bool | `%DB200.DBX0.0` |
| `HMI_CmdDisable` | Bool | `%DB200.DBX0.1` |
| `HMI_CmdReset` | Bool | `%DB200.DBX0.2` |
| `HMI_CmdApply` | Bool | `%DB200.DBX0.3` |
| `HMI_StatusActive` | Bool | `%DB200.DBX1.0` |
| `HMI_StatusError` | Bool | `%DB200.DBX1.1` |
| `HMI_StatusWarning` | Bool | `%DB200.DBX1.2` |
| `HMI_StepNo` | Int | `%DB200.DBW2` |
| `HMI_ValueSetpoint` | Real | `%DB200.DBD4` |
| `HMI_ValueActual` | Real | `%DB200.DBD8` |
| `HMI_ValueOutput` | Real | `%DB200.DBD12` |
| `HMI_OutputMin` | Real | `%DB200.DBD16` |
| `HMI_OutputMax` | Real | `%DB200.DBD20` |
| `HMI_CounterPreset` | DInt | `%DB200.DBD24` |
| `HMI_CounterValue` | DInt | `%DB200.DBD28` |

Regras de layout:

- Bool usa endereçamento por bit dentro do byte (`.0` a `.7`).
- Int ocupa 2 bytes e é alinhado por **palavra**; Real / DInt ocupam 4 bytes e são alinhados por **palavra dupla**.
- Quando houver mudança de segmento entre Bools, preserve os bits de preenchimento de alinhamento (o template já reserva `_pad1_0_4` a `_pad1_0_7`).

## 3. Criação de variáveis no MCP (endereço absoluto)

A implementação atual de `EnsureUnifiedHmiTag` aceita o parâmetro `plcTag` (símbolo). Para forçar o uso de endereços absolutos:

1. Chame `EnsureUnifiedHmiTag` para criar a variável, **sem vinculação ao PLC**: informe apenas `hmiSoftwarePath`, `tagTableName`, `tagName`, `hmiDataType` e `connectionName`.
2. Em seguida, use `InvokeObject` ou `DescribeObject` para escrever a propriedade `LogicalAddress` da HMI Tag, usando um dos valores `%DBn.DBxx.x` / `%DBn.DBWnn` / `%DBn.DBDnn` da tabela acima.
3. Use `DescribeHmiTag` para ler `LogicalAddress` e validar o resultado.

> Observação: diferentes builds do MCP podem usar nomes ligeiramente diferentes para `LogicalAddress` (como `Address` ou `PlcTagSymbolic`). Consulte `DescribeObject(HmiTag)` e selecione a propriedade de string **gravável**.

## 4. Consulta rápida de falhas

| Sintoma | Ordem de tratamento |
|---|---|
| Uma única Tag em vermelho | Verifique o tamanho do endereço e o alinhamento de bytes; confirme que o DB não otimizado não foi alterado para otimizado |
| Todas as Tags em vermelho | Verifique `CommunicationDriver`, `Partner`, `Node`, sub-rede e se o PLC está online |
| Símbolos alterados para uso no TIA | Depende dos requisitos do local; ao voltar à vinculação simbólica, confirme a estabilidade do nome do DB e dos membros |

## 5. Relação com a interconexão simbólica

A interconexão simbólica não está errada; ela apenas **não é usada por padrão**. Se a equipe precisar explicitamente dela (por exemplo, para DBs com acesso otimizado ou renomeação acompanhando os membros), é necessário:

- confirmar no TIA que os símbolos do PLC foram compilados com sucesso;
- garantir que `plcName` da HMI seja igual ao nome do nó do software PLC em `GetProjectTree`;
- testar em `DescribeHmiTag` se o estado de resolução não está mais em vermelho.

Depois dessas condições, o endereço absoluto pode ser mantido simultaneamente como campo de “contingência”, facilitando verificações posteriores.
