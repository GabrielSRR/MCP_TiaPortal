# MCP e IDE: limites do pacote de entrega

O pacote de entrega **não depende** de um IDE específico (Cursor / VS Code / Claude Desktop / cliente HTTP próprio).
Há apenas dois tipos de protocolo: **stdio** (JSON-RPC em subprocesso) e **HTTP** (sessão MCP completa); consulte `tools/tiaportal-mcp/skill/SKILL.md` §2.

## 1. Qual fonte define a lista de ferramentas

| Fonte | Função |
|---|---|
| **`manifest/tools-list.json`** | Snapshot offline: facilita pesquisas, referências cruzadas na documentação e validações de CI. |
| **`tools/list` retornado pelo `TiaMcpServer` em execução** | **Autoridade**: corresponde aos assemblies realmente carregados; nomes/parâmetros podem apresentar pequenas diferenças em relação ao snapshot. |

Qualquer IDE que conecte corretamente o MCP Server deve conseguir enumerar o conjunto **completo** de ferramentas (por exemplo, `PlcBuildAndImport`, `ConnectDeviceNodesToProfinetSubnet` etc.).

## 2. O que significa “redução pelo IDE” (não é uma falha do pacote)

Alguns IDEs, no lado do **plugin MCP**, expõem ao modelo apenas **descritores JSON previamente armazenados no disco** para autocompletar/validação. Se esse descritor **não estiver sincronizado com o servidor**, o modelo verá **ferramentas ausentes**, embora o **mesmo executável em outros clientes ou na CLI ainda possa chamar todas as ferramentas**.

**Soluções possíveis:**

1. Compare `manifest/tools-list.json` e `docs/tool-capability-matrix.md` com os requisitos reais;
2. No cliente, **atualize / registre novamente** o MCP Server, para sincronizar o descritor com o `TiaMcpServer.exe` atual;
3. Chame diretamente `tools/list` no Server em execução e registre o resultado em um documento interno de “lista autorizada de ferramentas”.

## 3. Relação com a documentação do pacote

- Os nomes das ferramentas em `README.md` e `full-project-generation-runbook.md` são escritos com base no **manifest + SKILL** do pacote de entrega.
- Se o IDE exibir “ferramenta inexistente”, **suspeite primeiro de atraso no descritor do cliente**, não de ausência da capacidade no pacote.
