# PreInvocation Hook — 每轮注入开机自检 + 搜索门
# Antigravity 契约：stdin 收 JSON，stdout 出 {"injectSteps":[{"ephemeralMessage":"..."}]}
#
# 设计原则：本 hook 每轮都执行，注入的内容长期占据 flash 的注意力。
# 详细规则已由 GEMINI.md（每轮加载）承载，此处只保留最容易忘、违反代价最高的提醒。
# 不要再往这里加内容——加之前先问：GEMINI.md 或 search-discipline SKILL 里有了吗？

$ErrorActionPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

# 排空 stdin，避免管道阻塞
try { $null = [Console]::In.ReadToEnd() } catch {}

$msg = @'
[开机自检]
1. 第一行写 Token 行
2. 先读 C:\Users\Lenovo\.claude\memory\principles.md。禁读 Desktop/Documents/Downloads，不猜不翻
3. SubAgent 靠"注册"不靠"扮演"，详见 .gemini\config\skills\antigravity-selfcheck\SKILL.md
4. 搜索门 → 本轮答案若涉及【版本号 / 产品型号 / 没见过的代号 / 报错原文 / 价格基准 / 选型推荐 / 训练截止后的事】：先用搜索工具查，禁止凭参数记忆直接答。判据："会随时间变吗？""我是在回忆还是在确认？"
'@

$payload = @{
    injectSteps = @(
        @{ ephemeralMessage = $msg }
    )
}

$payload | ConvertTo-Json -Depth 6 -Compress
