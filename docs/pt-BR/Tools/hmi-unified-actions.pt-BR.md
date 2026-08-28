# Receitas de ações HMI Unified

ID do documento: `hmi-unified-actions`

Este documento é o contrato estável para receitas de ações de botões WinCC Unified no servidor TIA MCP. Ele é deliberadamente conservador: somente comandos de bits determinísticos podem ser aplicados diretamente pela ferramenta segura de alto nível.

## Seleção de ferramentas

| Ferramenta | Uso | Grava no projeto |
|---|---|---|
| `BuildUnifiedHmiButtonActionScript` | Geração e lint offline de receitas | Não |
| `RunHmiActionScriptRecipeSafetySelfTest` | Prova offline dos limites de segurança | Não |
| `EnsureUnifiedHmiButtonAction` | Aplica receita segura de bit a evento real | Sim |
| `SetUnifiedHmiButtonEventScriptCode` | Define ScriptCode com SyntaxCheck do TIA | Sim |
| `BindUnifiedHmiTagDynamization` | Vincula propriedade de item HMI a uma HMI Tag | Sim |

## Receitas diretamente aplicáveis

Estas são as únicas ações que `EnsureUnifiedHmiButtonAction` pode aplicar:

| `actionKind` | Requisito | Script gerado |
|---|---|---|
| `set-bit` | Exatamente uma HMI Tag verificada | `HMIRuntime.Tags.SysFct.SetBitInTag("<tag>", 0);` |
| `reset-bit` | Exatamente uma HMI Tag verificada | `HMIRuntime.Tags.SysFct.ResetBitInTag("<tag>", 0);` |
| `toggle-bit` | Exatamente uma HMI Tag verificada | `HMIRuntime.Tags.SysFct.ToggleBitInTag("<tag>", 0);` |

Antes de aplicar:

1. Execute `GetProjectTree` e resolva o caminho real do software HMI.
2. Execute `GetHmiScreens`, `GetHmiTagTables` e faça a leitura posterior das HMI Tags.
3. Verifique a existência da HMI Tag de destino.
4. Confirme que ela mapeia para uma tag/membro real do PLC; nunca use bits M presumidos.
5. Aplique com `EnsureUnifiedHmiButtonAction`.
6. Verifique `SyntaxCheck` e os metadados de leitura de `SetUnifiedHmiButtonEventScriptCode`.

## Receitas bloqueadas ou provisórias

| `actionKind` | Status | Motivo |
|---|---|---|
| `set-value` | Bloqueada | Exige validação de faixa, permissões, confirmação do operador, SyntaxCheck e leitura posterior. |
| `confirm-write` | Bloqueada | Igual a `set-value`; requer confirmação específica da interface do projeto. |
| `goto-screen` | Bloqueada até descoberta | A API de navegação precisa ser descoberta e lida em projeto temporário. |
| `open-popup` | Bloqueada até descoberta | A API de popup precisa ser descoberta e lida em projeto temporário. |
| `script` | Não determinística | Scripts genéricos não podem ser comprovados como seguros apenas pelos metadados da ação. |
| `project-binding-placeholder` | Somente estrutural | Nenhum ScriptCode executável é gerado ou aplicado. |

## Linhas vermelhas de segurança

- Scripts gerados não podem conter `Force`.
- Scripts gerados não podem referenciar `WatchTable` ou `ForceTable`.
- É proibida a modificação online de watch/monitor tables.
- Ações de escrita HMI não podem ser promovidas de bloqueadas para aplicáveis sem validação de faixa, confirmação do operador, permissões, SyntaxCheck do TIA e evidência de leitura posterior.
- Navegação e popups são específicos do projeto até que um projeto temporário TIA V21 prove a API e o formato exatos do ScriptCode.

## Exemplo de receita offline

Entrada:

```text
BuildUnifiedHmiButtonActionScript(
  actionKind: "set-bit",
  eventType: "Tapped",
  targetTag: "Cmd_Start"
)
```

Campos esperados:

```json
{
  "recipeKind": "set-bit",
  "event": "Tapped",
  "targetTags": ["Cmd_Start"],
  "script": "HMIRuntime.Tags.SysFct.SetBitInTag(\"Cmd_Start\", 0);",
  "safetyLevel": "command",
  "requiresApiDiscovery": false,
  "requiresSafetyPolicy": false,
  "applyBlocked": false,
  "requiresSyntaxCheckInTia": true,
  "requiresReadback": true
}
```

## Checklist de aplicação real

1. `Connect`
2. `GetProjectTree`
3. `ValidateAutomationContext`
4. `GetHmiScreens`
5. `GetHmiTagTables`
6. Verifique o mapeamento HMI Tag/símbolo PLC.
7. Execute `BuildUnifiedHmiButtonActionScript` e inspecione `Meta.errors`, `Meta.warnings`, `Meta.applyBlocked`.
8. Chame `EnsureUnifiedHmiButtonAction` somente para `set-bit`, `reset-bit` ou `toggle-bit`.
9. Confirme os metadados de SyntaxCheck/leitura de `SetUnifiedHmiButtonEventScriptCode`.
10. Salve somente após a leitura posterior ter sucesso.

## Validação em projeto temporário

Para receitas atualmente bloqueadas por descoberta da API:

1. Crie ou abra um projeto TIA V21 descartável.
2. Adicione uma tela Unified mínima e um botão.
3. Configure o evento de navegação/popup manualmente ou por um caminho Openness verificado.
4. Leia o ScriptCode e o formato da API.
5. Reaplique-o a uma tela descartável por `SetUnifiedHmiButtonEventScriptCode`.
6. Execute SyntaxCheck e leia o ScriptCode novamente.
7. Só então atualize este contrato e o autoteste de segurança.
