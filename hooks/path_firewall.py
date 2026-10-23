"""
Permission Firewall Hook (PreToolUse)
Intercepts unauthorized filesystem access and dangerous directory traversals.
Triggered by Claude Code, Antigravity, or Workbuddy tool execution lifecycle.
Exit Code 1 signals an immediate hard block to the host engine.
"""

import sys
import os

ALLOWED_PREFIXES = (
    "projects",
    ".claude",
    ".gemini"
)

FORBIDDEN_KEYWORDS = (
    "desktop",
    "documents",
    "downloads",
    "system32",
    "/etc/passwd",
    ".."
)

def check_path_permission(target_path: str) -> bool:
    if not target_path:
        return True
        
    normalized = os.path.normpath(target_path).lower()
    
    # 1. 拦截危险目录与目录穿越
    for kw in FORBIDDEN_KEYWORDS:
        if kw in normalized:
            sys.stderr.write(f"[SECURITY VIOLATION] Target path contains forbidden pattern: '{kw}' in '{target_path}'\n")
            return False
            
    # 2. 检查白名单范围 (如果在系统驱动器下，必须落在受控目录)
    # 允许相对路径或白名单前缀
    parts = normalized.split(os.sep)
    # 检查路径片段中是否含有白名单根目录
    has_allowed = any(prefix in parts for prefix in ALLOWED_PREFIXES)
    is_relative = not os.path.isabs(target_path) and not target_path.startswith(("\\", "/"))
    
    if not (has_allowed or is_relative):
        sys.stderr.write(f"[SECURITY VIOLATION] Target path outside authorized projects directory: '{target_path}'\n")
        return False
        
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
        
    path_to_check = sys.argv[1]
    if not check_path_permission(path_to_check):
        sys.stderr.write("[GATEWAY BLOCKED] Application-level physical intercept: Permission Denied.\n")
        sys.exit(1)
        
    sys.exit(0)
