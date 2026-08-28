# Linha de comando `tia` — comece em 5 minutos

A partir da v2.0, **o mesmo executável** do pacote de entrega é tanto o serviço MCP quanto a linha de comando `tia`.
Não é preciso instalar cliente MCP nem saber programar: **qualquer IA escreve um spec e você roda um comando.**

## Deixar o comando `tia` disponível (uma única vez)

A raiz do pacote de entrega já traz os pontos de entrada prontos:

- **`tia.cmd`** (V21) / **`tia-v20.cmd`** (V20) — escolha conforme a versão principal do TIA que você tem instalada.

Duas formas de uso:

1. **Usar o nome completo diretamente:** na raiz do pacote, rode `tia gen spec.yaml` (usuários de V20: `tia-v20 gen spec.yaml`).
2. **Adicionar ao PATH e usar de qualquer lugar (recomendado):** inclua a raiz do pacote na variável de ambiente `PATH` do sistema; depois disso, `tia gen ...` funciona em qualquer diretório.

> Daqui em diante o texto escreve sempre `tia`; usuários de V20 devem trocar por `tia-v20`. Os dois `.cmd` apenas repassam os argumentos ao executável do motor
> (layout do zip: `…\bin\Release\net48\` e `…\bin-v20\…`; layout do git clone: `runtime\v21\` — o script localiza automaticamente), devolvendo o código de saída sem alteração.
> Se preferir não configurar nada, chamar o caminho completo do `.exe` tem exatamente o mesmo efeito.

---

## Três formas de uso, da mais simples à mais avançada

### 1. O mais simples: duplo clique no .bat
- **Arraste um `spec.yaml` ou `spec.json` sobre o `scripts\生成工程.bat`** (*gerar projeto*) → o projeto é criado automaticamente.
- Para conectar mais rápido: primeiro dê duplo clique em `scripts\预热.bat` (*pré-aquecimento*) e deixe a janela aberta; depois disso, cada criação de projeto conecta em cerca de 1 segundo.

### 2. Um único comando
```
tia gen  projeto.yaml            # cria o projeto completo a partir do spec
tia gen  projeto.yaml --dry-run  # só valida o spec offline; não conecta ao TIA nem cria nada
tia patch alteracoes.yaml        # mescla o spec de forma incremental em um projeto existente (com projectPath no spec)
tia compile  D:\proj\X.ap21 --plc PLC_1
tia describe D:\proj\X.ap21 --plc PLC_1
tia prewarm                      # mantém uma instância headless residente; comandos seguintes conectam em ~1s
tia doctor                       # check-up completo: instalação do TIA / correspondência de versão do exe / grupo Openness / registro no host (--fix corrige o grupo de usuário automaticamente)
tia config                       # registra o MCP de uma vez em Claude Desktop / Claude Code / Cursor / VS Code (--lite = perfil enxuto com 42 ferramentas)
tia schema                       # imprime a descrição de todos os campos do spec
```
Códigos de saída: **0 = sucesso, 1 = houve etapas com falha, 2 = erro** (prático para scripts e CI).
Acrescente `--json` para saída legível por máquina, facilitando que a IA leia o resultado e se autocorrija.

### 3. Deixar a IA gerar o spec
Cole em qualquer IA o prompt de `docs/AI_spec_prompt.md` junto com a saída de `tia schema`,
descreva o projeto que você quer, a IA produz um `spec.yaml` e você segue pela forma 1 ou 2.

---

## Como é um spec

Exemplo mínimo (YAML):
```yaml
projectName: MyLine
plcName: PLC_1
plcFamily: S7-1500
udt:
  - name: UDT_Status
    members:
      - { name: Active, datatype: Bool, commentZhCn: 运行 }
tagTable:
  - tableName: IO
    tags:
      - { name: Start, dataTypeName: Bool, logicalAddress: "%I0.0" }
compile: true
save: true
```
Os campos completos estão em `tia schema`; templates prontos estão em `templates/project-blueprints/` (partida/parada e motor, ambos compilando com 0 erros).
Esses dois templates funcionam **direto, sem ajustes**: os caminhos que referenciam arquivos `.scl` / `.s7dcl` são escritos como `__BUNDLE__\...`,
e o `tia` resolve automaticamente o `__BUNDLE__` para a raiz do pacote de entrega. Basta rodar `tia gen scaffold_spec_motor.json`,
sem substituir caminho nenhum manualmente. (Copiar os templates para outro lugar também funciona, desde que o `tia` continue dentro do pacote.)

Dicas:
- `tia gen` cria do zero; `tia patch` altera um projeto existente (acrescente `projectPath: D:\...\X.ap21` no spec).
- O `width`/`height` das telas HMI deve seguir a resolução nativa do painel, caso contrário a tela é cortada.
- Usar endereços absolutos (`%M..`) em `hmiTags` facilita a validação por releitura.
- JSON é o formato preferido (zero ambiguidade, mais estável na geração por IA); YAML é a conveniência para leitura e escrita humana.

---

## Perguntas frequentes

- **Está lento?** A primeira conexão faz cold start do TIA headless em cerca de 10–28s; depois de um `tia prewarm`, cai para cerca de 1s. Não dá para ir além disso — `CreateProject` / `AddDevice` / `Save` têm custo de tempo inerente à Openness.
- **Caracteres corrompidos?** A saída já é forçada para UTF-8; salve os arquivos `.scl` em UTF-8 com BOM.
- **V20 ou V21?** Use o executável correspondente à sua versão principal do TIA (no zip: `bin\Release` = V21 e `bin-v20\Release` = V20; o git clone traz apenas o `runtime\v21`, da V21). É possível sobrescrever com `--tia-major-version 20|21` ou `--tia-portal-location <raiz de instalação>`.
- **Quero ver a interface gráfica.** Acrescente `--with-ui` para iniciar com a interface completa (mais lento).
- **Posso usar caminho relativo para o projeto?** Sim — os caminhos de projeto em `tia describe/compile/export/import` e em `tia patch` agora são resolvidos a partir do diretório em que você está (corrigido na v2.0; antes só o diretório do `.exe` era reconhecido, resultando em `Projects.Open failed`).
- **Como parar o `tia prewarm`?** Pressione `Ctrl+C` na janela em que ele está rodando para encerrar de forma limpa. Se ele foi iniciado em segundo plano ou por duplo clique, o `tia prewarm --stop` encerra apenas aquela instância headless do TIA; o **processo de pré-aquecimento em si** precisa ser finalizado manualmente (o `TiaMcpServer.exe` no Gerenciador de Tarefas).
