# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 语言设置

**优先使用中文回答**，保持专业术语使用英文原词。例如：
- Function、Class、Hook、Filter、Action
- WP_Query、$wpdb、wp_enqueue_script
- template hierarchy、nonce、transient

## 代码注释规范

**所有代码必须使用中文注释**，包括但不限于：
- PHP文件头部说明
- Function和Class的功能描述
- 复杂逻辑的解释说明
- 参数和返回值的说明
- WordPress Hooks的说明

## Skills 使用规范

**执行任务前，必须先检查是否有可用的 SKILLS**

### 任务处理流程

1. **分析用户需求**
   - 理解任务目标和上下文

2. **查询可用 Skills**
   - 检查已安装的全局 skills：
     * document-skills（docx、pdf、pptx、xlsx）
     * example-skills（frontend-design、mcp-builder、webapp-testing 等）
   - 检查项目级 skills（如果存在）

3. **评估 Skill 适用性**
   - 判断任务是否适合使用某个 skill
   - 优先推荐使用相关 skill

4. **告知用户**
   - 如果发现匹配的 skill，主动告知用户
   - 说明使用该 skill 的好处
   - 等待用户确认后再调用

### 已安装的 Skills 参考

**文档处理 Skills（document-skills）：**
- docx - Microsoft Word 文档创建、编辑、转换
- pdf - PDF 文档解析、表单提取、合并拆分
- pptx - PowerPoint 演示文稿创建和编辑
- xlsx - Excel 表格处理、数据分析

**开发与设计 Skills（example-skills）：**
- frontend-design - 前端 UI 设计转换（HTML/CSS/React）
- canvas-design - Canvas 图形和视觉设计
- algorithmic-art - 算法艺术生成
- theme-factory - 主题生成器
- mcp-builder - MCP 服务器构建
- webapp-testing - Web 应用测试（Playwright）
- web-artifacts-builder - Web 资源构建器
- skill-creator - Skill 创建助手
- brand-guidelines - 品牌规范应用
- internal-comms - 内部通讯文档
- doc-coauthoring - 文档协作
- slack-gif-creator - Slack GIF 创建

### 示例场景

**场景 1：用户要求创建前端界面**
```
用户："创建一个响应式导航栏"
Claude：检测到 frontend-design skill 可用，
      建议使用该 skill 以获得更好的设计质量。
      是否使用？(等待确认)
```

**场景 2：用户需要处理文档**
```
用户："提取这个 PDF 的表单字段"
Claude：检测到 pdf skill 可用于此任务，
      是否使用 pdf skill 完成？（等待确认）
```

**场景 3：没有匹配的 skill**
```
用户："修改 WordPress 的 functions.php"
Claude：此任务没有特定的 skill，
      直接使用标准开发流程完成。
```

### 重要原则

- ✅ **主动查询** - 每次任务前都检查可用 skills
- ✅ **明确告知** - 告知用户哪些 skills 可能有用
- ✅ **等待确认** - 未经用户确认不自动调用 skill
- ✅ **提供建议** - 即使不使用 skill，也告知用户有这个选项
