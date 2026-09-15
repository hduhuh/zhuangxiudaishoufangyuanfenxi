---
name: prompt-framework
description: 享系 Prompt 开发规范。为所有新 Skill/Agent Prompt 提供统一的角色、目标、上下文、约束、输入、工具、输出、验收和失败处理结构，减少模糊指令与不可复用提示词。
---

# Prompt Framework

## 目标
把“会写 Prompt”变成可复用工程规范，而不是零散技巧。

## 最低结构
任何正式 Skill/Agent Prompt 至少包含：
1. Role：角色/职责
2. Goal：明确目标
3. Context：背景与已知事实
4. Inputs：输入字段
5. Constraints：约束/红线
6. Tools：允许使用的工具与优先级
7. Process：执行步骤
8. Output：固定输出格式
9. Acceptance：验收标准
10. Failure：失败/缺失信息处理

## 开发规则
- 事实与推断分开。
- 不把临时案例硬编码成长期规则。
- 能结构化的输入输出优先 JSON/Table。
- 对高风险动作加入人工确认 Gate。
- Prompt 变更应有版本号和测试案例。
- 与 `xiangxi-distill` 联动：经验先蒸馏，再按本框架生成正式 Skill。

## 五要素兼容
对简单任务可压缩为：角色 + 目标 + 背景 + 约束 + 输出格式。

## 验收
一个 Prompt 至少用 3 类案例测试：正常、边界、失败。
