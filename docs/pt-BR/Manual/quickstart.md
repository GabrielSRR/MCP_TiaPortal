# Início Rápido — TIA Portal MCP (versão do pacote de entrega)

Este documento é consistente com o **`README.md` em inglês/chinês da raiz**: o pacote de entrega já contém o **`TiaMcpServer.exe`**, e em geral **não é necessário** rodar `dotnet build` por conta própria. Compilar a partir do projeto de código-fonte fornecido pela Siemens só é preciso se você for fazer desenvolvimento adicional no servidor (o que não faz parte dos passos deste pacote).

---

## 1. Pré-requisitos

- **Windows**, **.NET Framework 4.8**
- **TIA Portal** (recomendada a **V21**; outras versões principais dependem do ambiente e da PublicAPI)
- Usuário pertencente ao grupo **`Siemens TIA Openness`**: `whoami /groups | findstr Openness`
- Variável de ambiente de usuário **`TiaPortalLocation`** = raiz de instalação do Portal, por exemplo:
  `D:\app\TIA21\Portal V21` ou `C:\Program Files\Siemens\Automation\Portal V21`
- Na primeira conexão, autorize o acesso do **Openness** dentro do TIA

---

## 2. Verificação de integridade do pacote (offline)

A partir da **raiz do pacote de entrega** (a pasta que contém o `README.md`):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Validate-Bundle.ps1
```

---

## 3. Conectar o MCP — **stdio recomendado**

Copie o `cursor-mcp.example.json` para a configuração do seu cliente. Defina o `command` como o **caminho absoluto** de:

`tools\tiaportal-mcp\src\TiaMcpServer\bin\Release\net48\TiaMcpServer.exe`

Reinicie o cliente. Primeiras chamadas de automação: **`Bootstrap`** → **`Connect`** → **`GetProjectTree`**.

**Documentação estática incluída neste pacote:**

- `manifest/tools-list.json` — nomes e camadas das ferramentas
- `docs/tool-capability-matrix.md` — matriz de capacidades

Com o servidor em execução, o **`tools/list`** (ou o seletor de ferramentas do seu cliente) é a lista **autoritativa** em tempo de execução — as contagens podem variar ligeiramente entre builds.

---

## 4. Transporte HTTP (avançado)

```powershell
TiaMcpServer.exe --transport http --http-prefix http://127.0.0.1:8765/ --http-api-key <segredo>
```

- **`GET /mcp/health`** — apenas verificação de vida (liveness)
- **`POST /mcp`** — **sessão MCP JSON-RPC completa** (não um único `tools/call` isolado). Scripts customizados precisam implementar o protocolo (initialize, sessão/SSE conforme necessário). Veja a §2 de **`tools/tiaportal-mcp/skill/SKILL.md`** e a tabela "como escolher o modo de chamada".

---

## 5. Primeiras verificações dentro da sessão do TIA

Peça ao seu assistente para executar:

1. `RunCapabilitySelfTest` — teste rápido do ambiente (smoke test)
2. Com um projeto aberto: `Connect` → `AttachToOpenProject`, ou crie um via `CreateProject` → `GetProjectTree`

---

## 6. O que a Openness não consegue fazer

Ler/escrever o estado RUN/STOP da CPU, buffer de diagnóstico e limpeza seletiva de forces como operações discretas de runtime — veja **`openness-limitations.md`**. Prefira **OPC UA** para dados de runtime.

---

## 7. Solução de problemas

| Sintoma | Correção |
|---------|----------|
| `TIA Portal not running` | Inicie o TIA primeiro |
| Árvore vazia | Abra um projeto ou use `CreateProject` / `AttachToOpenProject` |
| Openness negado | Grupo do Windows + diálogo de autorização do TIA |
| MCP HTTP travando | Não use POST cru; use um cliente stdio ou um cliente MCP completo |

Mais informações: **`error-model.md`**. Receitas de linguagem natural: **`TIA_NL_INTENT_RECIPES.md`**.
