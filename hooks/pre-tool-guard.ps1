# PreToolUse Hook — 写操作确认门
# Antigravity 契约：stdin 收 {"toolCall":{"name":...,"args":{...}},...}
# stdout 出 {"decision":"allow|deny|ask|force_ask", "reason":"..."}
# 对应 Claude Code 的 pre-modify-guard.ps1（CC 里只打印提醒，这里升级为真实拦截）

$ErrorActionPreference = 'SilentlyContinue'
$OutputEncoding = [System.Text.Encoding]::UTF8
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$raw = ''
try { $raw = [Console]::In.ReadToEnd() } catch {}

$tool = '(unknown)'
$target = ''

try {
    $d = $raw | ConvertFrom-Json
    if ($d.toolCall.name) { $tool = $d.toolCall.name }
    # 兼容不同版本的参数键名
    foreach ($k in @('TargetFile', 'target_file', 'AbsolutePath', 'absolute_path',
                     'file_path', 'FilePath', 'CommandLine', 'command_line', 'Command')) {
        $v = $d.toolCall.args.$k
        if (-not [string]::IsNullOrWhiteSpace($v)) { $target = $v; break }
    }
} catch { }

if ($target.Length -gt 300) { $target = $target.Substring(0, 300) + '...' }

$reason = "写操作即将执行：[$tool] $target  —— 你已在回复里用一句话说明这次改动了吗？没确认就按 Deny 中断。"

$out = @{
    decision = 'ask'
    reason   = $reason
}

$out | ConvertTo-Json -Depth 5 -Compress
