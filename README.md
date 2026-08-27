# Pacote Completo TIA Portal MCP (**v2.0.0** / V20+V21 + S7DCL + CLI)

[English](README.en.md) · [中文](README.md) · **Português**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/bulaofen0036-coder/TIA_Portal_Openness_MCP)](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP/releases)

> **Livre e open source (MIT):** o servidor roda **sem nenhuma license key** e **não contém qualquer código de validação de licença**.

![Diagrama de arquitetura](docs/assets/architecture.svg)

Em **Windows + TIA Portal V20 ou V21**, dirija o TIA Portal via **MCP (stdio ou HTTP)**: criar projeto, adicionar hardware, gerar PLC (Tag/UDT/DB/SCL/LAD), gerar telas e eventos do **WinCC Unified**, compilar com diagnóstico e salvar.

O pacote já inclui o **runtime compilado**, a Skill, a lista estática de ferramentas, a matriz de capacidades, templates de PLC/HMI, **blueprints de projeto legíveis** e os manuais. **Não é necessário** clonar o repositório de código-fonte.

---

## Início rápido (3 passos, sem cliente MCP)

Primeira vez? Não precisa de cliente MCP nem escrever código. Com o TIA já instalado, siga estes 3 passos e gere seu primeiro projeto em poucos minutos.

*(Quer conectar Cursor / Claude Desktop e outros clientes de IA via MCP? Pule para [Passos de instalação](#passos-de-instalação).)*

1. **Preparação:** instale TIA Portal V20 ou V21 + .NET Framework 4.8; adicione o usuário Windows atual ao grupo local **`Siemens TIA Openness`** e faça logoff/login uma vez. Use o atalho correspondente à sua versão — a raiz do pacote já traz `tia.cmd` (V21) e `tia-v20.cmd` (V20); os demais caminhos são resolvidos automaticamente.

2. **Pré-aquecimento (opcional, mas fortemente recomendado):** dê duplo clique em `scripts\prewarm.bat` e **deixe a janela aberta**. Ela mantém residente uma instância headless do TIA, fazendo cada comando seguinte conectar em ~1 segundo (sem pré-aquecimento, cada cold start leva cerca de 3 minutos). Encerre com `Ctrl+C` quando terminar.

3. **Gerar o projeto:** arraste o template `templates\project-blueprints\scaffold_spec_motor.json` (ou `scaffold_spec_start_stop.json`) sobre o ícone de `scripts\gerar-projeto.bat` — ele executa a linha completa: criar projeto → adicionar PLC/HMI → escrever blocos → compilar → salvar. **Código de saída 0 significa sucesso.**

---

## Novidades da v2.0.0 — linha de comando `tia`

> **O mesmo executável é servidor MCP e ferramenta de linha de comando.** Qualquer IA produz um spec YAML/JSON e qualquer técnico roda um único comando para criar ou alterar um projeto do zero — **sem cliente MCP e sem instalação**. Por baixo, reutiliza integralmente o mesmo motor. Detalhes em [`docs/CLI_quickstart.md`](docs/CLI_quickstart.md).

- **`tia gen <spec.yaml|json>`** — cria um projeto completo a partir do spec com um comando só (equivale a `ScaffoldProject`). Use `--dry-run` para validação offline e `--json` para saída legível por máquina.
- **`tia patch <spec>`** — aplica o spec de forma **incremental (upsert) em um projeto existente** (o `projectPath` dentro do spec aponta para o `.apXX`). Elementos não mencionados permanecem intocados; `--no-overwrite` protege blocos LAD editados manualmente.
- Também disponíveis: `tia compile / describe / export / import / prewarm / schema / version`. Códigos de saída: **0 = sucesso / 1 = houve etapas com falha / 2 = erro**.
- **Ponto de entrada `tia`:** os arquivos `tia.cmd` (V21) e `tia-v20.cmd` (V20) na raiz do pacote. Adicione a raiz ao `PATH` e rode `tia gen ...` de qualquer lugar, sem memorizar o caminho profundo do `.exe`.
- **Zero programação:** basta arrastar o spec sobre `scripts\gerar-projeto.bat` (se a V21 não existir, cai automaticamente para a V20). O `scripts\prewarm.bat` mantém uma instância headless residente para que os comandos seguintes conectem em ~1s.
- **Templates prontos para uso:** os specs de partida/parada e de motor em `templates/project-blueprints/` funcionam direto com `tia gen`. O `tia` resolve automaticamente o marcador `__BUNDLE__` para a raiz do pacote — não é preciso editar caminhos.
- **Faça qualquer IA gerar o spec:** veja [`docs/AI_spec_prompt.md`](docs/AI_spec_prompt.md) — um contrato genérico do tipo "produza um spec", que **não exige** que a IA suporte MCP.
- **Parsing duplo YAML + JSON:** JSON é preferível (zero ambiguidade), YAML é mais confortável para leitura e escrita humana. O mesmo spec produz resultado idêntico nos dois formatos.

> Continuam existindo os dois binários V20/V21 e o serviço MCP completo (o comportamento fora dos verbos `tia` não mudou). CLI e MCP compartilham o mesmo motor.

---

## Novidades da v1.0.0 (rápido, prático, à prova de erro)

- **Início headless por padrão, conexão ~10× mais rápida:** a conexão ao TIA passa a ser sem interface (`WithoutUserInterface`), derrubando o cold start de cerca de 200–340s para cerca de 10–28s. Para acompanhar visualmente o TIA, inicie o `.exe` com `--with-ui` (ou abra o `.ap21` diretamente após a geração).

- **`ScaffoldProject` — projeto completo em uma frase:** passe um `spec` JSON e uma única chamada executa "criar projeto → adicionar hardware PLC/HMI → UDT/DB/tabelas de tags → blocos SCL/LAD → compilar → conexão/telas/variáveis HMI → salvar", retornando um relatório passo a passo. Condensa um runbook de ~20 etapas em uma chamada. Use `dryRun=true` para validar o spec offline antes de executar de verdade. Templates prontos: `templates/project-blueprints/scaffold_spec_start_stop.json` (partida/parada) e `scaffold_spec_motor.json` (motor).

- **Instância residente, conexão em segundos (opcional):** deixe um terminal rodando `python scripts/prewarm_tia.py`; depois disso, cada sessão faz `Connect` em cerca de 0,8–1s.

- **Menos propenso a erro:** detecção automática do caminho do software HMI (não mais fixo em `HMI_RT_1`); timeout e descarte de instâncias TIA travadas ou órfãs durante a conexão; importação de bloco individual (`ImportFromDocuments` / `ImportBlock`) faz releitura de confirmação e retorna `Meta.verified`.

- Ferramentas consolidadas em **180** (removidas 4 variantes `Export*ToTemp` e acrescentadas descrições desambiguadoras para as ferramentas de Export/Import que se confundiam).

### Nesta atualização (em relação ao pacote 20260512)

- **Barreiras rígidas de geração estável (v0.0.39):** sobre a v0.0.38, o `PlcBuildAndImport` passa a retornar `CapabilityDecision` / `CapabilityWarnings` / `RecommendedNextActions`; o `ApplyUnifiedHmiScreenDesignJson(strict=true)` agora falha por padrão quando a escrita de propriedade HMI não é aplicada; e o `EnsureUnifiedHmiTag(requireVerifiedBinding=true)` passa a exigir por padrão a releitura confirmando `SymbolicVerified` ou `AbsoluteVerified`, evitando o problema conhecido de "gerou com sucesso, mas a variável não ficou realmente vinculada".

- **Suporte às duas versões (V20 + V21):** o pacote contém dois executáveis — `bin/Release/net48/TiaMcpServer.exe` (compilado para V21) e `bin-v20/Release/net48/TiaMcpServer.exe` (compilado para V20).
  * Eles **devem ser usados separadamente e não são intercambiáveis**: a V21 usa DLLs modulares (`Siemens.Engineering.Base` / `Step7` / ...) e a V20 usa a DLL monolítica `Siemens.Engineering.dll`; o binding difere no nível de IL.
  * Ambos aceitam o argumento `--tia-portal-location <caminho>`, combinado com `--tia-major-version <20|21>`, para instalações fora do local padrão.

- **Ferramentas de formato texto S7DCL/SCL:** em projetos V20+, as ferramentas `ExportAsDocuments` / `ExportBlocksAsDocuments` / `ImportFromDocuments` / `ImportBlocksFromDocuments` importam e exportam blocos de programa no formato texto SIMATIC SD (`.s7dcl` + `.s7res`), mais legível e mais amigável a `diff` que o XML SimaticML. As descrições trazem a marcação "PREFERRED on V21+" para orientar a IA a preferi-las.

- **Validação ponta a ponta na V21** (DemoProjects/MCP_Demo_Rich_20260523): ciclo de exportação e reimportação de 8 blocos em 14,7s.

- **Validação ponta a ponta na V20** (projeto de teste Jiangxia 5T): `CompileSoftware` → `ExportBlocksAsDocuments`, com exportação bem-sucedida de 51 arquivos `.s7dcl` e 33 `.s7res`. Blocos LAD são expressos em texto no formato `RUNG / I_Contact / Coil / TON{...}`, amigável a `diff`.

**Independente da IDE:** qualquer cliente compatível com MCP (Cursor, VS Code, Claude Desktop, cliente HTTP próprio etc.) usa o mesmo `TiaMcpServer.exe`. Se alguma IDE "não mostra determinada ferramenta", trata-se de **cache/descritor de ferramentas do cliente**, e não de recursos removidos do pacote; veja [`docs/mcp-ide-and-tool-visibility.md`](docs/mcp-ide-and-tool-visibility.md).

**Independente do repositório de código:** quem recebe o pacote só precisa descompactá-lo. Na configuração MCP, aponte o `command` para o executável dentro do pacote, em `tools\tiaportal-mcp\src\TiaMcpServer\bin\Release\net48\TiaMcpServer.exe` (veja `cursor-mcp.example.json` e substitua `REPLACE_ME` pela raiz do pacote). Se outros documentos exibirem caminhos como `…\PID博途块\…`, são apenas os diretórios de build do autor — **não é necessário** clonar aquele repositório.

---

## Passos de instalação

### 1. Preparação do ambiente

- **.NET Framework 4.8** e **TIA Portal V20 ou V21** instalados;
- Usuário atual no grupo local **`Siemens TIA Openness`**; faça logoff e login novamente;
- Localize a raiz de instalação do TIA por uma destas três vias:
  a) passe `--tia-portal-location "D:\app\TIA20\Portal V20"` ao iniciar o `.exe` (recomendado, e obrigatório em instalações fora do padrão);
  b) defina a variável de ambiente de usuário `TiaPortalLocation` apontando para a raiz de instalação;
  c) deixe o programa ler automaticamente do registro, em `HKLM\SOFTWARE\Siemens\Automation\_InstalledSW\TIAP{20|21}\TIA_Opns\Path`.
- Com múltiplas versões instaladas na máquina, passe `--tia-major-version 20` (ou `21`) explicitamente para evitar que a versão mais alta seja escolhida automaticamente;
- Na primeira conexão, autorize o **Openness** no diálogo exibido pelo TIA Portal.

### 2. Montar o MCP

- Copie o trecho de `cursor-mcp.example.json` para qualquer cliente compatível com MCP (Cursor / VS Code / Claude Desktop / cliente HTTP próprio);
- Substitua **`REPLACE_ME`** pela **raiz do pacote**;
- **Escolha o caminho do `.exe` conforme a versão do TIA:**
  * V21 → `…\tools\tiaportal-mcp\src\TiaMcpServer\bin\Release\net48\TiaMcpServer.exe`
  * V20 → `…\tools\tiaportal-mcp\src\TiaMcpServer\bin-v20\Release\net48\TiaMcpServer.exe`
- Em instalações fora do local padrão, é obrigatório acrescentar aos `args` do cliente: `--tia-portal-location "<raiz de instalação>" --tia-major-version <20|21>`. Por exemplo: `"--tia-portal-location","D:\\app\\TIA20\\Portal V20","--tia-major-version","20"`.

### 3. Ordem das primeiras chamadas

`Bootstrap` → `Connect` → `OpenProject` (ou `CreateProject`) → `GetProjectTree`. Leia os caminhos reais de `PLC_xxx` / `HMI_RT_xxx` a partir da árvore antes de prosseguir.

---

## Validação offline (sem iniciar o TIA Portal)

Na raiz do projeto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Validate-Bundle.ps1
```

Verifica: existência do runtime, integridade dos arquivos listados nos blueprints, consistência entre `manifest/tools-list.json` e a contagem real de ferramentas, e se os JSONs de PLC/HMI são parseáveis. Com `-Strict`, aplica comparação mais rigorosa entre manifesto e matriz (opcional).

---

## Dois caminhos de trabalho

| Objetivo | O que ler | Resumo da sequência MCP |
| --- | --- | --- |
| **Gerar PLC + HMI Unified completos do zero** | `templates/project-blueprints/full_plc_hmi_project.json` + `docs/full-project-generation-runbook.md` | `Bootstrap` → `CreateProject` → hardware e rede → **PLC: `PlcBuildAndImport` com `dryRun=true` item a item** → `CompileAndDiagnosePlc` → **HMI: `EnsureUnified*` + `ApplyUnifiedHmiScreenDesignJson` + `BindUnifiedHmiTagDynamization` + `EnsureUnifiedHmiButtonAction`** → `SaveProject` |
| **Apenas validar o caminho de importação MCP/LAD/SCL** | `templates/mcp-full-e2e-verify/README.md` | Importe blocos e tags em um projeto existente conforme as instruções e compile |

---

## Mapa da documentação

| Caminho | Descrição |
| --- | --- |
| `tools/tiaportal-mcp/skill/SKILL.md` | **Especificação principal:** camadas de ferramentas, armadilhas de parâmetros, schema do Unified HMI, limites de LAD/SCL |
| `manifest/tools-list.json` | Nomes e hierarquia estáticos das ferramentas; a **lista autoritativa em tempo de execução** é o `tools/list` após conectar ao servidor |
| `docs/tool-capability-matrix.md` | Matriz de capacidades (índice estático) |
| `docs/full-project-generation-runbook.md` | Etapas de geração de projeto completo |
| `docs/basic-plc-template-library.md` | Instruções de PLC e descrição dos templates |
| `docs/scl-instruction-library.md` | **Biblioteca de instruções SCL** (controle de fluxo, escalonamento, temporizadores e contadores, PID, rampa, UDT e outros templates neutros) |
| `docs/lad-instruction-library.md` | **Biblioteca de instruções LAD** (contatos/bobinas/comparação/aritmética/temporizadores/contadores e cuidados no XML) |
| `docs/hmi-plc-tag-binding-and-addressing.md` | **HMI ↔ PLC:** endereçamento absoluto por padrão, layout de bytes do `DB200`, diagnóstico de texto em vermelho |
| `docs/hmi-connection-driver-matrix.md` | **Escolha do driver de comunicação** (`CommunicationDriver` conforme a família de CPU) |
| `docs/mcp-ide-and-tool-visibility.md` | Independência de IDE e fonte autoritativa da lista de ferramentas (`tools/list`) |
| `docs/optional-reference-materials.md` | Projetos de exemplo, em conjunto com o diretório `reference` do repositório |
| `docs/plc-network-patterns-expanded.md` | Padrões estendidos de rede e instruções de PLC (como escrever segmentos de programa mais longos) |
| `docs/tools/*.md` | Por tema: construção de PLC, hardware, ações de HMI etc. |
| `手册/quickstart.md` | Início rápido em inglês, em paralelo com este README |
| `手册/openness-limitations.md` | O que a Openness **não consegue fazer** |
| `手册/error-model.md` | Descrição do modelo de erros |
| `手册/TIA_NL_INTENT_RECIPES.md` | Linguagem natural → índice de sequências de ferramentas |
| `templates/plc/README.md` / `templates/hmi/README.md` | Índice de templates |

---

## Ciclo fechado padrão (resumido)

```
Bootstrap → Connect → CreateProject → AddDeviceWithFallback → AddHardwareCatalogDeviceWithProbe
→ ConnectDeviceNodesToProfinetSubnet → GetProjectTree → ValidateAutomationContext
→ PlcBuildAndImport(dryRun=true, item a item) → PlcBuildAndImport(dryRun=false, na ordem de importação)
→ CompileAndDiagnosePlc → EnsureUnifiedHmiConnection → EnsureUnifiedHmiTagTable → EnsureUnifiedHmiTag
→ EnsureUnifiedHmiScreen → ApplyUnifiedHmiScreenDesignJson → BindUnifiedHmiTagDynamization
→ EnsureUnifiedHmiButtonAction → SaveProject → Disconnect
```

---

## Escopo e limites de capacidade

**O que é possível:** projeto e hardware, PROFINET, importação declarativa de PLC, importação de LAD via XML, conexão / variáveis (endereçamento absoluto por padrão) / telas / ações de botão Down·Up / dinamização do Unified HMI, compilação com diagnóstico e salvamento.

**O que não está incluído no pacote:** mídia de instalação da Siemens, projetos exportados de campo e tecnologia de processo específica de negócio. O diretório `reference/` serve apenas como referência de estilo e de instruções, não participando da geração automática; consulte o campo `notBundled` em `manifest/package-manifest.json`.

---

## Estratégia de vinculação HMI

- **Endereçamento absoluto em todos os casos:** o DB de interface HMI `DB_HMI_Interface` usa acesso **não-otimizado (Standard)**. Os offsets de byte estão no campo `absoluteLayout` de `templates/plc/plcbuild-json/db_hmi_interface.json`.

- **A chamada da variável deve incluir o endereço:** ao chamar `EnsureUnifiedHmiTag`, passe `plcTag` e `address` juntos, conforme o `tags[]` do blueprint. Por exemplo, `plcTag="DB_HMI_Interface.CmdEnable"` e `address="%DB200.DBX0.0"`. Na releitura, você deve ver `Connection=HMI_Connection_1` e `Address/LogicalAddress` no formato `%DB200...`.

- **Escolha o driver de comunicação conforme o dispositivo PLC real:** o `plcName` de `EnsureUnifiedHmiConnection` usa o nó de software de PLC obtido em `GetProjectTree`. A ferramenta resolve o dispositivo PLC real, a estação, o nó PN e a família da CPU, e grava Partner/Station/Node com o driver correspondente. Detalhes em `docs/hmi-connection-driver-matrix.md`.

- **Ordem de importação:** primeiro a compilação do PLC deve passar → criar a conexão HMI → criar a tabela de variáveis → criar a tela → `BindUnifiedHmiTagDynamization` → `EnsureUnifiedHmiButtonAction`.

---

## Índice de conteúdo (caminhos)

| Caminho | Descrição |
| --- | --- |
| `tools/tiaportal-mcp/src/TiaMcpServer/bin/Release/net48/` | `TiaMcpServer.exe` e dependências |
| `scripts/Validate-Bundle.ps1` | Validação de integridade do pacote |
| `templates/project-blueprints/full_plc_hmi_project.json` | Blueprint de projeto completo |
| `templates/plc/` | Tag, UDT, DB, FC, FB, receitas LAD e exemplos SCL |
| `templates/hmi/` | `designJson` multipágina do Unified |
| `templates/mcp-full-e2e-verify/` | Materiais de importação para validação E2E |

---

## Licença

MIT. Consulte [LICENSE](LICENSE).

Esta é uma tradução para o português do README original de
[bulaofen0036-coder/TIA_Portal_Openness_MCP](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP).
Todos os direitos e créditos pertencem ao autor original.

TIA Portal, TIA, SIMATIC, STEP 7, WinCC e Siemens são marcas registradas da Siemens AG.
Este projeto não é afiliado, endossado ou patrocinado pela Siemens AG.
