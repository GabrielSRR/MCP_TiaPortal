# Ferramentas de tema/layout HMI Unified

ID do documento: `hmi-unified-theme-layout`

Este documento é o contrato estável para ferramentas de alto nível de estilização de telas WinCC Unified.

## Seleção de ferramentas

| Ferramenta | Uso | Grava no projeto |
|---|---|---|
| `BuildUnifiedHmiThemeDesignJson` | Gera JSON de execução de tema/paleta offline | Não |
| `BuildUnifiedHmiLayoutDesignJson` | Gera JSON de execução de layout em grade offline | Não |
| `ApplyUnifiedHmiTheme` | Aplica tema a uma tela Unified real por `ApplyUnifiedHmiScreenDesignJson` | Sim |
| `ApplyUnifiedHmiLayout` | Aplica layout em grade a uma tela Unified real | Sim |
| `ApplyUnifiedHmiScreenDesignJson` | Executor de design de baixo nível | Sim |

## Entrada de tema

```json
{
  "name": "PlantClean",
  "palette": {
    "Page": "0xFFF4F6F8",
    "Surface": "0xFFFFFFFF",
    "Text": "0xFF172033",
    "Border": "0xFFD7DEE8"
  }
}
```

As cores devem usar strings ARGB do TIA, como `0xFFF4F6F8`.

## Entrada de layout

```json
{
  "grid": 8,
  "left": 24,
  "top": 72,
  "gap": 16,
  "columns": 2,
  "cellWidth": 160,
  "cellHeight": 80,
  "items": [
    { "name": "Card_Run", "type": "Rectangle", "text": "运行" },
    { "name": "Card_Fault", "type": "Rectangle", "colSpan": 2, "text": "故障" }
  ]
}
```

O builder calcula `left`, `top`, `width` e `height` a partir das linhas/colunas e ajusta os valores à grade configurada.

## Checklist de aplicação real

1. Execute primeiro `BuildUnifiedHmiThemeDesignJson` ou `BuildUnifiedHmiLayoutDesignJson`.
2. Inspecione o JSON de execução gerado.
3. Execute `Connect`, `GetProjectTree` e `ValidateAutomationContext`.
4. Resolva o caminho real do software HMI e o nome da tela.
5. Aplique com `ApplyUnifiedHmiTheme` ou `ApplyUnifiedHmiLayout`.
6. Leia os objetos alterados com `DescribeHmiScreenItem`.
7. Para botões/eventos, execute o fluxo de receitas de ação e mantenha evidência de `SyntaxCheck` com 0 erros.
8. Salve somente após a leitura posterior ter sucesso.

## Regras de segurança

- Ferramentas de tema/layout não devem criar tags PLC nem vinculações presumidas.
- Ferramentas de layout somente posicionam/estilizam itens; a sincronização PLC-HMI é tratada pela suíte de preflight de símbolos PLC.
- Gravações reais no projeto exigem evidência de leitura posterior antes de salvar.
- Scripts de eventos HMI continuam sujeitos ao contrato separado de segurança das receitas e às evidências de `SyntaxCheck`.
