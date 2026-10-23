# Agent 工作流 HANDOFF

> 新会话启动必读。本文件定义 Agent 调用流程、红线边界、心跳规则、输出管道。

## 调用时机

| 场景 | Agent | 说明 |
|:----|:-----|:-----|
| 代码任务开始 | **Coordinator** | 第一个调。只分派不干活，分完就结束 |
| 任何 Edit/Write 前 | **PreToolUse Hook** | 自动弹出黄色确认框，不需手动调用 |
| 协调完成拿到分派单 | **Planner** | 审分派单、出 spec |
| spec 就绪，改码前 | **Preflight** | 安全检查：切隔离分支、拒绝在主分支写代码。不过不放行 |
| Preflight PASS | **Generator** | 按 spec 写代码，**每文件改完立即 git commit**。不自评"全部修复" |
| Generator 交付后 | **Reviewer** | **读改完的文件，逐行验证。不信 Generator 的自评** |
| 有可运行应用 | **Evaluator** | 行为测试，不读代码 |
| 每次回复末尾 | **Inspector** | 最后一道关，不可越过 |

## 并行 / 串行规则

- **多文件无重叠** → Reviewer×N 或 Generator×N 可并行
- **同文件** → Generator 必须串行。多个 Generator 不能同时改同一个文件
- **共享目录** → `.agent_outputs/` 存中间产物（分派单、spec、审查报告）

## 红线速查

- **Coordinator**: 只分派，不自干
- **Generator**: 只写代码，报告"改了什么"而非"修没修好"。不自评"X/Y PASS"。**每文件改完立即 git commit，禁止在 main/master 上写代码**
- **Reviewer**: 必须读代码核实 Generator 声明。不读到就信 = 失职
- **Inspector**: 最后一道关。Generator 自评不可信
- **Planner**: 只出 spec，不读源码验证
- **Preflight**: Generator 启动前强制安全检查。切隔离分支、审核环境变量。不通过不放行

## 心跳

每个 Agent 启动后 60 秒：SendMessage 问进度。2 次无响应 → 杀。

## 输出管道

Agent A 输出 → 写入 `.agent_outputs/{agent}_output.md` → Agent B prompt 里引用路径。
不要只贴摘要——贴原文或文件路径，避免下一个 Agent 找不到。
