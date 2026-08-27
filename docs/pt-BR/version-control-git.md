# Colocando o projeto do TIA Portal no Git — Guia de uso da interface de controle de versão (VCI)

> Aplicável ao TIA Portal **V21 ou superior** (a VCI foi introduzida na V21). A V20 e versões anteriores não possuem essa interface.

Os projetos do TIA Portal são binários e o Git não consegue fazer diff deles. Por isso, durante muito tempo, o “controle de versão” se limitava a **salvar cópias em várias pastas datadas**.

A interface de controle de versão (Version Control Interface) da V21 resolve esse problema: o **workspace** é uma pasta comum; cada objeto é armazenado como um arquivo de texto (`.xml` / SimaticML), que pode ser comparado, versionado e revisado.

Este MCP transforma todo o processo em alguns comandos, **sem precisar clicar em nada na interface do TIA Portal**.

---

## Comece em 30 segundos

Diga à IA:

```
Coloque o projeto atual no Git; use D:\repos\my-plc como workspace
```

A IA chamará, nesta ordem:

```
CreateVersionControlWorkspace(workspaceName="git", folderPath="D:\repos\my-plc")
ConnectProjectToWorkspace(dryRun=false)          ← gerencia automaticamente todo o projeto, sem precisar selecionar nenhum bloco
SyncVersionControlWorkspace(direction="ProjectToWorkspace", dryRun=false)
```

Depois, na pasta:

```bash
git init && git add -A && git commit -m "Baseline do programa PLC"
```

**Pronto.** A partir daí, sempre que o programa for alterado, basta perguntar “quais blocos mudaram?”:

```
GetVersionControlStatus(changedOnly=true)
→ A3_4_Hoist | Unequal | ...
```

Para exportar e fazer o commit:

```
SyncVersionControlWorkspace(direction="ProjectToWorkspace", dryRun=false)
git add -A && git commit -m "Ajuste na distribuição da velocidade de elevação"
```

---

## As cinco ferramentas

| Ferramenta | O que faz | Nível |
|---|---|---|
| `CreateVersionControlWorkspace` | Cria um workspace apontando para uma pasta (**recomenda-se usar a árvore de trabalho do Git**) | Gratuito |
| `ConnectProjectToWorkspace` | **Gerencia automaticamente todo o projeto**: percorre a árvore do projeto e inclui todos os objetos compatíveis no controle de versão | Gratuito |
| `GetVersionControlWorkspaces` | Lista os workspaces (nome, caminho no disco e quantidade de objetos gerenciados) | Gratuito |
| `GetVersionControlStatus` | **Compara objeto por objeto**: mostra quais blocos estão diferentes dos arquivos de texto — essa é a entrada do changelog | Gratuito |
| `SyncVersionControlWorkspace` `direction=ProjectToWorkspace` | Projeto → texto (**exportação; execute antes do commit**) | Gratuito |
| `SyncVersionControlWorkspace` `direction=WorkspaceToProject` | Texto → projeto (**restauração; substitui os blocos do projeto**) | Pro |

A lógica dos níveis é simples: **tudo que apenas lê o projeto ou escreve nos arquivos de texto é gratuito**; a única operação que **altera o projeto** (aplicar uma versão do Git de volta ao projeto) exige o nível Pro.

As operações de escrita usam `dryRun=true` por padrão: primeiro informam o que será feito; após a confirmação, passe `dryRun=false`.

---

## Escopo: o que pode e o que não pode ser gerenciado

✅ **Pode**: FC / FB / OB / DB, tabelas de variáveis do PLC e tipos de dados do PLC (UDT) — ou seja, **todo o lado do programa**.

❌ **Não pode**:
- **Configuração de hardware** (dispositivos, módulos e sub-redes) — a VCI não oferece suporte; `GetSupportedFileFormats` retorna diretamente “não suportado”.
  O hardware ainda precisa de um backup `.ap21` ou de uma exportação CAx/AML.
- **Blocos protegidos por know-how** — o TIA Portal recusa a exportação:
  `The block is know-how protected. Export is not possible.`
  Esses blocos são listados explicitamente no resultado do gerenciamento; não são ignorados silenciosamente.

`ConnectProjectToWorkspace` adota uma abordagem de **granularidade maior primeiro**: quando um objeto pode ser gerenciado como um todo, ele não é dividido em partes menores; objetos incompatíveis são **reportados individualmente**, nunca descartados silenciosamente.

---

## Três comportamentos essenciais (sem eles, você pode achar que a ferramenta está com defeito)

### 1. Depois de alterar, é preciso **compilar** para exportar

Após uma alteração, o bloco fica em estado “inconsistente” e o TIA Portal recusa a exportação:

```
The block is inconsistent. Compile the block prior to export.
```

- A **detecção** não é afetada: é possível identificar imediatamente que o bloco mudou, **mesmo que ele ainda não tenha sido salvo**.
- A **exportação** exige compilação. Compile uma vez no TIA Portal (ou chame `CompileSoftware`) e sincronize novamente.

### 2. `Unequal` não significa necessariamente que o conteúdo mudou

A comparação não verifica apenas o conteúdo. Se `git checkout` / `git pull` reescreverem o arquivo (mesmo conteúdo, mas com alteração no timestamp), ele também será considerado `Unequal`. **Antes do commit, os scripts de automação devem verificar novamente se `git status` indica uma diferença real**; caso contrário, serão criados vários commits vazios.

### 3. Objetos já sincronizados não podem ser “forçados” a sincronizar novamente

Ao chamar a sincronização para um mapeamento com estado `Equal`, o TIA Portal recusa diretamente:

```
Synchronize cannot be called on a workspace mapping that has a compare status of equal.
```

Por isso, esta ferramenta **sempre ignora os objetos `Equal`** e informa no resultado quantos foram ignorados.

---

## Recomendações para o lado do Git

Os arquivos exportados usam **UTF-8 com BOM + CRLF**, e nomes de blocos em chinês são comuns. Crie um `.gitattributes`:

```
*.xml   text eol=crlf working-tree-encoding=UTF-8
*.s7dcl text eol=crlf working-tree-encoding=UTF-8
*.s7res text eol=crlf working-tree-encoding=UTF-8
```

Além disso, configure `git config core.quotepath false` para que os nomes de blocos em chinês não apareçam como escapes octais em `git log --stat`.

---

## Quer automatizar tudo? Consulte `tools/vci-watch/`

O repositório inclui um pequeno monitor: **a cada alteração no programa, ele compila, exporta automaticamente, grava o CHANGELOG e executa `git commit`**. O engenheiro não precisa fazer nada. Ele usa apenas ferramentas do nível gratuito, tem menos de 300 linhas e pode ser adaptado diretamente.

Consulte [`tools/vci-watch/README.md`](../tools/vci-watch/README.md).

---

## Dados de referência de um projeto real

Um projeto de guindaste (5 PLCs, projeto de 159 MB):

| Ação | Quantidade / duração |
|---|---|
| Gerenciamento automático de todo o projeto | **345 objetos**, cerca de 165 segundos sem a interface aberta (cerca de 265 segundos com a interface aberta) |
| Verificação de status subsequente | 3–10 segundos (cerca de 80 segundos com a interface aberta) |
| Exportação de um bloco | Cerca de 2 segundos |
| Tamanho do repositório de texto | 345 arquivos `.xml`, cerca de 22 MB |

Dois objetos não puderam ser gerenciados, e os motivos foram informados claramente: um bloco estava inconsistente (era necessário compilá-lo antes) e o outro era um bloco protegido por know-how.
