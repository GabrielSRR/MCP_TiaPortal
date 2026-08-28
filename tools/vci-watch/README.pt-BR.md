# Watchdog VCI do TIA

Quando um programa no TIA é alterado, ele é exportado automaticamente como texto, o changelog é atualizado e um commit Git é criado. **Nenhuma operação manual é necessária.**

## O que ele faz / o que não faz

**Faz**:
- A cada ciclo: verifica se o TIA está em execução → anexa ao projeto que você já abriu → consulta ao VCI quais blocos e arquivos de texto estão inconsistentes →
  exporta as alterações (`ProjectToWorkspace`) → atualiza `CHANGELOG.md` → executa `git commit`.
- Sem alterações → **não faz nada**, sem criar commits vazios.

**O que ele nunca faz** (leia estas três regras antes de alterar o código):
1. **Nunca abre o TIA nem um projeto**. Se o TIA não estiver aberto, encerra imediatamente. O projeto só pode ser anexado — esta é uma regra rígida.
2. **Nunca grava no projeto**. Executa somente na direção `ProjectToWorkspace`, nunca chama `WorkspaceToProject`
   nem `SaveProject`. Salvar ou não é decisão sua.
3. **Nunca compila por você** (exceto quando `autoCompile` for explicitamente habilitado na configuração).

## Uma limitação importante: é preciso compilar antes de exportar

Regra da Siemens: depois de alterado, um bloco fica no estado inconsistente e o VCI recusa a exportação —
`The block is inconsistent. Compile the block prior to export.`

Portanto:
- **Detecção**: a alteração é detectada imediatamente (**mesmo que você ainda não tenha salvado**, conforme validado em testes).
- **Exportação/commit**: é preciso esperar o bloco ser compilado. Compile-o uma vez no TIA; no ciclo seguinte o watchdog concluirá o processo automaticamente.
- Para eliminar essa etapa → defina `"autoCompile": true` na configuração e liste `compileSoftwarePaths`;
  o watchdog compilará antes de exportar (atenção: compilação é uma operação de escrita e altera o estado do projeto).

Outra limitação: **blocos protegidos por know-how não podem ser exportados**;
o VCI os recusa explicitamente (isso ocorreu com um FB em um projeto real), portanto esses blocos não entram no controle de versão.
**A configuração de hardware também não entra no VCI**; somente o lado do programa (blocos / tabelas de variáveis / UDTs).

## Configuração em `config.json`

```json
{
  "enginePath": "E:\\PID博途块\\MCP\\_bulaofen_release\\runtime\\v21\\TiaMcpServer.exe",
  "tiaMajorVersion": 21,
  "workspaceFolder": "C:\\path\\to\\your-git-worktree",
  "workspaceName": "git",
  "gitAuthor": "tia-vci-watch <watch@local>",
  "autoCompile": false,
  "compileSoftwarePaths": ["PLC_1"]
}
```

`workspaceFolder` deve ser simultaneamente a **área de trabalho VCI** e a **árvore de trabalho Git**.
No projeto, é necessário executar primeiro `ConnectProjectToWorkspace` (gerenciamento automático do projeto inteiro); só então o watchdog terá algo para monitorar.

## Execução

- Executar um ciclo manualmente: `python watch.py`
- Executar periodicamente: `register-task.ps1` (registra uma tarefa agendada do Windows; padrão de um ciclo a cada 10 minutos);
  remover: `register-task.ps1 -Remove`
- Log: `log\watch-YYYYMMDD.log` (o nome do arquivo é recalculado a cada ciclo, evitando acumular dias diferentes no mesmo arquivo)

## Validação realizada (projeto real, 345 objetos)

- Sem alterações → nenhuma ação e nenhum commit (sentinela reverso, validado em teste)
- Alteração feita no projeto **sem salvar** → detectada
- **✅ Alteração manual na interface do TIA seguida de compilação → detecção, exportação, atualização do CHANGELOG e commit Git totalmente automáticos**
  (validação em campo: uma linha de comentário foi adicionada a um bloco no TIA e compilada; o watchdog exportou e confirmou automaticamente)
- Alterado, mas não compilado → apenas registra “aguardando compilação”, **sem reportar uma falha incorretamente e sem fazer commit**
- Após a compilação → exportação automática + atualização do CHANGELOG + commit; o diff contém a alteração real do bloco
- `Unequal` no VCI **não significa que o conteúdo mudou**: `git checkout`/`pull` pode regravar os arquivos sem alterações de conteúdo (mudando o timestamp), o que também resulta em `Unequal`;
  por isso, antes do commit é preciso verificar se `git status` mostra diferenças reais; caso contrário, commits vazios podem ser criados (esse problema ocorreu em um teste real)

## Controle de recursos (não deixe o computador lento)

Custos medidos por ciclo (com a interface do TIA aberta em um projeto com 345 objetos):
**aproximadamente 81–95 segundos sem alterações; 273 segundos com alterações (incluindo exportação e commit)**. O pico de memória do mecanismo foi de aproximadamente 72 MB, e o número de processos voltou ao valor original ao final.
Por isso, um ciclo a cada 10 minutos não se sobrepõe, mas não defina intervalos inferiores a 5 minutos.
Quase todo o tempo é gasto na verificação de estado — os 345 objetos são consultados individualmente pelo Openness; a mesma operação em uma instância headless leva apenas de 3 a 10 segundos.
A instância GUI é mais lenta porque precisa compartilhar o mesmo mecanismo com a interface.

Foram adotadas seis proteções:
1. **Se o TIA não estiver em execução → encerra imediatamente**, sem iniciá-lo apenas para verificar.
2. **O mecanismo usa prioridade BelowNormal**, sem disputar CPU com o TIA que você está usando; a própria tarefa agendada também usa prioridade baixa (7).
3. **Bloqueio de instância única**: se o ciclo anterior ainda não terminou, o ciclo atual é ignorado, sem sobreposição (um ciclo de 10 minutos contra um ciclo de 81 segundos).
   Se o bloqueio exceder `lockTimeoutSeconds` (padrão 900 s), será considerado travado e assumido automaticamente.
4. **Tempo limite rígido** `cycleTimeoutSeconds` (padrão **600 s**): ao atingir o limite, o watchdog **encerra de fato o mecanismo**, em vez de apenas registrar uma linha no log.
   Isso foi validado com injeção de falha (limite ajustado para 5 segundos → mecanismo interrompido, código de saída 1 e nenhum resíduo). A tarefa agendada possui ainda um limite de segurança de 15 minutos.
5. **Limpeza automática de resíduos**: o PID do próprio mecanismo é salvo em `watch.state.json`; no início do ciclo seguinte, a linha de comando é verificada e o processo travado anterior é encerrado.
   **Somente o PID salvo pelo próprio watchdog é aceito; nunca há encerramento em massa por nome de processo** — outra sessão do Claude pode estar usando o mesmo executável.
6. **Nunca deixa instâncias órfãs do TIA**: ao finalizar, encerra instâncias do TIA cujo processo pai seja o mecanismo do ciclo atual;
   a interface GUI aberta por você (cujo processo pai é o Explorer) nunca é tocada.

Pausar/retomar/desinstalar:
```powershell
Disable-ScheduledTask TiaVciWatch      # pausa temporária
Enable-ScheduledTask  TiaVciWatch
.\register-task.ps1 -Remove            # desinstalação completa
.\register-task.ps1 -IntervalMinutes 30  # altera o intervalo
```

## Recuo: por que ele não permanece conectado ao TIA (2.5.1)

O erro mais comum na automação por polling é tratar um **estado de falha estável** como um **erro pontual** e tentar novamente sem parar.

Caso real: havia 11 blocos alterados, mas não compilados. A cada ciclo esses blocos eram considerados “alterados”,
e a exportação falhava sempre com `The block is inconsistent` — **não importa quantas vezes se tente, o resultado não muda**.

O resultado era um ciclo completo a cada rodada (com pendências, um ciclo chegou a **533 segundos**: 345 consultas de estado + 11 exportações destinadas a falhar),
enquanto a tarefa era executada a cada 2 minutos. Assim, o ciclo seguinte começava logo após o anterior, mantendo o watchdog quase permanentemente conectado ao TIA e fazendo a interface piscar continuamente.

Agora existem três proteções:

| Proteção | Parâmetro | Função |
|---|---|---|
| Recuo de compilação pendente | `pendingCompileCooldownMinutes` (padrão 30) | Se todas as falhas de um ciclo forem **“não compilado”**, não tenta novamente durante o período de recuo. A condição de desbloqueio é uma alteração no diretório do projeto (a compilação grava em `XRef\`), não apenas a passagem do tempo |
| Intervalo mínimo entre verificações completas | `minFullCheckMinutes` (padrão 10) | Um ciclo com alterações pode levar vários minutos; intervalos curtos fazem os ciclos se encadearem e manterem uma conexão permanente |
| Verificação completa de segurança | `forceFullCheckMinutes` (padrão 60) | Mesmo que nenhum sinal tenha mudado, executa periodicamente uma verificação completa, sem depender apenas de heurísticas |

Quando está ocioso, cada ciclo termina em **0,37 segundo** (sem iniciar sequer o mecanismo). Recomenda-se um intervalo de **5 minutos** na tarefa agendada.

> Princípio em uma frase: **toda falha cujo resultado não possa mudar com novas tentativas deve usar recuo, e a condição para liberar o recuo deve estar vinculada a uma mudança de estado externa.**

## Como ele determina se o TIA está aberto (2.5.2)

**Ele não conta os processos `Siemens.Automation.Portal.exe`.** Em uma máquina podem existir simultaneamente três tipos:

| Processo | Característica da linha de comando | Conta como “TIA aberto por você”? |
|---|---|---|
| GUI aberta por você ao clicar duas vezes em `.apXX` | Apenas o caminho do projeto | ✅ Sim |
| Processo auxiliar iniciado pela própria GUI | `-bootstrapper=…BackgroundProcessBootStrapper` + `-processId=<PID da GUI>` | ❌ Não |
| Instância headless iniciada por outro cliente Openness | `-bootstrapper=…Openness.Loader.BootStrapper` | ❌ Não |

Testes mostram que uma GUI com um projeto aberto corresponde a **3 processos**. Julgar pela quantidade de processos causa dois problemas, sendo o segundo um incidente real:

1. Superestimação — um único projeto aberto parece representar três projetos.
2. **Loop autossustentado** — uma máquina sem projeto aberto, mas com um resíduo headless, também conta 1.
   O watchdog conclui que “o TIA está aberto” → inicia o mecanismo → não encontra projeto para anexar →
   **inicia outra instância headless** → é interrompido pelo limite de 600 segundos → deixa um resíduo que faz o próximo ciclo continuar contando 1.
   Em testes, isso manteve um loop durante toda a noite, uma vez a cada 72 minutos, com logs sempre informando “o ciclo excedeu 600 segundos; mecanismo interrompido por travamento”.

Por isso, agora existem duas proteções:

- **Antes de iniciar o mecanismo**: qualquer processo com `-bootstrapper=` é ignorado; somente sessões GUI reais são contadas.
- **Antes de `Connect`**: `ListPortalProcessProjects` (que apenas detecta processos já em execução e não inicia o TIA)
  confirma que há um projeto real ao qual anexar; caso contrário, o ciclo termina. `Connect` pode iniciar o TIA, portanto não deve ser usado para “ajudar”.

**Limpeza adicional de resíduos**: o limite de 15 minutos da tarefa agendada é menor que o pior caso de um ciclo; se o script inteiro for encerrado, o código de finalização não será executado,
e a instância headless ficará consumindo memória (em um teste, uma permaneceu travada por um dia inteiro). Agora, antes de iniciar, o PID é salvo em
`watch.state.json`; no início do ciclo seguinte, ele é validado pela **linha de comando completa** e então encerrado — somente
`Openness.Loader.BootStrapper` é aceito. Como esse texto não aparece na linha de comando da sua GUI, ela não pode ser encerrada por engano.
