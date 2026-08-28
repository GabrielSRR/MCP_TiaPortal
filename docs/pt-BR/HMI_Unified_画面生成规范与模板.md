# Especificação de geração de telas WinCC Unified

Esta especificação é usada para gerar telas, tags, ações de botões e vinculações de dinamização do WinCC Unified. Os templates estão em `templates/hmi/`; todos são `designJson` legíveis, editáveis e diretamente aplicáveis.

> ⚠️ **Escopo (leia primeiro)**: a capacidade **totalmente automática** de telas/tags/conexões desta coleção existe **somente para painéis WinCC Unified**. A conexão PLC↔HMI, a vinculação de variáveis e a importação de telas de painéis clássicos/básicos/comfort (KTP Basic, TP/KTP Comfort) **não podem ser concluídas automaticamente via Openness** (`CommunicationConnections` não é exposto). Se o projeto exigir automação de ponta a ponta, **selecione um painel Unified já na configuração do hardware** (por exemplo, `MTP700 Unified Basic 6AV2 123-3GB32-0AW0`). Consulte `docs/hmi-connection-driver-matrix.md`.

A relação entre variáveis HMI e PLC (símbolos/endereços absolutos e solução de problemas de textos em vermelho) está em **`docs/hmi-plc-tag-binding-and-addressing.md`** (independente do IDE e aplicável a todos os clientes MCP).

## Ordem de geração

```text
GetProjectTree
GetHmiProgramInfo
EnsureUnifiedHmiConnection
EnsureUnifiedHmiTagTable
EnsureUnifiedHmiTag
EnsureUnifiedHmiScreen
ApplyUnifiedHmiScreenDesignJson
BindUnifiedHmiTagDynamization
EnsureUnifiedHmiButtonAction
SaveProject
```

## Contrato de `designJson`

- Chaves de nível superior: `screen`, `items`.
- Cores: `0xAARRGGBB`.
- Campos comuns dos controles: `type`, `name`, `left`, `top`, `width`, `height`.
- Controles comuns: `Rectangle`, `Text`, `Button`, `IOField`.
- **Rótulos de texto (títulos, nomes de campos e textos explicativos) devem usar `Text` (correspondente a `HmiText`)**. `Rectangle` **não possui a propriedade Text**; escrever texto em um retângulo causa **falha silenciosa e deixa o rótulo em branco** — retângulos servem apenas para lâmpadas de status, bases ou blocos de fundo. Botões e IOFields podem ter texto próprio, sem necessidade de um `Text` adicional.
- Os nomes dos controles devem ser exclusivos na mesma tela.
- `width`/`height` de `EnsureUnifiedHmiScreen` devem corresponder às dimensões do template.

## Arquivos de template

| Arquivo | Dimensões | Descrição |
|---|---:|---|
| `unified_overview_1280x800.json` | 1280 x 800 | Visão geral, navegação, comandos, status, área de processo e resumo de eventos |
| `unified_basic_dashboard_1024x768.json` | 1024 x 768 | Dashboard |
| `unified_control_strip_1024x768.json` | 1024 x 768 | Barra de controle |
| `unified_parameter_page_1024x768.json` | 1024 x 768 | Página de parâmetros |
| `unified_trend_page_1024x768.json` | 1024 x 768 | Página de tendências |
| `unified_basic_tag_diagnostics_1024x768.json` | 1024 x 768 | Diagnóstico de tags |
| `unified_basic_event_log_1024x768.json` | 1024 x 768 | Lista de eventos |

## Ações dos botões

Ações de alto nível validadas:

| Ação | Evento | Descrição |
|---|---|---|
| `set-bit` | `Down` | Define o bit ao pressionar |
| `reset-bit` | `Up` | Reseta o bit ao soltar |
| `toggle-bit` | `Down` ou `Up` | Inverte o bit |

Comandos recomendados:

| Botão | HMI Tag |
|---|---|
| `Btn_Enable` / `Btn_Start` | `HMI_CmdEnable` |
| `Btn_Disable` / `Btn_Stop` | `HMI_CmdDisable` |
| `Btn_Reset` | `HMI_CmdReset` |
| `Btn_Apply` | `HMI_CmdApply` |

## Dinamização

| Controle | Propriedade | HMI Tag |
|---|---|---|
| `Lamp_Active` / `Lamp_Run` | `BackColor` | `HMI_StatusActive` |
| `Lamp_Error` / `Lamp_Fault` | `BackColor` | `HMI_StatusError` |
| `IO_Setpoint` | `ProcessValue` | `HMI_ValueSetpoint` |
| `IO_Actual` | `ProcessValue` | `HMI_ValueActual` |
| `IO_Output` | `ProcessValue` | `HMI_ValueOutput` |
| `IO_OutputMin` | `ProcessValue` | `HMI_OutputMin` |
| `IO_OutputMax` | `ProcessValue` | `HMI_OutputMax` |
| `IO_CounterPreset` | `ProcessValue` | `HMI_CounterPreset` |

## Padrão visual

- Use fundo escuro na barra superior e título branco.
- O fundo da página principal deve ser cinza-claro e os cartões devem ter fundo branco.
- Use bordas cinza-claro nos cartões e evite grandes áreas com cores muito saturadas.
- A altura dos botões não deve ser inferior a 42 px; para botões importantes, recomenda-se mais de 48 px.
- Use fundos verde-claro, vermelho-claro e amarelo-claro nas lâmpadas de status, com texto escuro.

## Validação

- `ApplyUnifiedHmiScreenDesignJson` não apresenta falhas sem explicação.
- Os controles podem ser lidos posteriormente.
- A tabela de HMI Tags existe e as tags podem ser lidas.
- As ações dos botões passam no `SyntaxCheck`.
- A vinculação de dinamização pode ser lida ou retorna um status de sucesso explícito.
