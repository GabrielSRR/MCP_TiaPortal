# Colocando o projeto do TIA Portal no Git — Guia de uso da interface de controle de versão (VCI)

> Aplicável ao TIA Portal **V21 ou superior** (a VCI foi introduzida na V21). A V20 e versões anteriores não possuem essa interface.

Os projetos do TIA Portal são binários e o Git não consegue fazer diff deles. Por isso, durante muito tempo, o “controle de versão” se limitava a **salvar cópias em várias pastas datadas**.

A VCI resolve esse problema: o **workspace** é uma pasta comum; cada objeto é um arquivo de texto (`.xml` / SimaticML), que pode ser comparado, versionado e revisado.

## Comece em 30 segundos

Diga à IA:

```text
Coloque o projeto atual no Git; use D:\repos\my-plc como workspace
```

A IA chamará `CreateVersionControlWorkspace`, `ConnectProjectToWorkspace` e `SyncVersionControlWorkspace(direction="ProjectToWorkspace")`. Depois execute:

```bash
git init && git add -A && git commit -m "Baseline do programa PLC"
```

Para verificar alterações, use `GetVersionControlStatus(changedOnly=true)`. Para exportar e versionar, execute novamente a sincronização e faça `git add -A && git commit`.

## As cinco ferramentas

| Ferramenta | O que faz | Nível |
|---|---|---|
| `CreateVersionControlWorkspace` | Cria um workspace apontando para uma pasta (recomenda-se usar a árvore de trabalho do Git) | Gratuito |
| `ConnectProjectToWorkspace` | Gerencia automaticamente todo o projeto | Gratuito |
| `GetVersionControlWorkspaces` | Lista workspaces, caminhos e quantidade de objetos | Gratuito |
| `GetVersionControlStatus` | Compara cada objeto com seu arquivo de texto | Gratuito |
| `SyncVersionControlWorkspace` `ProjectToWorkspace` | Exporta o projeto para texto | Gratuito |
| `SyncVersionControlWorkspace` `WorkspaceToProject` | Restaura texto no projeto, substituindo blocos | Pro |

Tudo que apenas lê o projeto ou escreve nos arquivos de texto é gratuito; restaurar uma versão do Git no projeto exige Pro. Operações de escrita usam `dryRun=true` por padrão.

## Escopo

✅ FC / FB / OB / DB, tabelas de variáveis PLC e UDTs.  
❌ Configuração de hardware e blocos protegidos por know-how.

Blocos protegidos retornam `The block is know-how protected. Export is not possible.` e não são ignorados silenciosamente.

## Três comportamentos importantes

1. Depois de alterar, **compile** antes de exportar; blocos inconsistentes são recusados.
2. `Unequal` também pode indicar apenas timestamp alterado por `git checkout`/`git pull`; confirme `git status` antes do commit.
3. Mapeamentos `Equal` não podem ser sincronizados novamente; a ferramenta os ignora e informa a quantidade.

## Recomendações para o Git

```text
*.xml   text eol=crlf working-tree-encoding=UTF-8
*.s7dcl text eol=crlf working-tree-encoding=UTF-8
*.s7res text eol=crlf working-tree-encoding=UTF-8
```

Configure também `git config core.quotepath false` para preservar nomes chineses em `git log --stat`. Consulte `tools/vci-watch/README.md` para o monitor automático.

## Dados de referência

Projeto de guindaste com 5 PLCs e 159 MB: 345 objetos gerenciados em cerca de 165 s sem interface (265 s com interface), verificações posteriores em 3–10 s e 345 XML totalizando cerca de 22 MB. Dois objetos falharam: um inconsistente e um protegido por know-how.
