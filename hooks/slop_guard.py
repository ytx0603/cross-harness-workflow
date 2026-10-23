#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PreToolUse Hook — 纯净载荷物理拦截门（Anti-Slop & Zero Meta-Commentary Guard）
Antigravity 契约：
  stdin 收 {"toolCall":{"name":...,"args":{...}},...}
  stdout 出 {"decision":"allow|deny|ask|force_ask", "reason":"..."}
目标：物理拦截模型在交付物（代码、文件、文档）中夹带自我辩解、历史穿帮、反向立牌坊（如“绝对不含之前那个傻逼的东西”或解释“为什么之前是错的”）。
"""

import sys
import json
import re

def main():
    try:
        raw = sys.stdin.read()
    except Exception:
        raw = ""

    if not raw.strip():
        print(json.dumps({"decision": "allow"}))
        return

    try:
        data = json.loads(raw)
    except Exception:
        # 非 JSON 输入不阻断
        print(json.dumps({"decision": "allow"}))
        return

    tool_call = data.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    tool_args = tool_call.get("args", {})

    write_tools = {"write_to_file", "replace_file_content", "multi_replace_file_content"}
    if tool_name not in write_tools:
        print(json.dumps({"decision": "allow"}))
        return

    # 获取目标文件路径
    target_file = ""
    for k in ["TargetFile", "target_file", "AbsolutePath", "absolute_path", "FilePath", "file_path"]:
        if k in tool_args and tool_args[k]:
            target_file = str(tool_args[k])
            break

    # 治理资产与规则文件白名单放行（避免讨论规则本身时被拦截）
    whitelist_keywords = [
        "principles.md",
        "lessons_learned.md",
        "pre_write_slop_guard",
        "selfcheck.ps1",
        "inspector.md",
        "reviewer.md",
        "test_slop_guard",
        "SKILL.md"
    ]
    if any(kw in target_file for kw in whitelist_keywords):
        print(json.dumps({"decision": "allow"}))
        return

    # 提取写入或替换的内容
    content_parts = []
    for k in ["CodeContent", "ReplacementContent", "Content", "content"]:
        if k in tool_args and tool_args[k]:
            content_parts.append(str(tool_args[k]))

    full_content = "\n".join(content_parts)
    if not full_content.strip():
        print(json.dumps({"decision": "allow"}))
        return

    # 违规元解释/自辩/历史提及/解释为何放弃模式库
    meta_patterns = [
        r"绝对不含",
        r"不包含之前",
        r"不再包含之前",
        r"不再有之前",
        r"去掉了之前",
        r"去除了之前",
        r"删除了之前",
        r"移除了之前",
        r"根据要求去掉",
        r"根据要求删除",
        r"按照要求去掉",
        r"按照要求删除",
        r"根据反馈去掉",
        r"根据反馈删除",
        r"之前.{0,20}是错的",
        r"此前.{0,20}是错的",
        r"此前.{0,20}是错误的",
        r"上一版.{0,20}有问题",
        r"之前那个.{0,20}傻逼",
        r"之所以去掉.{0,20}是因为",
        r"之所以放弃",
        r"放弃.{0,15}是因为",
        r"放弃使用",
        r"不采用.{0,15}是因为",
        r"不使用.{0,15}是因为",
        r"不在.{0,15}是因为",
        r"不用.{0,15}是因为",
        r"未采用.{0,15}是因为",
        r"没有采用.{0,15}是因为",
        r"修正了之前",
        r"纠正了上一版",
        r"注[：:].{0,10}已剔除",
        r"注意[：:].{0,10}不含",
        r"注意[：:].{0,10}去掉了",
        r"注意[：:].{0,10}不再有",
        r"不再含有之前",
        r"修复了上一版关于",
        r"//.{0,10}不再包含",
        r"//.{0,10}去掉了",
        r"#.{0,10}不再包含",
        r"#.{0,10}去掉了",
        r"<!--.{0,10}不再包含",
        r"<!--.{0,10}去掉了"
    ]

    # 技术文档与代码中严禁出现的假大空/套话词汇库
    marketing_slop_patterns = [
        r"工业级",
        r"丝滑",
        r"无缝",
        r"极致",
        r"大刀阔斧",
        r"降维打击",
        r"自研黑科技",
        r"遥遥领先"
    ]

    forbidden_patterns = meta_patterns + marketing_slop_patterns

    matched_pattern = None
    matched_text = ""
    for pat in forbidden_patterns:
        m = re.search(pat, full_content)
        if m:
            matched_pattern = pat
            matched_text = m.group(0)
            break

    if matched_pattern:
        reason = (
            f"【物理硬拦截】检测到交付物中夹带元解释/自我辩解/历史穿帮废话（命中违规片段：'{matched_text}'）。\n"
            f"硬约束红线：交付物文件必须是 100% 纯净目标实体（Pure Payload）。\n"
            f"严禁在代码、正文、注释或修改内容中提及'之前被删的内容'，严禁写'绝对不含XX'，严禁解释'为什么之前是错的'！\n"
            f"请立刻剔除一切自我辩解与过程性废话，仅保留纯净、合规的有效代码/文档内容后重试。"
        )
        print(json.dumps({"decision": "deny", "reason": reason}, ensure_ascii=False))
        return

    # 放行
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
