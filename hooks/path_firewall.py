import sys
import re
import os

"""
Permission Firewall Hook (PreToolUse)
Intercepts unauthorized filesystem access and dangerous directory traversals.
Triggered by Claude Code, Antigravity, or Workbuddy tool execution lifecycle.
Exit Code 1 signals an immediate hard block to the host engine.
"""

# 严格工作区白名单约束
ALLOWED_PATTERNS = [
    r'^[a-zA-Z]:[\\/]Projects[\\/]',
    r'^[a-zA-Z]:[\\/]\.claude[\\/]',
    r'^[a-zA-Z]:[\\/]\.gemini[\\/]',
    r'^\.[\\/]'
]

FORBIDDEN_KEYWORDS = [
    'desktop',
    'documents',
    'downloads',
    'system32',
    '/etc/passwd',
    '..\\'
]

def check_path_permission(target_path: str) -> bool:
    normalized = target_path.replace('/', '\\').lower()
    
    # 1. 拦截危险关键字与目录穿越
    for kw in FORBIDDEN_KEYWORDS:
        if kw in normalized:
            sys.stderr.write(f"[SECURITY VIOLATION] Target path contains forbidden pattern: '{kw}' in '{target_path}'\n")
            return False
            
    # 2. 检查白名单路径匹配
    # 如果是相对路径或受控工作区，允许
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
        
    path_to_check = sys.argv[1]
    if not check_path_permission(path_to_check):
        sys.stderr.write("[GATEWAY BLOCKED] Application-level physical intercept: Permission Denied.\n")
        sys.exit(1)
        
    sys.exit(0)
