# cross-harness-workflow: Host-Agnostic Agentic Governance Protocol

[![CI Tests](https://github.com/ytx0603/cross-harness-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/ytx0603/cross-harness-workflow/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hosts](https://img.shields.io/badge/Hosts-Claude%20Code%20%7C%20Antigravity%20%7C%20Workbuddy-8A2BE2.svg)](#cross-host-compatibility)

A lightweight, host-agnostic engineering governance & self-correction workflow designed for complex 3D/WebGL applications.

---

## 🎯 Architecture & Philosophy

Instead of reinventing an isolated, fragile agent execution loop from scratch, `cross-harness-workflow` sits on top of battle-tested AI coding engines (**Claude Code**, **Antigravity / Gemini CLI**, and **Workbuddy**).

It leverages native platform primitives:
- **Permission Hooks (`PreToolUse` / `PostToolUse`)**: Enforces application-level physical firewalls using process exit codes (`exit 1` / `exit 2`).
- **Sub-agents Topology**: Enforces strict separation of concerns (`Planner -> Generator -> Evaluator -> Reviewer`).
- **Blackbox Evaluator Gate (Playwright WebGL)**: Validates actual runtime behaviors in a headless browser without reading or rationalizing generated code.

```text
[Task Request]
      │
      ▼
【Planner Agent】 ──► Generates Frozen Spec & Acceptance Contract
      │
      ▼
【Generator Agent】 ──► Produces Code (Restricted by PreToolUse Path Firewall)
      │
      ▼
【Evaluator Agent (Playwright)】 ──► Non-invasive Blackbox Assertion (triangles > 0, non-black screen)
      ├── [FAIL] ──► Formats Diagnostic Stack ──► Loop back to Generator (Self-Correction)
      └── [PASS] ──► 【Reviewer Agent】 (Static Audit) ──► Deliver to Host
```

---

## 🛡️ Cross-Host Compatibility

| Host Engine | Hook Binding Mechanism | Subagent Invocation Protocol |
| :--- | :--- | :--- |
| **Claude Code** | `settings.json` -> PreToolUse / PostToolUse | Native `.claude/agents/*.md` Forking |
| **Antigravity** | `hooks.json` -> PreToolUse Command Handlers | `.gemini/config/agents/*.md` Dispatch |
| **Workbuddy** | Native Tool Gateway Interceptor | Task Orchestrator Matrix |

---

## 🧪 Verified Production Case: Hongyuanpai 3D CDSS Gallery

This governance workflow was battle-tested during the autonomous construction and verification of the **Hongyuanpai Heritage CDSS Gallery (117 Interactive 3D WebGL Relics)**:
- Prevented LLM hallucinated file tampering via `path_firewall.py`;
- Automatically detected Three.js shader crashes, blank canvas renders (`(0,0,0)` pixels), and missing meshes via headless WebGL assertions;
- Completed zero-human-intervention self-correction loops.

---

## 🚀 Running Tests

```bash
git clone https://github.com/ytx0603/cross-harness-workflow.git
cd cross-harness-workflow

python -m unittest discover tests
```

Expected output:
```text
Ran 3 tests in 0.001s
OK
```

## License
MIT License.
