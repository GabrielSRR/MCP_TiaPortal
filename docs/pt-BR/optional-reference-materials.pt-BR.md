# Materiais de referência opcionais (diretório `reference` do repositório)

O pacote de entrega tem **tamanho controlado** e não inclui projetos-modelo Siemens grandes. Recomenda-se manter o diretório no mesmo nível ou acima deste repositório:

`…\PID博途块\reference\`

Ele pode conter, por exemplo:

| Conteúdo | Uso típico |
|---|---|
| `Siemens Standard Template V5_V21\*.ap21` | Abrir no TIA para **comparar** alarmes do PLC, drives e organização de bibliotecas; **copiar blocos/trechos** para o projeto gerado pelo MCP e depois compilar. |
| `HMI_Template_Suite_WinCC_Unified_V18\*.al21` / `*_V21` | **Suíte oficial de templates WinCC Unified**: abrir no TIA para estudar **layout, estilos e combinações de controles**; `templates/hmi/*.json` deste pacote é um subconjunto **simplificado e programável**, cuja aparência pode se aproximar da suíte. |
| `XM_Mxxxx_*_V21\*.ap21` | Referência completa de linha de produção/múltiplas instâncias HMI: **dispositivos e rede**, vários RTs e roteamento. |

## Forma recomendada de uso

1. Abra o `.ap21` de referência **separadamente** no TIA Portal; **não** misture e alterne entre ele e um projeto modificado automaticamente pelo MCP na mesma sessão não salva.
2. Para reutilizar blocos: use **copiar/biblioteca** no TIA ou **exporte XML** e depois use `ImportBlock` no projeto MCP.
3. Para reutilizar estilos HMI: faça **capturas/anotações dos valores de cor e espaçamentos** no projeto de referência e aplique-os ao `designJson` deste pacote ou aos seus próprios templates.

## Relação com os templates do pacote

- `templates/hmi/*.json`: `designJson` plano, **regravável pelo MCP**, adequado para automação.
- `.ap21/.al21` em `reference`: **modelos de referência para refinamento e validação manual no TIA**, que **não** precisam ser importados integralmente por scripts.
