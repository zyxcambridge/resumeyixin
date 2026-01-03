# 项目理解文档：NVIDIA岗位申请助手

## 📋 项目概述

这是一个**自动化简历定制工具**，帮助求职者针对NVIDIA的AI相关岗位生成定制化简历。

### 核心功能
1. **岗位搜索** - 搜索NVIDIA AI Agent相关岗位（上海）
2. **岗位解析** - 自动解析岗位描述和要求，提取关键词
3. **简历定制** - 根据岗位要求生成定制化简历
4. **申请指导** - 生成详细的申请步骤指导

---

## 🏗️ 架构图（Architecture Diagram）

展示主要模块、组件之间的关系和依赖。

```mermaid
flowchart TB
    subgraph INPUT["📥 输入层"]
        RESUME["resume.tex<br/>基础简历"]
        JOBURL["岗位URL<br/>NVIDIA Workday"]
    end

    subgraph CORE["⚙️ 核心处理层"]
        subgraph AGENT["NVIDIAJobAgent"]
            SEARCH["search_jobs()<br/>岗位搜索"]
            PARSE["parse_job_description()<br/>岗位解析"]
            EXTRACT["extract_keywords()<br/>关键词提取"]
            MATCH["match_resume_sections()<br/>简历匹配"]
            GENERATE["generate_customized_resume()<br/>生成定制简历"]
            GUIDE["create_application_guide()<br/>创建申请指导"]
        end

        subgraph CUSTOMIZER["ResumeCustomizer"]
            LOAD["load_resume()<br/>加载简历"]
            JOB_KW["extract_job_keywords()<br/>提取岗位关键词"]
            CUSTOM_SEC["customize_section()<br/>定制化章节"]
            GEN_CUSTOM["generate_customized_resume()<br/>生成定制简历"]
        end
    end

    subgraph OUTPUT["📤 输出层"]
        TEX["定制化简历.tex"]
        PDF["定制化简历.pdf"]
        JSON["关键词.json"]
        MD["申请指导.md"]
    end

    subgraph EXTERNAL["🌐 外部依赖"]
        WORKDAY["NVIDIA Workday<br/>招聘网站"]
        XELATEX["XeLaTeX<br/>PDF编译"]
    end

    RESUME --> LOAD
    JOBURL --> PARSE
    PARSE --> EXTRACT
    EXTRACT --> JOB_KW
    LOAD --> CUSTOM_SEC
    JOB_KW --> CUSTOM_SEC
    CUSTOM_SEC --> GEN_CUSTOM
    GEN_CUSTOM --> TEX
    TEX --> XELATEX
    XELATEX --> PDF
    GEN_CUSTOM --> JSON
    GENERATE --> GUIDE
    GUIDE --> MD

    WORKDAY -.->|"HTTP请求"| PARSE

    style INPUT fill:#e1f5fe,stroke:#01579b,color:#000
    style CORE fill:#fff3e0,stroke:#e65100,color:#000
    style OUTPUT fill:#e8f5e9,stroke:#1b5e20,color:#000
    style EXTERNAL fill:#fce4ec,stroke:#880e4f,color:#000
```

**说明**：系统分为输入层（基础简历+岗位URL）、核心处理层（两个主要类）、输出层（定制化文件）和外部依赖（招聘网站+编译器）。

---

## 📞 API调用图（API Call Graph）

展示核心API函数之间的调用顺序和依赖路径。

```mermaid
flowchart LR
    subgraph MAIN["main() 主函数"]
        M1["创建 NVIDIAJobAgent"]
        M2["遍历 job_urls"]
    end

    subgraph AGENT_FLOW["NVIDIAJobAgent 调用流程"]
        A1["parse_job_description(job_url)"]
        A2["extract_keywords(job_desc)"]
        A3["generate_customized_resume(job_info, output)"]
        A4["create_application_guide(job_info, resume)"]
    end

    subgraph CUSTOMIZER_FLOW["ResumeCustomizer 调用流程"]
        C1["load_resume()"]
        C2["extract_job_keywords(job_desc)"]
        C3["customize_section(section, keywords)"]
        C4["generate_customized_resume(job_info, output)"]
    end

    subgraph EXTERNAL_CALLS["外部调用"]
        E1["requests.get(job_url)"]
        E2["BeautifulSoup(html)"]
        E3["subprocess.run(xelatex)"]
    end

    M1 --> M2
    M2 --> A1
    A1 --> E1
    E1 --> E2
    A1 --> A2
    A2 --> A3
    A3 --> E3
    A3 --> A4

    C1 --> C2
    C2 --> C3
    C3 --> C4

    style MAIN fill:#e3f2fd,stroke:#1565c0,color:#000
    style AGENT_FLOW fill:#fff8e1,stroke:#f57f17,color:#000
    style CUSTOMIZER_FLOW fill:#f3e5f5,stroke:#7b1fa2,color:#000
    style EXTERNAL_CALLS fill:#ffebee,stroke:#c62828,color:#000
```

**说明**：主函数创建Agent实例后，依次调用岗位解析→关键词提取→简历生成→指导文档的流程，外部调用包括HTTP请求和LaTeX编译。

---

## 🔄 数据流向图（Data Flow Diagram）

展示数据从输入、处理、存储到输出的流转路径。

```mermaid
flowchart TB
    subgraph INPUT_DATA["📥 输入数据"]
        D1["resume.tex<br/>LaTeX简历源文件"]
        D2["job_urls[]<br/>岗位URL列表"]
    end

    subgraph PROCESS["🔄 数据处理流程"]
        P1["HTTP请求获取HTML"]
        P2["BeautifulSoup解析HTML"]
        P3["正则匹配提取关键词"]
        P4["生成岗位信息Dict"]
        P5["读取简历内容String"]
        P6["添加定制化注释头"]
        P7["合并生成定制简历"]
    end

    subgraph DATA_STRUCT["📊 核心数据结构"]
        S1["job_info: Dict<br/>title, url, description<br/>requirements, location"]
        S2["keywords: Dict<br/>technologies[]<br/>skills[]<br/>domains[]"]
        S3["resume_content: String<br/>LaTeX源码"]
    end

    subgraph OUTPUT_DATA["📤 输出数据"]
        O1["resume_nvidia_*.tex<br/>定制化LaTeX文件"]
        O2["*_keywords.json<br/>关键词JSON文件"]
        O3["resume_nvidia_*.pdf<br/>PDF简历"]
        O4["application_guide_*.md<br/>申请指导"]
    end

    D2 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> S2
    P2 --> P4
    P4 --> S1
    D1 --> P5
    P5 --> S3
    S1 --> P6
    S2 --> P6
    S3 --> P6
    P6 --> P7
    P7 --> O1
    S1 --> O2
    S2 --> O2
    O1 -->|"xelatex编译"| O3
    S1 --> O4

    style INPUT_DATA fill:#e8eaf6,stroke:#3f51b5,color:#000
    style PROCESS fill:#fffde7,stroke:#fbc02d,color:#000
    style DATA_STRUCT fill:#e0f7fa,stroke:#00838f,color:#000
    style OUTPUT_DATA fill:#e8f5e9,stroke:#2e7d32,color:#000
```

**说明**：数据从URL和简历文件输入，经过解析、提取、合并处理，最终生成定制化的tex/pdf/json/md四种输出文件。

---

## 🧠 核心算法详解

### 关键词提取算法

```mermaid
flowchart TB
    subgraph INPUT["输入"]
        JD["岗位描述文本<br/>job_description"]
    end

    subgraph PATTERNS["正则模式匹配"]
        TECH["技术栈模式<br/>PyTorch|TensorFlow|CUDA|LLM..."]
        DOMAIN["领域模式<br/>Autonomous|Robotics|Healthcare..."]
        SKILL["技能模式<br/>Deep Learning|ML|RL..."]
    end

    subgraph PROCESS["处理流程"]
        P1["re.findall(pattern, text)"]
        P2["去重 set()"]
        P3["分类整理"]
    end

    subgraph OUTPUT["输出"]
        RESULT["keywords: Dict<br/>technologies: [...]<br/>domains: [...]<br/>skills: [...]"]
    end

    JD --> TECH
    JD --> DOMAIN
    JD --> SKILL
    TECH --> P1
    DOMAIN --> P1
    SKILL --> P1
    P1 --> P2
    P2 --> P3
    P3 --> RESULT

    style INPUT fill:#e3f2fd,stroke:#1565c0,color:#000
    style PATTERNS fill:#fff3e0,stroke:#ef6c00,color:#000
    style PROCESS fill:#f3e5f5,stroke:#7b1fa2,color:#000
    style OUTPUT fill:#e8f5e9,stroke:#2e7d32,color:#000
```

**算法说明**：
1. 预定义技术栈、领域、技能三类正则模式
2. 对岗位描述进行多模式匹配
3. 去重并分类整理为字典结构
4. 用于后续简历定制化和匹配度评估

---

## 📁 文件结构

```
/workspace/
├── 📄 核心脚本
│   ├── job_application_agent.py    # 主Agent脚本（NVIDIAJobAgent类）
│   └── customize_resume.py          # 简历定制工具（ResumeCustomizer类）
│
├── 📝 简历文件
│   ├── resume.tex                   # 基础中文简历（LaTeX源码）
│   ├── resume.pdf                   # 基础简历PDF
│   ├── resume_en.tex                # 英文简历
│   └── resume_en.pdf                # 英文简历PDF
│
├── 🎯 定制化输出
│   ├── resume_nvidia_Senior_Software_Engineer_-_Multi-Agent_S.tex
│   ├── resume_nvidia_Senior_Software_Engineer_-_Multi-Agent_S.pdf
│   ├── resume_nvidia_Senior_Software_Engineer_-_Multi-Agent_S_keywords.json
│   ├── resume_nvidia_Developer_Technology_Engineer_-_AI.tex
│   ├── resume_nvidia_Developer_Technology_Engineer_-_AI.pdf
│   └── resume_nvidia_Developer_Technology_Engineer_-_AI_keywords.json
│
├── 📚 文档
│   ├── README_JOB_AGENT.md          # 项目说明文档
│   └── QUICK_START.md               # 快速开始指南
│
└── 🔧 配置
    └── requirements.txt             # Python依赖
```

---

## 👤 简历主人信息

### 张益新 (Yixin Zhang)

| 项目 | 信息 |
|------|------|
| **职位** | 算法工程师 |
| **邮箱** | zyxcambridge@gmail.com |
| **电话** | 17521398109 |
| **位置** | 上海 |
| **教育** | 北华航天工业学院 网络工程学士 (2010-2014) |

### 核心技术栈
- **深度学习框架**: PyTorch, TensorFlow, ONNX
- **GPU计算**: CUDA, TensorRT, TensorRT-LLM
- **部署平台**: NVIDIA Orin/Thor/Jetson, 地平线J5/J6, FPGA
- **AI Agent**: Multi-Agent系统, LLM, Transformer
- **自动驾驶**: BEV感知, 端到端部署, V2X

### 重要成就
1. 🏆 **NeurIPS 2025** CureBench国际智能体评测竞赛 **全球第二名**
2. 📄 论文发表: CureAgent (arXiv:2512.05576)
3. 📚 著作: 《自进化智能体–动态记忆与持续运行的架构实践》
4. 🎖️ Google机器学习开发专家 (连续5年)
5. 💰 商业成果: 量产MEC设备100+台, 创收500万+

---

## 🎯 当前目标岗位

### 1. Senior Software Engineer - Multi-Agent System - AV Infrastructure
- **匹配关键词**: Multi-Agent, AI Agent, PyTorch, CUDA, LLM, Distributed Systems, Autonomous Vehicle
- **定制简历**: `resume_nvidia_Senior_Software_Engineer_-_Multi-Agent_S.pdf`

### 2. Developer Technology Engineer - AI
- **匹配关键词**: Deep Learning, Machine Learning, GPU, CUDA, LLM, Transformer, Python
- **定制简历**: `resume_nvidia_Developer_Technology_Engineer_-_AI.pdf`

---

## 📊 技术依赖

```
requests>=2.31.0      # HTTP请求
beautifulsoup4>=4.12.0 # HTML解析
lxml>=4.9.0           # XML/HTML解析器
xelatex               # LaTeX编译器（系统级）
```

---

## 🚀 使用流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant S as 脚本
    participant W as NVIDIA Workday
    participant L as XeLaTeX

    U->>S: 运行 python customize_resume.py
    S->>S: 加载 resume.tex
    S->>W: 获取岗位描述（可选）
    W-->>S: 返回HTML
    S->>S: 提取关键词
    S->>S: 生成定制化简历
    S->>L: 编译 .tex 文件
    L-->>S: 生成 .pdf
    S-->>U: 输出定制化简历+指导文档
```

---

**生成时间**: 2026-01-03

**文档版本**: v1.0
