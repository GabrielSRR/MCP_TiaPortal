# Pacote completo de entrega TIA Portal MCP (V20+V21 + S7DCL + CLI + monitoramento online somente leitura + configuração em um clique + diagnóstico Doctor)

> A versão atual aparece no selo Release acima e em [CHANGELOG.md](CHANGELOG.md) (o README não fixa mais o número da versão).

[English](README.en.md) · 中文 · **Português**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/bulaofen0036-coder/TIA_Portal_Openness_MCP)](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP/releases) [![validate-bundle](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP/actions/workflows/validate.yml/badge.svg)](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP/actions/workflows/validate.yml)

> **Código aberto gratuito (MIT)**: o servidor funciona **sem qualquer license key** e **não contém código de validação de licença**.

![Diagrama da arquitetura](docs/assets/architecture.svg)

No **Windows + TIA Portal V20 ou V21**, o pacote usa **MCP (stdio ou HTTP)** para controlar o TIA Portal: criar projetos, adicionar hardware, gerar PLC (Tag/UDT/DB/SCL/LAD), gerar telas e eventos **WinCC Unified**, compilar, diagnosticar e salvar.
O pacote inclui **runtime já compilado**, Skill, lista estática de ferramentas, matriz de capacidades, templates PLC/HMI, **blueprints de projeto prontos para leitura** e manuais. **Não é necessário** clonar o repositório de código-fonte.

## 🆕 v2.5.0: colocar o projeto do TIA no Git (VCI)

Projetos TIA são binários e o Git não consegue fazer diff; por isso, o controle de versão normalmente exigia várias pastas datadas.
A **interface de controle de versão** da V21 mapeia o projeto para uma pasta comum, com **um arquivo de texto por bloco**, permitindo diff, commit e revisão.

Basta dizer à IA:

```text
Coloque o projeto atual no Git; use D:\repos\my-plc como área de trabalho
```

Ela cria a área de trabalho, gerencia automaticamente todo o projeto, exporta os textos e você executa `git commit`.
Para consultar alterações:

```text
GetVersionControlStatus(changedOnly=true)
→ A3_4_Hoist | Unequal        ← precisão por bloco
```

- **Abrangência**: FC / FB / OB / DB, tabelas de variáveis PLC e UDT (todo o lado do programa). Configuração de hardware e blocos protegidos por know-how ficam fora do VCI e são informados explicitamente.
- **É preciso compilar antes de exportar** (limitação do TIA); a detecção funciona mesmo sem salvar.
- `tools/vci-watch/` automatiza exportação, atualização do CHANGELOG e commit após a compilação.

📖 Uso completo e os três comportamentos essenciais → **[docs/version-control-git.md](docs/version-control-git.md)**

## ⚡ Início rápido (3 etapas, sem programação e via CLI)

1. **Preparar**: instale **TIA Portal V20 ou V21** e **.NET Framework 4.8**; adicione o usuário Windows ao grupo local **`Siemens TIA Openness`** e faça logoff/login. Use `tia.cmd` (V21) ou `tia-v20.cmd` (V20). Execute antes `tia.cmd doctor` (ou `tia-v20.cmd doctor`) para verificar instalação, versão, grupo Openness e registro do host.
2. **Pré-aquecimento (opcional, recomendado)**: execute `scripts\预热.bat` e mantenha a janela aberta. Uma instância TIA headless permanecerá ativa e as conexões seguintes levarão cerca de **1 segundo**. Finalize com `Ctrl+C`.
3. **Gerar o projeto**: arraste `templates\project-blueprints\scaffold_spec_motor.json` (ou `scaffold_spec_start_stop.json`) para `scripts\生成工程.bat`. O fluxo cria o projeto, adiciona PLC/HMI, escreve blocos, compila e salva. Código de saída `0` indica sucesso.

Para requisitos próprios, peça a qualquer IA uma spec conforme [`docs/AI_spec_prompt.md`](docs/AI_spec_prompt.md) e arraste-a para o mesmo script. Equivalente de linha de comando: `tia gen <spec>`; use primeiro `--dry-run`.

## v2.0.0 — CLI `tia`

O mesmo executável funciona como servidor MCP e CLI. `tia gen <spec.yaml|json>` cria um projeto completo (`ScaffoldProject`); `tia patch <spec>` aplica alterações incrementais em um projeto existente. Também existem `tia compile`, `describe`, `export`, `import`, `prewarm`, `schema` e `version`.

Os códigos de saída são **0 = sucesso / 1 = etapas com falha / 2 = erro**. YAML e JSON são aceitos, e `--dry-run` valida offline.
Os comandos `tia.cmd` (V21) e `tia-v20.cmd` (V20) ficam na raiz do pacote. Os templates de partida/parada e motor em `templates/project-blueprints/` podem ser usados diretamente.

## v1.0.0 — rápido, útil e confiável

- Inicialização headless padrão (`WithoutUserInterface`) reduz a inicialização de aproximadamente 200–340 s para 10–28 s; use `--with-ui` quando precisar da interface.
- `ScaffoldProject` cria hardware PLC/HMI, UDT/DB/tags, blocos SCL/LAD, compila, configura HMI e salva em uma chamada. `dryRun=true` valida a spec offline.
- `python scripts/prewarm_tia.py` mantém uma instância residente e reduz `Connect` para cerca de 0,8–1 s.
- O caminho do software HMI é detectado automaticamente; importações individuais confirmam o resultado por `Meta.verified`.

### Atualizações em relação ao pacote 20260512

- Geração estável com `CapabilityDecision`, `CapabilityWarnings` e `RecommendedNextActions`; `strict=true` e `requireVerifiedBinding=true` evitam sucessos falsos.
- O pacote contém executáveis separados para V21 e V20. Eles **não devem ser intercambiados**, pois usam assemblies Openness diferentes.
- `ExportAsDocuments`, `ExportBlocksAsDocuments`, `ImportFromDocuments` e `ImportBlocksFromDocuments` usam o formato textual SIMATIC SD (`.s7dcl + .s7res`), mais legível e adequado a diff.
- Validação ponta a ponta: V21 exportou/importou 8 blocos em 14,7 s; V20 exportou 51 `.s7dcl` e 33 `.s7res`.

**Independente de IDE**: clientes MCP como Cursor, VS Code, Claude Desktop e clientes HTTP próprios usam o mesmo `TiaMcpServer.exe`. Se uma ferramenta não aparecer em uma IDE, isso normalmente é cache/descritor do cliente; consulte `docs/mcp-ide-and-tool-visibility.md`.

### Localização dos executáveis

| Forma de obtenção | Executável V21 | Executável V20 |
|---|---|---|
| ZIP Release (recomendado) | `tools\tiaportal-mcp\src\TiaMcpServer\bin\Release\net48\TiaMcpServer.exe` | `tools\...\bin-v20\Release\net48\TiaMcpServer.exe` |
| Clone Git | `runtime\v21\TiaMcpServer.exe` | Não distribuído no repositório; baixe o ZIP Release |

`配置MCP.bat`, `tia.cmd` e `scripts\*.bat` procuram automaticamente os dois layouts. A configuração manual usa `cursor-mcp.example.json`; substitua `REPLACE_ME` pelo diretório real.

## Branches por versão e contribuições

`master` é a linha estável oficial para **TIA Portal V20/V21**. Correções específicas de versões antigas devem ir para suas branches:

| Branch | Versão-alvo | Manutenção |
|---|---|---|
| `master` | V20 / V21 | Linha oficial |
| `v21` | V21 / Openness V21 | Oficial, adaptações exclusivas V21 |
| `v20` | V20 / Openness V20 | Oficial, adaptações exclusivas V20 |
| `v19` a `v16` | Openness correspondente | Contribuição da comunidade |

Alterações compatíveis com V20 e V21 continuam em `master`. Não envie projetos `.apXX`, `bin`, `obj`, logs, capturas, backups, caminhos absolutos ou projetos temporários de teste.

## Etapas de instalação

1. Instale .NET Framework **4.8** e TIA Portal V20/V21; entre no grupo **`Siemens TIA Openness`**; escolha a instalação com `--tia-portal-location`, `TiaPortalLocation` ou descoberta pelo registro; use `--tia-major-version 20|21` quando necessário; autorize Openness no primeiro vínculo.
2. Execute `config` pela raiz (`tia.cmd config` ou `配置MCP.bat`). O comando detecta caminhos, versão e hosts Claude Desktop, Claude Code, Cursor e VS Code, preservando backups `.bak`.
3. Primeiro fluxo MCP: `Bootstrap` → `Connect` → `OpenProject` ou `CreateProject` → `GetProjectTree`; use somente os caminhos reais `PLC_xxx` e `HMI_RT_xxx` retornados pela árvore.

## Perfis de ferramentas

O servidor contém **208** ferramentas, mas o perfil padrão expõe aproximadamente **48** em `tools/list`. Isso reduz o schema de cerca de 157 KB/40.200 tokens para 34 KB/8.600 tokens e evita limites de 128 ferramentas em VS Code/Copilot.

As demais ferramentas continuam disponíveis sob demanda:

```text
FindTools("watch table")
CallTool("ExportPlcWatchTable", "{...}")
```

| Perfil | Ativação | Ferramentas listadas |
|---|---|---|
| Reduzido (padrão) | nenhuma | ~48 |
| Completo | `config --full`, `--profile full` ou `TIA_MCP_PROFILE=full` | 208 |

## Validação offline

Na raiz do projeto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Validate-Bundle.ps1
```

O script verifica runtime, arquivos do blueprint, contagem de ferramentas e JSONs PLC/HMI. `-Strict` habilita comparações adicionais.

## Dois fluxos de trabalho

| Objetivo | Referências | Resumo MCP |
|---|---|---|
| Gerar PLC + Unified HMI completo | `templates/project-blueprints/full_plc_hmi_project.json` e `docs/full-project-generation-runbook.md` | `Bootstrap` → `CreateProject` → hardware/rede → `PlcBuildAndImport(dryRun=true)` → `CompileAndDiagnosePlc` → `EnsureUnified*` → `ApplyUnifiedHmiScreenDesignJson` → `BindUnifiedHmiTagDynamization` → `EnsureUnifiedHmiButtonAction` → `SaveProject` |
| Validar apenas importação MCP/LAD/SCL | `templates/mcp-full-e2e-verify/README.md` | importar blocos e tags em projeto existente e compilar |

## Mapa de documentação

Iniciantes devem seguir este README e depois [`docs/README.md`](docs/README.md). Os documentos principais incluem `SKILL.md`, `manifest/tools-list.json`, matrizes de capacidade, runbooks PLC/HMI, bibliotecas SCL/LAD, vinculação HMI↔PLC, limitações Openness, receitas de intenção natural, templates e `scripts/Validate-Bundle.ps1`.

## Fluxo padrão

```text
Bootstrap → Connect → CreateProject → AddDeviceWithFallback → AddHardwareCatalogDeviceWithProbe
→ ConnectDeviceNodesToProfinetSubnet → GetProjectTree → ValidateAutomationContext
→ PlcBuildAndImport(dryRun=true por item) → PlcBuildAndImport(dryRun=false na ordem correta)
→ CompileAndDiagnosePlc → EnsureUnifiedHmiConnection → EnsureUnifiedHmiTagTable → EnsureUnifiedHmiTag
→ EnsureUnifiedHmiScreen → ApplyUnifiedHmiScreenDesignJson → BindUnifiedHmiTagDynamization
→ EnsureUnifiedHmiButtonAction → SaveProject → Disconnect
```

## Escopo e limites

**Pode fazer**: projetos e hardware, PROFINET, importação declarativa PLC, importação LAD XML, conexões/variáveis/telas/botões Unified HMI, dinamizações, compilação, diagnóstico e salvamento.

**Não inclui**: mídia de instalação Siemens, projetos exportados de campo ou processos específicos de negócio. `reference/` serve apenas como referência de estilo e instruções; veja `notBundled` em `manifest/package-manifest.json`.

## Estratégia de vinculação HMI

- Use endereços absolutos no DB `DB_HMI_Interface`, com acesso **Standard/não otimizado**; os offsets estão em `templates/plc/plcbuild-json/db_hmi_interface.json`.
- Em `EnsureUnifiedHmiTag`, envie `plcTag` e `address`, por exemplo `DB_HMI_Interface.CmdEnable` e `%DB200.DBX0.0`; a leitura posterior deve mostrar `Connection=HMI_Connection_1` e `Address/LogicalAddress=%DB200...`.
- `EnsureUnifiedHmiConnection.plcName` deve ser o nó de software PLC obtido por `GetProjectTree`; o servidor resolve dispositivo, estação, nó PN, CPU e driver.
- Ordem: PLC compilado → conexão HMI → tabela de tags → tela → dinamizações → ações de botão.

## Índice de conteúdo

| Caminho | Descrição |
|---|---|
| `tools/tiaportal-mcp/src/TiaMcpServer/bin/Release/net48/` | `TiaMcpServer.exe` e dependências |
| `runtime/v21/` | layout do clone Git |
| `scripts/Validate-Bundle.ps1` | validação de integridade |
| `templates/project-blueprints/full_plc_hmi_project.json` | blueprint completo |
| `templates/plc/` | Tag, UDT, DB, FC, FB, LAD e SCL |
| `templates/hmi/` | `designJson` Unified multipágina |
| `templates/mcp-full-e2e-verify/` | materiais de validação E2E |
