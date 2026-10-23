# PostToolUse Hook — 代码文件改动后打标记
# Antigravity 契约：stdin 收 {"stepIdx":N,"error":"...",...}，stdout 必须出空 JSON {}
# 对应 Claude Code 的 posttooluse-code-check.ps1
# 作用：改到代码文件时，在 ~/.claude/.state/ 落下 planner-flag / review-flag，
#       供后续流程判断"这个改动是否需要补 Planner 出 spec / Reviewer 审查"

$ErrorActionPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$raw = ''
try { $raw = [Console]::In.ReadToEnd() } catch {}

$fp = ''
try {
    $d = $raw | ConvertFrom-Json
    foreach ($k in @('TargetFile', 'target_file', 'AbsolutePath', 'absolute_path',
                     'file_path', 'FilePath')) {
        $v = $d.toolCall.args.$k
        if (-not [string]::IsNullOrWhiteSpace($v)) { $fp = $v; break }
    }
} catch { }

$codeExts = @(
    '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.vue',
    '.java', '.go', '.rs', '.c', '.cpp', '.rb', '.php', '.swift', '.kt',
    '.sh', '.ps1', '.bat', '.json', '.yaml', '.yml', '.toml',
    '.conf', '.cfg', '.ini', '.env'
)

$flagDir = Join-Path $env:USERPROFILE '.claude\.state'
New-Item -ItemType Directory -Force -Path $flagDir | Out-Null

if (-not [string]::IsNullOrWhiteSpace($fp)) {
    $ext = [System.IO.Path]::GetExtension($fp).ToLower()
    if ($codeExts -contains $ext) {
        Get-Date -Format 's' | Out-File (Join-Path $flagDir 'planner-flag') -Encoding utf8
        Get-Date -Format 's' | Out-File (Join-Path $flagDir 'review-flag')  -Encoding utf8
    }
}

# PostToolUse 必须回空对象
'{}'
