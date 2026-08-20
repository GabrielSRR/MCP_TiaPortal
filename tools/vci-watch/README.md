# TIA VCI 看门狗

博途里的程序一变，就自动导出成文本、写 change log、git 提交。**不需要任何手动操作。**

## 它做什么 / 不做什么

**做**：
- 每轮：博途在跑吗 → 附着到你已经打开的工程 → 问 VCI「哪些块和文本文件不一致」→
  有变更就导出（`ProjectToWorkspace`）→ 写 `CHANGELOG.md` → `git commit`。
- 没变更 → **一声不吭**，不产生空提交。

**绝不做**（改代码前先读这三条）：
1. **绝不打开博途、绝不打开工程**。博途没开就直接退出。你的工程只能 Attach —— 这是红线。
2. **绝不往工程里写**。只做 `ProjectToWorkspace` 一个方向，永远不调 `WorkspaceToProject`，
   也不调 `SaveProject`。存不存盘是你的决定。
3. **绝不替你编译**（除非你在 config 里显式打开 `autoCompile`）。

## 一个必须知道的限制：改完要编译，才导得出

西门子的规矩：块改动后处于 inconsistent 状态，VCI 拒绝导出 ——
`The block is inconsistent. Compile the block prior to export.`

所以：
- **检测**：改完立刻就能检测到（**哪怕你还没存盘**，实测确认）。
- **导出/提交**：要等这个块被编译过。你在博途里编译一次，下一轮看门狗就自动补上。
- 想省这一步 → config 里 `"autoCompile": true` 并列出 `compileSoftwarePaths`，
  它会自己编译再导出（注意：编译是写操作，会改工程状态）。

另一个限制：**专有技术保护（know-how protected）的块导不出**，
VCI 明确拒绝（真实项目里遇到过一个这样的 FB），这类块进不了版本管理。
**硬件组态也进不了 VCI**，只有程序侧（块 / 变量表 / UDT）。

## 配置 `config.json`

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

`workspaceFolder` 必须同时是 **VCI 工作区**和 **git 工作树**。
工程侧要先做过一次 `ConnectProjectToWorkspace`（整工程自动纳管），看门狗才有东西可看。

## 跑

- 手动跑一轮：`python watch.py`
- 定时跑：`register-task.ps1`（注册 Windows 计划任务，默认 10 分钟一轮），
  卸载：`register-task.ps1 -Remove`
- 日志：`log\watch-YYYYMMDD.log`（每轮重算文件名，跨天不会堆进同一个文件）

## 已验证（真实项目，345 个对象）

- 无变更 → 不动作、不提交（反向哨兵，实测通过）
- 工程侧改了**且未保存** → 检测到
- **✅ 在博途 UI 里手改并编译 → 全自动检测、导出、写 CHANGELOG、git 提交**
  （现场验证：在博途里给某个块加了一句行注释并编译，看门狗自动导出并提交）
- 改了但未编译 → 只记「待编译」，**不误报失败、不提交**
- 编译后 → 自动导出 + 写 CHANGELOG + 提交，diff 里是真实的块内容变化
- VCI 的 `Unequal` **不等于内容变了**：git checkout/pull 把文件原样重写（时间戳变）也会判 Unequal，
  所以提交前还要看 `git status` 有没有真差异，否则会刷空提交（这个坑实测踩到过）


## 资源管控（不许拖慢本机）

实测一轮开销（博途界面开着一个 345 个对象的工程时）：
**无变更约 81~95 秒；有变更（含导出+提交）实测 273 秒**。引擎峰值内存约 72 MB，跑完进程数回到原样。
所以 10 分钟一轮不会叠加，但间隔别设到 5 分钟以下。
耗时几乎全在状态检查——345 个对象逐个问 Openness；同一操作在无头实例只要 3~10 秒，
GUI 实例慢是因为要和界面抢同一个引擎。

为此做了六道闸：
1. **博途没在跑 → 直接退出**，绝不为了检查而拉起博途。
2. **引擎降到 BelowNormal 优先级**，不跟你正在操作的博途抢 CPU；计划任务本身也设为低优先级(7)。
3. **单实例锁**：上一轮没跑完就跳过这一轮，绝不叠加（10 分钟一轮 vs 一轮 81 秒）。
   锁超过 `lockTimeoutSeconds`(默认 900s) 视为卡死，自动接管。
4. **硬超时** `cycleTimeoutSeconds`(默认 **600s**)：守护线程到点**真的杀引擎**，不是只记一行日志。
   已用故障注入验过（把超时调到 5 秒 → 引擎被掐断、退出码 1、无残留）。计划任务另有 15 分钟上限兜底。
5. **残留自清**：把自己引擎的 PID 记在 `watch.state.json`，下一轮开头核对命令行后清掉上一轮卡死的。
   **只认自己记下的 PID，绝不按进程名批量杀** —— 同一个 exe 别的 Claude 会话也在用。
6. **绝不留孤儿博途**：收尾时杀掉「父进程是本轮引擎」的博途实例；
   你自己开的 GUI（父进程是 explorer）绝对不碰。

暂停/恢复/卸载：
```powershell
Disable-ScheduledTask TiaVciWatch      # 临时停
Enable-ScheduledTask  TiaVciWatch
.\register-task.ps1 -Remove            # 彻底卸载
.\register-task.ps1 -IntervalMinutes 30  # 改间隔
```
