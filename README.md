# AI_Tool_Recommendation_System
# 🤖 场景化 AI 工具推荐助手 (AI-Tool-Recommender-Agent)
### 🌟 项目简介

在 AI 工具爆发式增长的背景下，用户常面临 **“看不懂技术参数”**、**“找不到可靠信源”** 以及 **“AI 虚构链接（幻觉）”** 的痛点。

本项目是一个基于 **LangChain** 和 **意图对齐算法** 开发的智能推荐 Agent。它不仅能理解用户的“大白话”需求，还能像行业专家一样，根据不同场景动态调整搜索策略，最终交付 **“精选工具表 + 原始证据溯源”** 的高信任度报告。

-----

### 🚀 核心功能亮点

  * **🧠 意图对齐与动态加权**：系统通过 LLM 预分析用户场景（如：办公、科研、开发），自动分配“榜单、评测、部署、体验”四维度的搜索权重，拒绝千篇一律的检索结果。
  * **🔍 定向配额检索**：接入 Tavily 搜索引擎，根据计算出的权重配额进行精准抓取，确保信源的多样性与专业性。
  * **🛡️ 防幻觉双层交付**：针对 LLM 易编造链接的痛点，采用“结论先行+证据溯源”模式。每一个推荐工具均需在原始网页中找到对应出处，彻底杜绝虚假链接。
  * **📊 结构化专家报告**：输出包含 Top 5 核心推荐表格及分维度的参考文献，满足用户从“快速决策”到“深度调研”的全方位需求。

-----

### 🛠️ 技术架构

1.  **意图识别层**：识别需求所属垂直领域。
2.  **战略规划层**：生成维度配额及针对性搜索词。
3.  **执行层**：多线程或定向配额检索。
4.  **精炼层**：上下文摘要提取与链接有效性对齐。
5.  **展示层**：Markdown 自动化渲染。

### 💻 运行样例展示
# 用户需求：
"想找一个能直接用来进行统计分析的工具，上传数据后就能自动分析，不想学习编程。"

# Agent 输出：
## 🏆 专家精选：Top 5 核心推荐
根据您的需求，系统已从海量信源中精选出以下 5 款**零编程门槛**的自动化统计工具：

| 工具名 | 核心优势 | 官网链接 |
| :--- | :--- | :--- |
| **Julius AI** | 🌟 **首选推荐**。支持自然语言对话，自动生成可视化报告 | [直达官网](https://julius.ai/) |
| **JMP** | 专为工程师设计，支持交互式点选建模，无需代码 | [直达官网](https://www.jmp.com/) |
| **IBM SPSS** | 行业标准工具，提供详尽的菜单式点击操作界面 | [直达官网](https://www.ibm.com/products/spss-statistics) |
| **SAS Viya** | 企业级 AI 预测平台，支持自动化的机器学习管道 | [直达官网](https://www.google.com/search?q=https://www.sas.com/en-us/software/viya.html) |
| **Minitab** | 极其易用的引导式统计软件，适合质量管理与教育 | `N/A` |

-----
## 📚 溯源参考文献 (Reference Report)
*本项目通过动态配额算法，为您整合了以下多维度信源，确保推荐的中立性与专业性。*

### 📊 【维度一：权威榜单】
> 侧重于行业覆盖度与工具知名度排名。
  * [2026 年度不可错过的 8 款统计分析软件精选](https://learn.g2.com/best-statistical-analysis-software)
  * [Julius AI：2026 年最佳统计工具对比报告](https://julius.ai/articles/statistical-analysis-tools)

### 🔍 【维度二：深度评测】
> 侧重于功能细节分析与专业系统对比。
  * [Top 5 核心统计系统深度对比综述](https://www.prostatservices.com/articles/a-review-of-the-top-five-statistical-software-systems)
  * [G2 深度报告：统计分析软件优劣势横评](https://learn.g2.com/best-statistical-analysis-software)

### 👤 【维度三：真实体验】
> 侧重于实际操作中的学习曲线与用户反馈。
  * [基于 2026 年用户反馈的 11 款 AI 统计工具定价与功能指南](https://julius.ai/articles/statistical-analysis-tools)


### 🛠️ 如何开始

1.  **克隆仓库**

    ```bash
    git clone https://github.com/你的用户名/仓库名.git
    cd 仓库名
    ```

2.  **安装依赖**

    ```bash
    pip install -r requirements.txt
    ```

3.  **配置环境**
    在根目录创建 `.env` 文件：

    ```text
    API_KEY=你的模型Key
    TAVILY_API_KEY=你的TavilyKey
    ```

4.  **运行程序**

    ```bash
    python main.py
    ```
