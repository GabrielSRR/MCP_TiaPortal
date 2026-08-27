# TIA Openness — Limites de Capacidade

Este documento lista o que a API pública do Siemens TIA Openness **não consegue fazer**, com base na
inspeção estática de `D:\app\TIA21\Portal V21\PublicAPI\V21\net48\*.xml`.

Se uma capacidade estiver marcada como **NÃO SUPORTADA**, não tente adicionar uma ferramenta MCP
que finja realizá-la via reflection — não existe caminho documentado. Essas
operações exigem um canal alternativo (servidor OPC UA na CPU, biblioteca de comunicação
S7, ou interação com o painel físico).

> Última verificação: 2026-05-09, contra a PublicAPI do TIA Portal V21.0

---

## Operações online: o que é suportado

| Capacidade | Tipo/Método da API | Ferramenta MCP |
|---|---|---|
| Ir para online / offline | `OnlineProvider.GoOnline / GoOffline` | `GoOnline`, `GoOffline` |
| Ler o estado da conexão (Offline/Online/Connecting/...) | `OnlineProvider.State` | `GetOnlineState` |
| Fazer download do projeto para a CPU (completo) | `DownloadProvider.Download(...)` | `DownloadToPlc` |
| Verificação de prontidão pré-download | (sonda customizada) | `CheckDownloadReadiness` |
| Comparar projeto offline com a CPU em operação | `PlcSoftware.CompareToOnline()` | `CompareSoftwareToOnline` |
| Definir senha de acesso da CPU (para módulos protegidos) | `OnlinePasswordConfiguration.SetPassword(SecureString)` | parâmetro `password` em `GoOnline` e `DownloadToPlc` |
| Ler valores da watch table online | reflection sobre `PlcWatchTableEntry` | `ReadPlcWatchTableCurrentValuesReadOnly` |
| Editar valores de modificação da watch table (definição offline) | `PlcWatchTableEntry.ModifyValue` | `SetWatchTableModifyValue` |
| Editar valores da force table (definição offline) | `PlcForceTableEntry.ForceValue` | `SetForceTableEntry` |

> Observação sobre Watch/Force: o TIA Openness expõe a **definição da tabela**, mas nenhum
> método documentado para "enviar a modificação agora" ou "aplicar o force agora" como comando
> discreto de runtime. Os valores passam a valer quando o TIA Portal está online e
> o gatilho da tabela dispara. Se você precisa de escrita precisa em runtime, use OPC UA.

---

## Operações online: NÃO suportadas via Openness

Estas foram investigadas e **não estão presentes** no XML da PublicAPI V21:

| Capacidade | O que foi pesquisado | Alternativa |
|---|---|---|
| **Ler o modo de operação da CPU (RUN/STOP/STARTUP)** | `CpuOperatingState`, `OperatingMode`, `RequestStateChange` — nada encontrado | Cliente OPC UA; ou leitura no painel físico |
| **Alterar o modo de operação da CPU (Run/Stop)** | `Run()`, `Stop()`, `RequestStateChange()` nos providers online — nada encontrado | Cliente OPC UA; manualmente pela interface do TIA Portal |
| **Limpar todos os forces / remover force** | `ClearForces`, `Unforce`, `RemoveForce` — nada encontrado | Excluir as entradas da force table pelo projeto e então fazer download |
| **Ler o buffer de diagnóstico / de falhas** | `DiagnosticBuffer`, `FaultBuffer`, `DiagnosticEntry` — nada encontrado em nenhum XML | Namespace `Server` do OPC UA; ou requisição SZL via S7 |
| **Download seletivo por bloco** | `DownloadSelectionConfiguration` existe, mas não há API de filtro documentada | Use o `DownloadToPlc` completo; sondagem via reflection é frágil |

Se um usuário pedir qualquer uma destas, o servidor MCP deve recusar educadamente com um
ponteiro para este documento, e **não** falhar silenciosamente nem retornar um
"sucesso" enganoso. Não implemente stubs baseados em reflection que aparentem funcionar.

---

## Operações de hardware: NÃO suportadas

| Capacidade | Situação |
|---|---|
| Ler remotamente o status dos LEDs de diagnóstico da CPU | Não exposto |
| Ler a saúde dos slots de módulo (online) | Não exposto |
| Identificar nós PROFINET online a partir de uma varredura de descoberta | Limitado; apenas o que está na configuração de hardware do projeto |

---

## Quando sugerir OPC UA no lugar

A API do TIA Openness é fundamentalmente uma API de **engenharia / modificação de projeto**.
Ela modela "o projeto que estou editando no TIA Portal", e não "a CPU rodando
neste momento". Quando um usuário pedir dados de runtime (valor atual de uma variável, estado
RUN, alarmes, histórico de diagnóstico), redirecione-o para:

1. Habilitar o servidor OPC UA da CPU (ferramenta MCP `SetOpcUaInterfaceEnabled`)
2. Conectar com um cliente OPC UA (componente separado, não este servidor MCP)

Essa fronteira é intencional — a Siemens publica o OPC UA como canal de dados de runtime
e a Openness como canal de engenharia.

---

## Como manter este documento atualizado

Quando uma nova versão do TIA Portal for lançada:

1. Rode novamente a inspeção estática da API contra o novo diretório `PublicAPI\V<n>\net48`
2. Compare (diff) com as listas atuais de "suportado" / "não suportado"
3. Atualize este arquivo antes de anunciar suporte à versão

Padrões de busca que se mostraram úteis (aplique sobre os arquivos `*.xml`):

- `OperatingState|OperatingMode|RunStop|RequestStateChange` — modo da CPU
- `ForceValue|ModifyValue|ClearForce|ApplyForce` — force/watch
- `CompareToOnline|CompareTo` — APIs de comparação
- `OnlinePassword|SetPassword|OnlineCredentials` — autenticação
- `DiagnosticBuffer|FaultBuffer|DiagnosticEntry` — diagnóstico
- `DownloadSelectionConfiguration|DownloadConfiguration` — configurações de download
