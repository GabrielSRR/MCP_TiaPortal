# Ferramentas de hardware/rede

ID do documento: `hardware-network`

Estas ferramentas dividem a configuração de rede de hardware em primitivas combináveis e verificáveis. O princípio central é: os caminhos devem vir da leitura do TIA; após uma gravação, deve ser retornada evidência de leitura posterior; não se deve adivinhar CPU, HMI, interfaces ou atributos pelo nome.

## Fluxo seguro

1. `Connect`
2. `GetState`
3. `GetProjectTree`
4. `GetDeviceItemTree(deviceItemPath)`
5. `GetDeviceItemNetworkInfo(deviceItemPath)`
6. `PlanHardwareNetworkConfiguration(planJson)`
7. `EnsureSubnet(...)`
8. `AttachDeviceNodeToSubnet(...)`
9. `SetCpuCommonSettings(...)`
10. `GetDeviceItemNetworkInfo(...)` ou `readback` retornado
11. Compile/salve somente após leitura posterior e diagnósticos aceitáveis.

## PlanHardwareNetworkConfiguration

`PlanHardwareNetworkConfiguration(planJson)` é somente offline; não conecta ao TIA nem modifica o projeto. Tipos aceitos: `EnsureSubnet`, `AttachDeviceNodeToSubnet` e `SetCpuCommonSettings`.

Exemplo:

```json
{
  "operations": [
    {
      "type": "EnsureSubnet",
      "anchorDeviceItemPath": "PLC_1/PLC_1.CPU_1",
      "subnetType": "PROFINET",
      "subnetName": "PN_IE_1",
      "ip": "192.168.0.1",
      "mask": "255.255.255.0"
    },
    {
      "type": "AttachDeviceNodeToSubnet",
      "deviceItemPath": "HMI_1/HMI_1.IE_CP_1",
      "interfaceIndex": 0,
      "subnetName": "PN_IE_1"
    },
    {
      "type": "SetCpuCommonSettings",
      "cpuPath": "PLC_1/PLC_1.CPU_1",
      "settings": {
        "exactAttributes": {
          "Name": "PLC_1"
        }
      }
    }
  ]
}
```

O planejador rejeita caminhos presumidos como `PLC`, `CPU`, `HMI`, curingas, tipos de sub-rede não suportados, IPv4/máscaras inválidos e configurações de CPU que usem aliases em vez dos nomes exatos dos atributos TIA.

## EnsureSubnet

`EnsureSubnet(anchorDeviceItemPath, subnetType, subnetName)` cria ou reutiliza uma sub-rede Industrial Ethernet/PROFINET ancorando-se em um caminho real de device item.

- `anchorDeviceItemPath` deve vir de `GetProjectTree`/`GetDeviceItemTree`.
- `subnetType` limita-se a `PROFINET`, `PN`, `PN/IE`, `IndustrialEthernet` ou `Industrial Ethernet`.
- A ferramenta retorna linhas `readback` com caminho do nó, item, tipo do nó e `connectedSubnet`.

## AttachDeviceNodeToSubnet

`AttachDeviceNodeToSubnet(deviceItemPath, interfaceIndex, subnetName, anchorDeviceItemPath?)` conecta um nó Industrial Ethernet/PROFINET descoberto a uma sub-rede.

- Resolva `deviceItemPath` pela leitura do projeto.
- Use `interfaceIndex` da lista de nós candidatos nos metadados retornados.
- Passe `anchorDeviceItemPath` somente quando a sub-rede precisar ser garantida primeiro.
- O sucesso só é verdadeiro quando a sub-rede solicitada e o nó-alvo aparecem na leitura posterior.

## SetCpuCommonSettings

`SetCpuCommonSettings(cpuPath, settingsJson)` grava atributos exatos do device item da CPU:

```json
{
  "exactAttributes": {
    "ExactAttributeNameFromGetDeviceItemNetworkInfo": "value"
  }
}
```

Não passe aliases como `ip`, `gateway` ou `profinetName`, a menos que sejam exatamente os nomes retornados por `GetDeviceItemInfo` ou `GetDeviceItemNetworkInfo`. A ferramenta rejeita atributos ausentes ou não graváveis e retorna listas aplicadas/rejeitadas com evidência de leitura posterior.

## Observações de segurança

- São ferramentas de edição offline do projeto; não ficam online e não executam operações de Force.
- O monitoramento online permanece somente leitura e separado das edições de rede.
- Nunca salve antes de a leitura posterior e os diagnósticos de compilação serem aceitáveis.
