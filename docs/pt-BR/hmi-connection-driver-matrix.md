# Tabela de seleção do driver de conexão HMI

## 0. Pré-requisito: painel clássico vs. Unified (limites de capacidade; leia antes de escolher o painel)

**A automação completa de HMI deste conjunto de MCP (conexão + vinculação de variáveis + telas) funciona somente com painéis WinCC Unified.**

| Tipo de painel | Criação da conexão | Vinculação de variáveis | Geração de telas | Conclusão |
|---|---|---|---|---|
| **WinCC Unified** (como MTP700 Unified Basic `6AV2 123-3GB32-0AW0`) | ✅ `EnsureUnifiedHmiConnection` | ✅ `EnsureUnifiedHmiTag` (com endereço absoluto) | ✅ `ApplyUnifiedHmiScreenDesignJson` | **Automação completa de ponta a ponta** |
| **Painel clássico / básico / comfort** (KTP Basic, TP/KTP Comfort) | ❌ O Openness não expõe o serviço `CommunicationConnections` | ❌ Sem uma conexão integrada, nenhum símbolo do PLC pode ser resolvido | ❌ A importação de XML de telas é muito frágil (`IOField.set_Visible`, `PropertyComposition.Create` e outras propriedades são rejeitadas) | **Não é possível automatizar completamente**; é necessário criar a conexão/importar o template pela interface gráfica |

> **Regra obrigatória para o modelo que faz a chamada**: se o usuário não especificar obrigatoriamente um painel clássico e precisar “criar a HMI automaticamente”, **selecione um painel Unified já na etapa `AddDevice`**. Não selecione KTP Basic para depois tentar criar a conexão automaticamente — esse caminho não funciona nesta build e só causará falhas repetidas.
> Se o local exigir um painel clássico: crie a conexão manualmente na visualização de rede do TIA (cerca de 15 segundos) ou exporte um XML de template com `ExportHmiConnection` a partir de um projeto que já tenha uma conexão e depois use `ImportHmiConnection`; as variáveis podem ser importadas via XML usando **endereços absolutos** (consulte `hmi-plc-tag-binding-and-addressing.md`).

---

Este arquivo apresenta as regras para o valor de **CommunicationDriver** ao usar `EnsureUnifiedHmiConnection` ou criar uma conexão HMI no TIA. Um driver incorreto pode fazer com que toda a coluna de variáveis HMI fique em vermelho, que não haja valores em runtime ou que a conexão apareça como “não conectada”.

## Regras de seleção

| Série da CPU PLC | Prefixo típico do número de pedido | `CommunicationDriver` (contém a substring) |
|---|---|---|
| S7-1500 | `6ES7 5xx-…` | `SIMATIC S7 1500` |
| S7-1200 | `6ES7 21x-…` | `SIMATIC S7 1200` |
| S7-300 | `6ES7 31x-…` | `SIMATIC S7 300/400` |
| S7-400 | `6ES7 41x-…` | `SIMATIC S7 300/400` |
| CPU SIMATIC ET 200SP | `6ES7 51x-…` | `SIMATIC S7 1500` |
| SoftPLC / S7-PLCSIM Adv. | (alvo de simulação) | `SIMATIC S7 1500` ou `SIMATIC S7 1200` (conforme o tipo de CPU simulada) |

Método de correspondência: o MCP deduz a série usando o “número de pedido” no `TypeIdentifier` do dispositivo PLC. **Atenção**: no catálogo do TIA, o número de pedido normalmente contém espaços (por exemplo, `6ES7 211-1BE40-0XB0`). Implementações antigas que verificavam apenas `6ES721…`, sem espaços, classificavam incorretamente como UNKNOWN; a conexão continuava mostrando o driver padrão **S7-300/400**. Isso já foi corrigido no código-fonte, em `Portal.cs` → `InferUnifiedPlcFamilyFromSoftwarePath`, removendo os espaços antes da comparação. **Recompile `TiaMcpServer.exe` e substitua o executável de mesmo nome no pacote de entrega** (ou use a saída Release recém-gerada em `tools/tiaportal-mcp` no repositório).

Se ainda for selecionado o padrão `SIMATIC S7 300/400`, **altere manualmente no TIA** para o driver correspondente e use `DescribeObject` para ler e validar o resultado.

## Consulta rápida da causa (S7-1200 exibido como 300/400)

| Causa | Explicação |
|---|---|
| Número de pedido com espaços | `TypeIdentifier` contém `6ES7 211…` em vez de `6ES7211…`; a lógica antiga não reconhecia → atualize o executável do MCP (veja acima) |
| Sub-rede PN não conectada | Afeta somente o online; nem sempre altera a exibição do driver, mas as variáveis ficam vermelhas | Use `ConnectDeviceNodesToProfinetSubnet` ou conecte a sub-rede manualmente |
| Diferença de nomes de enumeração por região | Em poucas instalações, a gravação da string falha | Selecione o driver manualmente no TIA uma vez |

## Parâmetros principais

| Campo | Regra de preenchimento |
|---|---|
| `Partner` | Nome do dispositivo PLC (igual ao nome do nó `Devices` em `GetProjectTree`, por exemplo, `PLC_Main`) |
| `Station` | Em projetos com várias CPUs, selecione a Station onde a CPU está localizada |
| `Node` | Nome da interface PROFINET, por exemplo, `PROFINET interface_1` |
| `InitialAddress` | IP da porta PN do PLC, por exemplo, `192.168.0.1` (leitura online) |
| `CommunicationDriver` | Consulte a tabela acima |

## Lista de verificação

1. `DescribeObject(HmiConnection)` retorna um nome de `CommunicationDriver` contendo a substring correta.
2. As portas PN da HMI e do PLC estão na **mesma sub-rede** (`ConnectDeviceNodesToProfinetSubnet`).
3. O PLC foi compilado com sucesso; o DB referenciado pelas tags HMI existe e foi compilado.
4. O DB de interface HMI usa acesso **não otimizado (Standard)**, permitindo endereçamento absoluto.

## Incompatibilidades comuns

| Sintoma | Causa | Tratamento |
|---|---|---|
| Toda a coluna em vermelho | O driver foi definido como `SIMATIC S7 300/400`, mas o PLC é 1200/1500 | No TIA, altere `CommunicationDriver` para o item correspondente, salve e leia novamente |
| Apenas algumas Tags em vermelho | Endereço fora dos limites / número do DB ou deslocamento de bytes incorreto | Verifique novamente o tamanho das palavras `DBn.DBW/DBD` e o alinhamento |
| Conexão cinza | Os três campos `Partner`/`Station`/`Node` não foram preenchidos | Recrie `EnsureUnifiedHmiConnection` ou complete os campos no TIA |
