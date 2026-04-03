<div align="right">

[English](#-openscientist) · [中文](#中文版本)

</div>

<div align="center">

# 🌍 OpenScientist

[![GitHub stars](https://img.shields.io/github/stars/OpenScientists/OpenScientist?style=social)](https://github.com/OpenScientists/OpenScientist/stargazers) [![GitHub forks](https://img.shields.io/github/forks/OpenScientists/OpenScientist?style=social)](https://github.com/OpenScientists/OpenScientist/fork) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

> 🏛️ *Building the Library of Alexandria for AGI — Accelerating Automated Scientific Discovery*
>
> **为 AGI 建一座亚历山大图书馆，加速自动化科学发现。**

<br>

**Our mission:** Unite the knowledge of the world's top experts across every domain — to accelerate AI-driven scientific discovery.

**Call for action:** Share your research expertise. Together, we create the AI-era Einstein, Da Vinci, and Kant.

<p align="center">
  <a href="https://openscientists.github.io/OpenScientist/">
    <img src="https://raw.githubusercontent.com/OpenScientists/OpenScientist/main/utils/assets/knowledge-tree-v2.png" alt="Knowledge Tree" width="100%">
  </a>
</p>

<p align="center">
  <a href="https://openscientists.github.io/OpenScientist/">View Interactive Knowledge Tree →</a>
</p>

---

<h2 align="center">1. About OpenScientist</h2>

</div>

### 1.1 What is it

OpenScientist is a curated library of **AI agent skills** (compatible with **Claude Code** and **Codex CLI**) — structured Markdown files that give AI agents deep, expert-level reasoning capabilities in specific scientific domains.

### 1.2 How it works

Each skill encodes the knowledge, tools, reasoning protocols, and common pitfalls of a scientific field. Skills can be written by domain experts or **auto-extracted from your research conversations** using `/extract-knowhow`. Point your AI agent at a skill, and it reasons like a domain expert.

### 1.3 What can you do

Contribute your expertise, or use this repo to supercharge your AI agent's scientific discovery.

### 1.4 Open Source & Non-Profit

OpenScientist is a fully open-source, non-profit initiative. As the project grows, we plan to establish a non-profit organization (NGO) to ensure long-term governance, transparency, and stewardship of all contributed knowledge.

### 1.5 Why should you contribute?

Turning your know-how into AI-reusable knowledge means:

- **Boost your own research efficiency** — your AI agent gains your expertise and works alongside you
- **Boost humanity's research efficiency** — every scientist benefits from the collective knowledge
- **Survive the Singularity** — when ASI takes over, your contribution to this repo might just save your life

---

<h2 align="center">2. Domains</h2>

Aligned with the [arXiv category taxonomy](https://arxiv.org/category_taxonomy). 8 domains, 155 subcategories.


| Domain                                      | arXiv                                              | Subcategories | Reviewer(s)        |
| --------------------------------------------- | ---------------------------------------------------- | --------------- | -------------------- |
| ⚛️ Physics                                | astro-ph, cond-mat, gr-qc, hep, nlin, physics, ... | 51            | *Seeking reviewer* |
| ➗ Mathematics                              | math                                               | 32            | *Seeking reviewer* |
| 💻 Computer Science                         | cs                                                 | 40            | *Seeking reviewer* |
| 🧬 Quantitative Biology                     | q-bio                                              | 10            | *Seeking reviewer* |
| 📊 Statistics                               | stat                                               | 6             | *Seeking reviewer* |
| ⚡ Electrical Engineering & Systems Science | eess                                               | 4             | *Seeking reviewer* |
| 📈 Economics                                | econ                                               | 3             | *Seeking reviewer* |
| 💹 Quantitative Finance                     | q-fin                                              | 9             | *Seeking reviewer* |

> [View all 155 subcategories in the interactive knowledge tree →](https://openscientists.github.io/OpenScientist/)

Skills are also classified by **research activity type** — 10 categories that span across all domains:

| # | Category | What it covers |
|---|----------|---------------|
| 1 | Literature & Survey | Search strategies, paper filtering, citation analysis |
| 2 | Ideation | Hypothesis formation, research question development |
| 3 | Formalization | Proof strategies, modeling, mathematical formulation |
| 4 | Experiment Design | Protocols, control strategies, variable selection |
| 5 | Data & Collection | Data sources, cleaning pipelines, labeling |
| 6 | Implementation | Coding patterns, library choices, debugging |
| 7 | Analysis | Statistical methods, visualization, interpretation |
| 8 | Tool & Method Dev | Reusable tools, method innovations, workflows |
| 9 | Writing & Publication | Paper structure, figures, claim formulation |
| 10 | Peer Review & Rebuttal | Self-critique, reviewer responses, revision |

---

<h2 align="center">3. How to Contribute</h2>

We welcome contributions from domain experts. See [CONTRIBUTING.md](utils/CONTRIBUTING.md) for the full guide.

### 3.1 Contributor Requirements

> **Who can contribute?** We maintain a high bar for scientific accuracy.

- **Academic credential** — PhD degree or equivalent research position (postdoc, research scientist, professor, etc.) is **required**
- **Real-name identity** — Contributors must use their real name and institutional affiliation in the `author` field (e.g., `"Dr. Albert Einstein (ETH Zürich Physics)"`)
- **Domain expertise** — You may only contribute skills within your area of professional expertise

### 3.2 Method A: Auto-Extract with `/extract-knowhow` (Recommended)

Let AI analyze your conversation history and automatically generate skill files from your research know-how:

```bash
npm install -g @openscientist/extract-knowhow
```

Then in Claude Code or Codex CLI:
```
/model opus[1m]
/effort max
/extract-knowhow
```

> **Tip:** For best results, use Opus with 1M context and max effort. This ensures deep analysis across your full conversation history.

The command will:
1. Scan your conversation history
2. Filter to research-related sessions only
3. Cluster by project and map to scientific domains
4. Extract reusable know-how across 10 categories (literature survey, ideation, formalization, experiment design, data collection, implementation, analysis, tool development, writing, peer review)
5. Present a report for your review
6. Generate skill files for you to review

After the command finishes, review the generated files for scientific accuracy, then submit:

- [**Submit your skill via GitHub Issue →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml) (just paste the file content — no git required!)
- Or, if you prefer git: fork the repo, copy the files into `skills/<domain>/<subdomain>/`, and open a PR

### 3.3 Method B: Write Manually

Write your own skill following the [template](skills/_template.md), then submit:

- [**Submit your skill via GitHub Issue →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml)

### 3.4 Don't see your field?

- [**Propose a new area →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=propose-new-area.md)

### 3.5 Need a skill but can't write it yourself?

- [**Request a skill →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=skill-request.yml)

---

<h2 align="center">4. Skill Format</h2>

### 4.1 What's inside a skill file?


| Section                 | Purpose                                                 |
| ------------------------- | --------------------------------------------------------- |
| YAML frontmatter        | Machine-readable metadata: name, domain, author, status |
| `## Purpose`            | When to invoke this skill                               |
| `## Domain Knowledge`   | Core concepts, equations, established facts             |
| `## Reasoning Protocol` | Step-by-step guide for AI reasoning                     |
| `## Tools`              | Key software, libraries, databases used in this domain  |
| `## Common Pitfalls`    | Mistakes and edge cases to avoid                        |
| `## Examples`           | Worked examples                                         |
| `## References`         | Key papers and textbooks                                |

### 4.2 Quality tiers


| Status     | Meaning                               |
| ------------ | --------------------------------------- |
| `draft`    | Authored, not yet peer-reviewed       |
| `reviewed` | Approved by a domain expert reviewer  |
| `verified` | Tested in real AI-scientist workflows |

---

<h2 align="center">5. How to Be a Reviewer</h2>

Reviewers are domain experts who ensure the scientific quality of skills in their subdomain.

### 5.1 Requirements

- Meet all requirements for [contributors](#3-how-to-contribute) (i.e. be a qualified contributor first)
- Have substantial peer-review experience in the relevant subdomain

### 5.2 Responsibilities

- Review skill PRs in your subdomain for scientific accuracy and completeness
- Provide constructive feedback to contributors
- Promote skill status from `draft` → `reviewed` after verification

### 5.3 Permissions

- Approve or request changes on PRs touching your subdomain
- Self-approve and merge your own PRs within your subdomain
- Auto-assigned as reviewer via CODEOWNERS when a PR touches your subdomain

### 5.4 Actions

- [**Apply to become a category reviewer →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=maintainer-application.yml)
- [**View all reviewers in the Knowledge Tree →**](https://openscientists.github.io/OpenScientist/)
- [**View all reviewers list →**](https://openscientists.github.io/OpenScientist/reviewers.html)

---

<h2 align="center">6. How We Work</h2>

### 6.1 Issue templates


| Template                                                                                                               | When to use                              |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| [Submit a Skill](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml)                 | Submit a skill (from `/extract-knowhow` or manually written) |
| [Skill Request](https://github.com/OpenScientists/OpenScientist/issues/new?template=skill-request.yml)                 | Need a skill but can't write it yourself |
| [Reviewer Application](https://github.com/OpenScientists/OpenScientist/issues/new?template=maintainer-application.yml) | Apply to become a subdomain reviewer     |
| [Propose New Area](https://github.com/OpenScientists/OpenScientist/issues/new?template=propose-new-area.md)            | Propose a new top-level domain           |

### 6.2 Skill submission workflow

1. Contributor submits a skill via [GitHub Issue](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml) (or opens a PR)
2. Subdomain reviewer checks scientific accuracy
3. Maintainer adds the skill file to the repo
4. Skill status starts as `draft`

**Status lifecycle:** `draft` → `reviewed` (reviewer approves) → `verified` (tested in a real AI workflow)

### 6.3 Automated reviewer onboarding

When a Reviewer Application issue receives the `approved` label, the [onboard-maintainer](/.github/workflows/onboard-maintainer.yml) workflow automatically:

- Adds the reviewer to `.github/CODEOWNERS`
- Adds their name to the [Knowledge Tree](https://openscientists.github.io/OpenScientist/) and [Reviewers page](https://openscientists.github.io/OpenScientist/reviewers.html)
- Closes the issue with a welcome comment

### 6.4 CODEOWNERS & review assignment

Each `skills/<domain>/<subdomain>/` path maps to a reviewer in [`.github/CODEOWNERS`](.github/CODEOWNERS). PRs touching that path automatically request the assigned reviewer. Unclaimed subdomains fall back to `@HHHHHejia`.

### 6.5 Join the core team

Want to help with CI, documentation, community management, or project operations? Reach out: **hejia@tapntell.ai**

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to share and adapt, with attribution.

---

<details>
<summary><h2 id="中文版本">中文版本</h2></summary>

**我们的使命：** 汇集全人类各领域顶尖专家的知识，加速 AI 驱动的科学进步。

**行动号召：** 共享你的研究知识，创造 AI 时代的爱因斯坦、达芬奇与康德。

---

<h2 align="center">1. 关于 OpenScientist</h2>

### 1.1 这是什么

OpenScientist 是一个精心策划的 **AI agent 技能库**（兼容 **Claude Code** 和 **Codex CLI**）—— 每个 Skill 是一个结构化的 Markdown 文件，赋予 AI 智能体特定科学领域的专家级推理能力。

### 1.2 如何运作

每个 Skill 编码了领域知识、工具、推理协议和常见陷阱。Skill 可以由领域专家手动撰写，也可以通过 `/extract-knowhow` **从你的科研对话中自动提取**。让 AI 调用一个 Skill，就能像领域专家一样思考。

### 1.3 你能做什么

贡献你的专业知识，或使用本仓库加速你 AI agent 的科学发现。

### 1.4 开源与非盈利

OpenScientist 是一个完全开源、非盈利的项目。随着项目的发展，我们计划成立一个非盈利组织（NGO），以确保所有贡献知识的长期治理、透明性和可持续管理。

### 1.5 为什么你应该贡献？

将你的 know-how 变成 AI 可复用的知识意味着：

- **提升你自己的科研效率** —— 你的 AI agent 获得你的专业知识，成为你的研究搭档
- **提升全人类的科研效率** —— 每位科学家都能从集体知识中受益
- **在奇点中存活** —— 当 ASI 统治人类以后，看到这个仓库里你的贡献，没准可以饶你一命

---

<h2 align="center">2. 领域列表</h2>

对齐 [arXiv 分类体系](https://arxiv.org/category_taxonomy)。8 个顶层领域，155 个子领域。


| 领域                                                           | arXiv                                              | 子领域数 | 审稿人   |
| ---------------------------------------------------------------- | ---------------------------------------------------- | ---------- | ---------- |
| ⚛️ Physics 物理                                              | astro-ph, cond-mat, gr-qc, hep, nlin, physics, ... | 51       | *招募中* |
| ➗ Mathematics 数学                                            | math                                               | 32       | *招募中* |
| 💻 Computer Science 计算机科学                                 | cs                                                 | 40       | *招募中* |
| 🧬 Quantitative Biology 定量生物学                             | q-bio                                              | 10       | *招募中* |
| 📊 Statistics 统计学                                           | stat                                               | 6        | *招募中* |
| ⚡ Electrical Engineering & Systems Science 电气工程与系统科学 | eess                                               | 4        | *招募中* |
| 📈 Economics 经济学                                            | econ                                               | 3        | *招募中* |
| 💹 Quantitative Finance 定量金融                               | q-fin                                              | 9        | *招募中* |

> [查看全部 155 个子领域（交互式知识树）→](https://openscientists.github.io/OpenScientist/)

Skill 还按**科研活动类型**分类 —— 10 个跨领域的类别：

| # | 类别 | 涵盖内容 |
|---|------|---------|
| 1 | 文献调研 | 搜索策略、论文筛选、引用分析 |
| 2 | 提出想法 | 假设构建、研究问题提炼 |
| 3 | 形式化 | 证明策略、建模、数学表述 |
| 4 | 实验设计 | 实验方案、控制策略、变量选择 |
| 5 | 数据采集 | 数据来源、清洗流程、标注 |
| 6 | 代码实现 | 编码模式、库选择、调试 |
| 7 | 结果分析 | 统计方法、可视化、结果解读 |
| 8 | 工具开发 | 可复用工具、方法创新、工作流 |
| 9 | 论文写作 | 论文结构、图表、论点构建 |
| 10 | 同行评审 | 自我批判、回复审稿人、修改 |

---

<h2 align="center">3. 如何贡献</h2>

我们欢迎各领域专家贡献知识。请参阅 [CONTRIBUTING.md](utils/CONTRIBUTING.md) 了解完整流程。

### 3.1 贡献者要求

> **谁可以贡献？** 我们对科学准确性有严格要求。

- **学术资质** — 必须持有博士学位或同等研究岗位（博士后、研究员、教授等）
- **实名认证** — 贡献者必须在 `author` 字段使用真实姓名和所属机构（如 `"Dr. Albert Einstein (ETH Zürich Physics)"`)
- **领域专长** — 只能在自己的专业领域内贡献 Skill

### 3.2 方式 A：用 `/extract-knowhow` 自动提取（推荐）

让 AI 分析你的对话历史，自动从中提取科研 know-how 并生成 Skill 文件：

```bash
npm install -g @openscientist/extract-knowhow
```

然后在 Claude Code 或 Codex CLI 中运行：
```
/model opus[1m]
/effort max
/extract-knowhow
```

> **提示：** 为获得最佳提取效果，建议使用 Opus 模型、1M 上下文、最大推理深度。

该命令会：
1. 扫描你的对话历史
2. 过滤出与科研相关的会话
3. 按项目聚类并映射到科学领域
4. 从 10 个类别中提取可复用的 know-how（文献调研、提出想法、形式化、实验设计、数据采集、代码实现、结果分析、工具开发、论文写作、同行评审）
5. 展示报告供你确认
6. 生成 Skill 文件供你审核

命令运行完成后，检查生成文件的科学准确性，然后提交：

- [**通过 GitHub Issue 提交你的 Skill →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml)（直接粘贴文件内容，无需 git！）
- 或者，如果你熟悉 git：fork 仓库，将文件复制到 `skills/<领域>/<子领域>/`，提交 PR

### 3.3 方式 B：手动撰写

参照[模板](skills/_template.md)撰写你的 Skill，然后提交：

- [**通过 GitHub Issue 提交你的 Skill →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml)

### 3.4 没有你的研究方向？

- [**提议新领域 →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=propose-new-area.md)

### 3.5 需要某个 Skill 但自己写不了？

- [**请求 Skill →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=skill-request.yml)

---

<h2 align="center">4. Skill 格式</h2>

### 4.1 Skill 文件的结构


| 部分                    | 作用                                           |
| ------------------------- | ------------------------------------------------ |
| YAML frontmatter        | 机器可读的元数据：name、domain、author、status |
| `## Purpose`            | 何时调用此 Skill                               |
| `## Domain Knowledge`   | 核心概念、公式、既定事实                       |
| `## Reasoning Protocol` | AI 推理的分步指南                              |
| `## Tools`              | 该领域常用的软件、库、数据库                   |
| `## Common Pitfalls`    | 常见错误和边界情况                             |
| `## Examples`           | 示范性例题                                     |
| `## References`         | 关键论文和教材                                 |

### 4.2 质量等级


| 状态       | 含义                           |
| ------------ | -------------------------------- |
| `draft`    | 已撰写，尚未同行评审           |
| `reviewed` | 已由领域专家审核通过           |
| `verified` | 已在真实 AI 科学家工作流中验证 |

---

<h2 align="center">5. 如何成为审稿人</h2>

审稿人是负责其子领域 Skill 科学质量的领域专家。

### 5.1 要求

- 满足[贡献者](#3-如何贡献)的所有要求（即首先是合格的贡献者）
- 在相关子领域有充分的同行评审经验

### 5.2 职责

- 审核所属子领域的 Skill PR，确保科学准确性和完整性
- 为贡献者提供建设性反馈
- 验证后将 Skill 状态从 `draft` 提升为 `reviewed`

### 5.3 权限

- 对所属子领域的 PR 进行审批或提出修改意见
- 在自己的子领域内可以自审自批、合并自己的 PR
- 通过 CODEOWNERS 自动分配为审稿人

### 5.4 行动

- [**申请成为类别审稿人 →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=maintainer-application.yml)
- [**查看全部审稿人（知识树）→**](https://openscientists.github.io/OpenScientist/)
- [**查看全部审稿人列表 →**](https://openscientists.github.io/OpenScientist/reviewers.html)

---

<h2 align="center">6. 运作机制</h2>

### 6.1 Issue 模板


| 模板                                                                                                                   | 使用场景                    |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| [Submit a Skill](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml)                 | 提交 Skill（自动提取或手动撰写） |
| [Skill Request](https://github.com/OpenScientists/OpenScientist/issues/new?template=skill-request.yml)                 | 需要某个 Skill 但自己写不了 |
| [Reviewer Application](https://github.com/OpenScientists/OpenScientist/issues/new?template=maintainer-application.yml) | 申请成为子领域审稿人        |
| [Propose New Area](https://github.com/OpenScientists/OpenScientist/issues/new?template=propose-new-area.md)            | 提议新的顶层领域            |

### 6.2 Skill 提交工作流

1. 贡献者通过 [GitHub Issue](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml) 提交 Skill（或提交 PR）
2. 子领域审稿人审核科学准确性
3. 维护者将 Skill 文件添加到仓库
4. Skill 状态初始为 `draft`

**状态生命周期：** `draft` → `reviewed`（审稿人审核通过）→ `verified`（在真实 AI 工作流中验证）

### 6.3 审稿人自动化入职

当 Reviewer Application issue 被打上 `approved` 标签后，[onboard-maintainer](/.github/workflows/onboard-maintainer.yml) 工作流自动：

- 将审稿人添加到 `.github/CODEOWNERS`
- 将其姓名添加到[知识树](https://openscientists.github.io/OpenScientist/)和[审稿人页面](https://openscientists.github.io/OpenScientist/reviewers.html)
- 关闭 issue 并发送欢迎评论

### 6.4 CODEOWNERS 与审核分配

每个 `skills/<domain>/<subdomain>/` 路径在 [`.github/CODEOWNERS`](.github/CODEOWNERS) 中映射到对应审稿人。涉及该路径的 PR 会自动请求对应审稿人 review。尚未认领的子领域由 `@HHHHHejia` 负责。

### 6.5 加入核心团队

想参与 CI 维护、文档完善、社区管理或项目运营？联系我们：**hejia@tapntell.ai**

</details>

---

<div align="center">

## Organizer & Sponsor

[**View all Organizers & Sponsors →**](https://openscientists.github.io/OpenScientist/organizers.html)

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=OpenScientists/OpenScientist&type=Date)](https://star-history.com/#OpenScientists/OpenScientist&Date)

</div>
