# Roadmap do servidor — alinhado à direção de baixa barreira

Data de status: 2026-06-17. **Este NÃO é um roadmap para alcançar o T-IA Connect / Openness Manager.** A direção do projeto (confirmada em 2026-06-17; memória `feedback-mcp-lower-barrier-not-features`) é otimizar **facilidade de adoção / usabilidade / precisão**, e não atingir paridade de recursos com suítes comerciais. Alguns recursos de destaque dos concorrentes foram **deliberadamente recusados** abaixo: oferecem pouco benefício real para a função desta ferramenta (automação de engenharia) e apresentam riscos reais em uma máquina em operação (o PLC de segurança de Jiangxia está no escopo).

Referências de concorrentes (somente contexto, **não são metas**): **T-IA Connect** (REST+MCP, F-safe, VCI/Git, UMAC, SiVArc) e **TIA Openness Manager** (testes unitários PLCSIM, diff por fingerprint, navegador OPC UA, cofre criptografado e interface Git). Consulte a tabela de limites de capacidade em SKILL.md §18.

---

## Concluído

### Falha de conversão no download para CPU V21 — CONCLUÍDO (2026-06-17)
- **O que ocorria:** `DownloadToPlc` falhava na V21 ao converter `ConnectionConfiguration` para `IConfiguration`. **Correção:** navegação até `ConfigurationTargetInterface` (o `IConfiguration` real) por `Modes → PcInterfaces → TargetInterfaces`; também corrigida a seleção de `StopModules` (`StopAll`, não o inexistente “StopModule”).
- **Validado** de ponta a ponta em um S7-1200 real (江夏 安全PLC): `state=Success, 0 errors`.
- **Acompanhamento — CONCLUÍDO (issue #14):** a seleção automática da primeira interface PG/PC falhava em PCs com várias NICs (WLAN + VPN + PLCSIM). As rotas agora são classificadas pela proximidade do IP da CPU; `DownloadToPlc` aceita as substituições opcionais `pgPcInterface` / `targetIpAddress`, e `CheckDownloadReadiness` lista todas as rotas candidatas em modo somente leitura.

---

## Explicitamente não planejado — recusado pela direção (baixo retorno + alto risco)

Decisão de 2026-06-17. Não inicie esses itens e não os divulgue como “em breve”. Se um usuário exigir um deles, reabra a discussão antes; não o implemente automaticamente.

- **Autoria/compilação/assinatura de blocos F de segurança.** Ferramentas comerciais começam por isso; nós não. Criar ou alterar lógica F por IA em uma CPU de segurança em operação é a ação de maior risco e menor benefício desta ferramenta; além disso, a compilação de F-CPU não possui API Openness (SKILL.md §4). A leitura de blocos *não relacionados à segurança* em um PLC de segurança já funciona (§10/§11, validada no 安全PLC), o que é suficiente.
- **Simulação/testes unitários PLCSIM Advanced.** Exigem licença/runtime separados (`Siemens.Simatic.Simulation.Runtime`) e uma integração extensa, elevando a barreira de adoção.
- **Git/VCI nativo.** A exportação textual (§16, `ExportBlocksAsDocuments`) já cobre 80% (diff/revisão/histórico) sem ampliar a superfície. Um clone nativo da VCI é recurso de suíte de produto, não de automação de engenharia.
- **Usuários/direitos UMAC, telas automáticas SiVArc, interface Git completa e cofre de credenciais criptografado.** São escopo de suíte de produto, fora do escopo de um MCP de automação de engenharia.
- **Escrita/chamada de métodos/assinatura OPC UA.** O OPC UA permanece **somente leitura** (`ReadPlcLiveValuesOpcUa`) de propósito; escritas supervisionadas em um guindaste em operação não compensam os modos de falha.

---

## Ainda em aberto — somente se for barato e alinhado

- **Proteção know-how de blocos** (`Protect`/`Unprotect` via `PlcBlockProtectionProvider`; formato comprovado em `TiaHelper.cs`). Esforço: S.
- **Auxiliar de snapshot Git** sobre a exportação textual (§16): exportar para um diretório Git e executar `git diff` contra o último snapshot. É apenas integração com ferramentas existentes, não um clone da VCI. Esforço: S–M.

---

## A fronteira real é empacotamento, não recursos do servidor

A única dimensão em que o concorrente mais simples (`AI助手`: um `.exe`, uma chave DeepSeek, “obter projeto”, chat e importação) supera este MCP é **a adoção/barreira inicial**. Isso é resolvido pelo **TiaHelperGui**, a interface WinForms fina para quem não consegue configurar o MCP, e não pela adição de ferramentas ao servidor. O produto Eigent **não é concorrente**: é um host MCP genérico que poderia montar este servidor. O diferencial é distribuição, não recursos.
