# Biblioteca de instruções LAD (referência neutra)

Este arquivo reúne instruções, pinos, operandos e formas de conexão comuns em redes LAD (diagrama de contatos), em conjunto com o registro de `Part Name` validado em `tools/tiaportal-mcp/skill/SKILL.md`. Todos os exemplos usam sintaxe genérica e não estão vinculados a um processo específico.

## 1. Princípios de divisão das redes

Normalmente, um CompileUnit corresponde a uma rede. Recomenda-se dividir por responsabilidade:

| Tipo de seção | Finalidade |
|---|---|
| Habilitação e intertravamento | Parada de emergência, modo e condições de intertravamento |
| Pré-processamento de entradas | Escalonamento e filtragem de valores analógicos |
| Tratamento de comandos | Comandos de partida/parada, set/reset |
| Lógica principal do processo | Sequenciamento, temporização e contagem |
| Mapeamento de saídas | Saídas de comando e de alarme |
| Diagnóstico | Palavra de status e código de erro |

## 2. Contatos e bobinas

| Nome | Part Name | Pinos |
|---|---|---|
| Contato normalmente aberto | `Contact` | `in`, `out`, `operand` |
| Contato normalmente fechado | `Contact` + `<Negated Name="operand"/>` | iguais aos anteriores |
| Bobina de saída | `Coil` | `in`, `operand` |
| Bobina de set | `SCoil` | `in`, `operand` |
| Bobina de reset | `RCoil` | `in`, `operand` |
| Paralelo (OR) | `O` (`TemplateValue Card=2`) | `in1`/`in2`/.../`out` |

## 3. Detecção de flancos

| Nome | Part Name | Observação |
|---|---|---|
| Flanco de subida | `PBox` | Requer duas cópias de `IdentCon` com o mesmo operando (dois `Access`/`UId`) |
| Flanco de descida | `NBox` | igual ao anterior |

## 4. Comparação

| Nome | Part Name | Valor do template | Pinos |
|---|---|---|---|
| Igual a | `Eq` | `SrcType=Int/DInt/Real/...` | `pre`, `in1`, `in2`, `out` |
| Diferente de | `Ne` | igual ao anterior | iguais aos anteriores |
| Maior que | `Gt` | igual ao anterior | iguais aos anteriores |
| Maior ou igual a | `Ge` | igual ao anterior | iguais aos anteriores |
| Menor que | `Lt` | igual ao anterior | iguais aos anteriores |
| Menor ou igual a | `Le` | igual ao anterior | iguais aos anteriores |

## 5. Aritmética

| Nome | Part Name | Valor do template | Pinos |
|---|---|---|---|
| Adição | `Add` | `SrcType` + `Card` | `en`, `eno`, `in1`, `in2`, `out` |
| Subtração | `Sub` | igual ao anterior (recomenda-se adicionar `DisabledENO="true"`) | iguais aos anteriores |
| Multiplicação | `Mul` | `SrcType` + `Card=2` | iguais aos anteriores |
| Divisão | `Div` | igual ao anterior | iguais aos anteriores |
| Módulo | `Mod` | `SrcType=Int/DInt` | iguais aos anteriores |
| Valor absoluto | `Abs` | `SrcType=Int/DInt/Real` | `en`, `eno`, `in`, `out` |
| Negação | `Neg` | igual ao anterior | iguais aos anteriores |

## 6. Transferência e conversão de dados

| Nome | Part Name | Observação |
|---|---|---|
| Transferência | `Move` | `TemplateValue Card=1` |
| Conversão de tipo | `Convert` | `TemplateValue SrcType`, `DestType` |
| Serialização/desserialização | `Serialize` / `Deserialize` | Em nível de byte |
| Dispersar/agrupar | `SCATTER` / `GATHER` | Bits/campos |

## 7. Temporizadores (IEC)

| Nome | Part Name |
|---|---|
| Retardo na energização | `TON` |
| Retardo na desenergização | `TOF` |
| Pulso único | `TP` |

Os temporizadores exigem instâncias:

- recomenda-se declará-las na seção **FB Static**, usando os tipos `TON_TIME` / `TOF_TIME` / `TP_TIME`;
- também é possível usar um **DB global independente**, referenciado no LAD por `<Instance Scope="GlobalVariable">`;
- a área Temp de um FC padrão de uma F-CPU **não permite** colocar diretamente instâncias de temporizadores IEC.

## 8. Contadores (IEC)

| Nome | Part Name |
|---|---|
| Contagem crescente | `CTU` |
| Contagem decrescente | `CTD` |
| Contagem crescente/decrescente | `CTUD` |

## 9. Bloco de expressões Calc

`Calc` é usado para escrever, dentro de um bloco, expressões combinadas com vários operandos:

- valores do template: `Card` (quantidade de operandos), `SrcType`, `<Equation>...</Equation>`;
- em redes extensas, é mais compacto que encadear `Add/Sub/Mul/Div`.

## 10. Observações sobre XML

Consulte `tools/tiaportal-mcp/skill/SKILL.md` §9–§11:

- os `UId` dentro de `<FlgNet>` devem ser decimais;
- remova todos os comentários XML `<!-- -->`;
- escape `&`, `<` e `>` dentro de `<Text>` / comentários;
- `<ProgrammingLanguage>` aparece tanto no **nível do bloco** quanto em cada **CompileUnit**;
- em caso de falha na importação, verifique primeiro o trecho final da cadeia de exceções fornecida por `Portal.cs::UnwrapImportError`.

## 11. Templates e exemplos

| Arquivo | Conteúdo |
|---|---|
| `tools/tiaportal-mcp/skill/lad-cookbook/MCPVerify_FC_LAD.xml` | Contatos/bobinas/comparação/transferência básicos |
| `tools/tiaportal-mcp/skill/lad-cookbook/MCPVerify_FC_LAD_v2.xml` | Aritmética, conversões e contatos negados |
| `tools/tiaportal-mcp/skill/lad-cookbook/MCPVerify_FC_LAD_v3.xml` | Redes de comparação em FC |
| `tools/tiaportal-mcp/skill/lad-cookbook/MCPVerify_FB_LAD_v3.xml` | Instância de temporizador IEC em FB |
