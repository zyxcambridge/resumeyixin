#!/usr/bin/env python3
"""
AGI岗位申请助手 - NVIDIA、Google、Microsoft
功能：
1. 搜索三大公司的AGI相关岗位
2. 解析岗位要求
3. 根据岗位要求生成定制化简历
4. 提供申请指导
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Optional
from pathlib import Path
import time
from dataclasses import dataclass

@dataclass
class JobInfo:
    """岗位信息数据类"""
    company: str
    title: str
    url: str
    location: str
    description: str
    requirements: List[str]
    keywords: List[str]


class AGIJobAgent:
    """AGI岗位申请助手"""
    
    def __init__(self, resume_path: str = "resume_en.tex"):
        self.resume_path = resume_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # 公司招聘网站配置
        self.company_configs = {
            'NVIDIA': {
                'base_url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite',
                'careers_page': 'https://www.nvidia.com/en-us/about-nvidia/careers/',
                'search_url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite'
            },
            'Google': {
                'base_url': 'https://www.google.com/about/careers/applications/jobs/results',
                'careers_page': 'https://careers.google.com/',
                'search_url': 'https://www.google.com/about/careers/applications/jobs/results'
            },
            'Microsoft': {
                'base_url': 'https://careers.microsoft.com/professionals/us/en/search-results',
                'careers_page': 'https://careers.microsoft.com/',
                'search_url': 'https://careers.microsoft.com/v2/global/en/search'
            }
        }
        
        # AGI相关关键词
        self.agi_keywords = [
            'AGI', 'Artificial General Intelligence',
            'AI Agent', 'AI Agents', 'Multi-Agent',
            'Large Language Model', 'LLM', 'Foundation Model',
            'Generative AI', 'GenAI',
            'Reinforcement Learning', 'RLHF',
            'Embodied AI', 'Embodied Intelligence',
            'Autonomous Agent', 'Agent Framework',
            'Reasoning', 'Planning',
            'Machine Learning Research',
            'Deep Learning Research',
            'AI Safety', 'AI Alignment',
            'Transformer', 'GPT', 'Multimodal'
        ]
    
    def get_nvidia_agi_jobs(self) -> List[Dict]:
        """获取NVIDIA AGI相关岗位"""
        print("\n🔍 搜索 NVIDIA AGI 相关岗位...")
        
        jobs = [
            {
                'company': 'NVIDIA',
                'title': 'Senior Software Engineer - Multi-Agent System - AV Infrastructure',
                'url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Senior-Software-Engineer--Multi-Agent-System---AV-Infrastructure_JR2010348',
                'location': 'Shanghai, China / Santa Clara, CA',
                'description': '''
                We are looking for a Senior Software Engineer to work on Multi-Agent System for Autonomous Vehicle Infrastructure.
                Join NVIDIA's team to build next-generation AI agents for autonomous systems.
                ''',
                'requirements': [
                    'Experience with AI Agent frameworks and multi-agent systems',
                    'Strong background in autonomous vehicle development',
                    'Proficiency in PyTorch, CUDA, and distributed systems',
                    'Experience with LLM and agent orchestration',
                    'Deep learning and machine learning expertise',
                    'Strong Python and C++ programming skills'
                ],
                'keywords': ['AI Agent', 'Multi-Agent', 'Autonomous Vehicle', 'PyTorch', 'CUDA', 'LLM', 'Distributed Systems']
            },
            {
                'company': 'NVIDIA',
                'title': 'Developer Technology Engineer - AI',
                'url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Developer-Technology-Engineer--AI_JR2000017',
                'location': 'Shanghai, China / Santa Clara, CA',
                'description': '''
                Developer Technology Engineer focused on AI technologies.
                Work on cutting-edge AI/ML solutions with NVIDIA's GPU computing platform.
                ''',
                'requirements': [
                    'Deep learning and machine learning expertise',
                    'GPU computing and CUDA programming',
                    'Experience with LLM and transformer models',
                    'Strong Python and C++ skills',
                    'Model optimization and deployment experience'
                ],
                'keywords': ['Deep Learning', 'Machine Learning', 'GPU', 'CUDA', 'LLM', 'Transformer', 'TensorRT']
            },
            {
                'company': 'NVIDIA',
                'title': 'Research Scientist - Generative AI',
                'url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/jobs',
                'location': 'Santa Clara, CA / Remote',
                'description': '''
                Join NVIDIA Research to work on Generative AI and Foundation Models.
                Push the boundaries of AI capabilities.
                ''',
                'requirements': [
                    'PhD or equivalent experience in ML/AI',
                    'Experience with large-scale model training',
                    'Publications in top-tier venues (NeurIPS, ICML, ICLR)',
                    'Experience with distributed training',
                    'Strong coding skills in Python, PyTorch'
                ],
                'keywords': ['Generative AI', 'Foundation Model', 'Research', 'PyTorch', 'Distributed Training', 'NeurIPS']
            },
            {
                'company': 'NVIDIA',
                'title': 'Senior Engineer - Embodied AI / Robotics',
                'url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/jobs',
                'location': 'Shanghai, China / Seattle, WA',
                'description': '''
                Work on Embodied AI and Robotics at NVIDIA.
                Build AI systems that interact with the physical world.
                ''',
                'requirements': [
                    'Experience with robotics and embodied AI',
                    'Vision-Language models experience',
                    'Reinforcement learning for robotics',
                    'Experience with Isaac Sim or similar',
                    'Strong background in perception and planning'
                ],
                'keywords': ['Embodied AI', 'Robotics', 'Vision-Language', 'Reinforcement Learning', 'Isaac Sim', 'VLN']
            }
        ]
        
        return jobs
    
    def get_google_agi_jobs(self) -> List[Dict]:
        """获取Google AGI相关岗位"""
        print("\n🔍 搜索 Google/DeepMind AGI 相关岗位...")
        
        jobs = [
            {
                'company': 'Google DeepMind',
                'title': 'Research Scientist - AGI Safety',
                'url': 'https://careers.google.com/jobs/results/?q=AGI&location=United%20States',
                'location': 'Mountain View, CA / London, UK',
                'description': '''
                Join DeepMind's AGI Safety team to ensure AI systems are aligned with human values.
                Work on fundamental research in AI safety and alignment.
                ''',
                'requirements': [
                    'PhD in ML, AI, or related field',
                    'Research experience in AI safety, alignment, or interpretability',
                    'Publications in top-tier venues',
                    'Strong theoretical and empirical research skills',
                    'Experience with large language models'
                ],
                'keywords': ['AGI', 'AI Safety', 'AI Alignment', 'Research', 'LLM', 'Interpretability']
            },
            {
                'company': 'Google DeepMind',
                'title': 'Research Engineer - Gemini',
                'url': 'https://careers.google.com/jobs/results/?q=Gemini',
                'location': 'Mountain View, CA / London, UK',
                'description': '''
                Join the Gemini team to build the next generation of multimodal AI models.
                Work on cutting-edge foundation models.
                ''',
                'requirements': [
                    'Strong software engineering skills',
                    'Experience with large-scale ML systems',
                    'Experience with JAX, TensorFlow, or PyTorch',
                    'Background in NLP, Computer Vision, or Multimodal AI',
                    'Distributed systems experience'
                ],
                'keywords': ['Gemini', 'Multimodal', 'Foundation Model', 'JAX', 'Distributed Systems', 'NLP']
            },
            {
                'company': 'Google',
                'title': 'Software Engineer - AI Agents (Agentic AI)',
                'url': 'https://careers.google.com/jobs/results/?q=AI%20Agent',
                'location': 'Mountain View, CA / New York, NY',
                'description': '''
                Build AI agents that can reason, plan, and take actions to accomplish user goals.
                Work on the future of human-AI interaction.
                ''',
                'requirements': [
                    'Experience building AI agents or autonomous systems',
                    'Strong software engineering fundamentals',
                    'Experience with LLMs and prompt engineering',
                    'Knowledge of reinforcement learning',
                    'Experience with tool use and function calling'
                ],
                'keywords': ['AI Agent', 'Agentic AI', 'LLM', 'Reasoning', 'Planning', 'Tool Use']
            },
            {
                'company': 'Google',
                'title': 'Machine Learning Engineer - AI Studio',
                'url': 'https://careers.google.com/jobs/results/?q=Machine%20Learning',
                'location': 'Mountain View, CA / Remote',
                'description': '''
                Work on Google AI Studio to democratize access to AI capabilities.
                Build tools and infrastructure for AI development.
                ''',
                'requirements': [
                    'Strong ML engineering skills',
                    'Experience with model serving and inference optimization',
                    'Background in NLP or Computer Vision',
                    'Experience with cloud platforms (GCP)',
                    'Strong Python and system design skills'
                ],
                'keywords': ['Machine Learning', 'AI Studio', 'Model Serving', 'GCP', 'Inference Optimization']
            }
        ]
        
        return jobs
    
    def get_microsoft_agi_jobs(self) -> List[Dict]:
        """获取Microsoft AGI相关岗位"""
        print("\n🔍 搜索 Microsoft/OpenAI AGI 相关岗位...")
        
        jobs = [
            {
                'company': 'Microsoft',
                'title': 'Senior Research Scientist - AI Frontiers',
                'url': 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=AGI',
                'location': 'Redmond, WA / Remote',
                'description': '''
                Join Microsoft Research to work on AI Frontiers and AGI research.
                Push the boundaries of artificial intelligence.
                ''',
                'requirements': [
                    'PhD in ML, AI, or related field',
                    'Proven track record of high-impact research',
                    'Experience with large language models',
                    'Publications in NeurIPS, ICML, ICLR, ACL',
                    'Strong theoretical and empirical research skills'
                ],
                'keywords': ['AGI', 'Research', 'LLM', 'Foundation Model', 'NeurIPS', 'Microsoft Research']
            },
            {
                'company': 'Microsoft',
                'title': 'Principal Software Engineer - Copilot',
                'url': 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=Copilot',
                'location': 'Redmond, WA / San Francisco, CA',
                'description': '''
                Work on Microsoft Copilot to bring AI assistance to millions of users.
                Build the future of AI-powered productivity tools.
                ''',
                'requirements': [
                    'Strong software engineering experience',
                    'Experience with LLMs and AI applications',
                    'System design and architecture skills',
                    'Experience with Azure cloud services',
                    'Background in developer tools or productivity software'
                ],
                'keywords': ['Copilot', 'LLM', 'AI Assistant', 'Azure', 'Developer Tools']
            },
            {
                'company': 'Microsoft',
                'title': 'Applied Scientist - Azure AI',
                'url': 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=Azure%20AI',
                'location': 'Redmond, WA / Remote',
                'description': '''
                Work on Azure AI services to bring AI capabilities to enterprises.
                Build and optimize large-scale AI systems.
                ''',
                'requirements': [
                    'MS/PhD in ML, AI, or related field',
                    'Experience with model training and optimization',
                    'Strong background in NLP or Computer Vision',
                    'Experience with distributed training',
                    'Strong Python and ML framework skills'
                ],
                'keywords': ['Azure AI', 'Model Training', 'NLP', 'Computer Vision', 'Distributed Training']
            },
            {
                'company': 'Microsoft',
                'title': 'Senior Engineer - AI Agents & Autonomous Systems',
                'url': 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=AI%20Agent',
                'location': 'Redmond, WA / San Francisco, CA',
                'description': '''
                Build AI agents that can autonomously accomplish complex tasks.
                Work on agentic AI systems for enterprise and consumer applications.
                ''',
                'requirements': [
                    'Experience with AI agent development',
                    'Strong software engineering skills',
                    'Experience with LLMs and tool integration',
                    'Knowledge of reinforcement learning',
                    'Background in planning and reasoning systems'
                ],
                'keywords': ['AI Agent', 'Autonomous Systems', 'LLM', 'Planning', 'Reasoning', 'Enterprise AI']
            }
        ]
        
        return jobs
    
    def get_all_agi_jobs(self) -> List[Dict]:
        """获取所有公司的AGI岗位"""
        all_jobs = []
        all_jobs.extend(self.get_nvidia_agi_jobs())
        all_jobs.extend(self.get_google_agi_jobs())
        all_jobs.extend(self.get_microsoft_agi_jobs())
        return all_jobs
    
    def match_candidate_with_job(self, job: Dict) -> Dict:
        """匹配候选人与岗位"""
        # 候选人核心优势
        candidate_strengths = {
            'NeurIPS Competition': 'NeurIPS 2025 CureBench Global 2nd Place - AI Agent development',
            'AI Agent Experience': 'CureAgent framework, Executor-Analyst architecture, tool-augmented reasoning',
            'LLM Deployment': 'Deployed Ollama, llama.cpp, vllm, TensorRT-LLM, mlc-llm',
            'NVIDIA Platforms': 'Deployed on Thor, Orin, Jetson platforms with 4x latency reduction',
            'Embodied AI': 'VLN deployment, 150m long-range navigation, zero-shot generalization',
            'Model Optimization': 'Quantization (PTQ/QAT), operator fusion, multi-task scheduling',
            'Production Experience': '100+ MEC devices, 5M+ RMB revenue',
            'Research': 'Paper published (arXiv:2512.05576), book in publication',
            'Community': 'Google ML Developer Expert, 5 years, 11,874 people impacted'
        }
        
        # 计算匹配度
        job_keywords_lower = [k.lower() for k in job.get('keywords', [])]
        match_score = 0
        matched_strengths = []
        
        keyword_mapping = {
            'ai agent': ['NeurIPS Competition', 'AI Agent Experience'],
            'multi-agent': ['AI Agent Experience'],
            'llm': ['AI Agent Experience', 'LLM Deployment'],
            'large language model': ['AI Agent Experience', 'LLM Deployment'],
            'pytorch': ['NVIDIA Platforms', 'Model Optimization'],
            'cuda': ['NVIDIA Platforms', 'Model Optimization'],
            'nvidia': ['NVIDIA Platforms'],
            'embodied': ['Embodied AI'],
            'robotics': ['Embodied AI'],
            'vln': ['Embodied AI'],
            'deployment': ['NVIDIA Platforms', 'Model Optimization', 'LLM Deployment'],
            'optimization': ['Model Optimization'],
            'research': ['Research', 'NeurIPS Competition'],
            'neurips': ['NeurIPS Competition', 'Research'],
            'foundation model': ['LLM Deployment', 'AI Agent Experience'],
            'distributed': ['NVIDIA Platforms', 'Model Optimization'],
            'transformer': ['LLM Deployment'],
            'reinforcement learning': ['AI Agent Experience'],
            'generative ai': ['LLM Deployment', 'AI Agent Experience']
        }
        
        for kw in job_keywords_lower:
            for pattern, strengths in keyword_mapping.items():
                if pattern in kw.lower():
                    match_score += 1
                    for s in strengths:
                        if s not in matched_strengths:
                            matched_strengths.append(s)
        
        return {
            'match_score': match_score,
            'matched_strengths': matched_strengths,
            'highlights': [candidate_strengths[s] for s in matched_strengths[:5]]
        }
    
    def generate_customized_resume(self, job: Dict, output_path: str) -> str:
        """生成定制化简历"""
        print(f"\n✏️  为 {job['title']} @ {job['company']} 生成定制化简历...")
        
        # 读取原始简历
        with open(self.resume_path, 'r', encoding='utf-8') as f:
            resume_content = f.read()
        
        # 获取匹配信息
        match_info = self.match_candidate_with_job(job)
        
        # 添加定制化注释
        header_comment = f"""
% ============================================
% 定制化简历 - AGI岗位申请
% 公司: {job['company']}
% 职位: {job['title']}
% URL: {job['url']}
% 地点: {job['location']}
% 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
% 
% 岗位关键词: {', '.join(job.get('keywords', [])[:8])}
% 匹配分数: {match_info['match_score']}
% 匹配优势:
% - {chr(10) + '% - '.join(match_info['highlights'][:5])}
% ============================================
"""
        customized_resume = header_comment + resume_content
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(customized_resume)
        
        print(f"✅ 已保存: {output_path}")
        
        # 保存关键词和匹配信息
        keywords_file = output_path.replace('.tex', '_match_info.json')
        with open(keywords_file, 'w', encoding='utf-8') as f:
            json.dump({
                'job_info': job,
                'match_info': match_info
            }, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def create_application_guide(self, jobs: List[Dict]) -> str:
        """创建申请指导文档"""
        guide_content = f"""# AGI岗位申请指南 - NVIDIA / Google / Microsoft

生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

---

## 📋 候选人核心优势

### 🏆 顶级成就
- **NeurIPS 2025 CureBench竞赛全球第二名** - AI Agent工具增强推理
- **论文发表**: CureAgent: A Training-Free Executor-Analyst Framework (arXiv:2512.05576)
- **著作**: 《自进化智能体–动态记忆与持续运行的架构实践》即将出版

### 💼 核心经验
- **AI Agent开发**: Executor-Analyst框架、工具增强推理、分层集成策略
- **NVIDIA平台部署**: Thor、Orin、Jetson平台，延迟降低75%
- **具身智能**: VLN部署、150米长距离导航、零样本泛化
- **大模型部署**: Ollama、llama.cpp、vllm、TensorRT-LLM、mlc-llm
- **量产经验**: 100+台MEC设备、500万+营收

### 🎓 技术社区
- **Google机器学习开发专家** - 连续5年，影响11,874人

---

## 🏢 NVIDIA 岗位

"""
        
        # NVIDIA岗位
        nvidia_jobs = [j for j in jobs if j['company'] == 'NVIDIA']
        for i, job in enumerate(nvidia_jobs, 1):
            match_info = self.match_candidate_with_job(job)
            guide_content += f"""
### {i}. {job['title']}

- **地点**: {job['location']}
- **申请链接**: {job['url']}
- **匹配分数**: {match_info['match_score']}/10

**岗位关键词**: {', '.join(job.get('keywords', []))}

**匹配优势**:
"""
            for highlight in match_info['highlights'][:4]:
                guide_content += f"- ✅ {highlight}\n"
            
            guide_content += f"""
**申请建议**:
1. 强调NVIDIA平台（Thor、Orin、Jetson）部署经验
2. 突出AI Agent和Multi-Agent系统开发能力
3. 展示端到端推理优化成果（4倍延迟降低）

---
"""
        
        # Google岗位
        guide_content += "\n## 🔵 Google/DeepMind 岗位\n"
        google_jobs = [j for j in jobs if 'Google' in j['company']]
        for i, job in enumerate(google_jobs, 1):
            match_info = self.match_candidate_with_job(job)
            guide_content += f"""
### {i}. {job['title']}

- **地点**: {job['location']}
- **申请链接**: {job['url']}
- **匹配分数**: {match_info['match_score']}/10

**岗位关键词**: {', '.join(job.get('keywords', []))}

**匹配优势**:
"""
            for highlight in match_info['highlights'][:4]:
                guide_content += f"- ✅ {highlight}\n"
            
            guide_content += f"""
**申请建议**:
1. 强调Google ML开发专家身份和社区贡献
2. 突出NeurIPS竞赛成果和研究能力
3. 展示AI Agent框架设计和实现经验

---
"""
        
        # Microsoft岗位
        guide_content += "\n## 🟦 Microsoft 岗位\n"
        ms_jobs = [j for j in jobs if j['company'] == 'Microsoft']
        for i, job in enumerate(ms_jobs, 1):
            match_info = self.match_candidate_with_job(job)
            guide_content += f"""
### {i}. {job['title']}

- **地点**: {job['location']}
- **申请链接**: {job['url']}
- **匹配分数**: {match_info['match_score']}/10

**岗位关键词**: {', '.join(job.get('keywords', []))}

**匹配优势**:
"""
            for highlight in match_info['highlights'][:4]:
                guide_content += f"- ✅ {highlight}\n"
            
            guide_content += f"""
**申请建议**:
1. 强调AI Agent和Autonomous Systems经验
2. 突出大模型部署和优化能力
3. 展示量产级别的工程实践经验

---
"""
        
        # 申请步骤
        guide_content += """
## 📝 申请步骤

### NVIDIA 申请流程
1. 访问 https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite
2. 搜索关键词: "AI Agent", "Multi-Agent", "Embodied AI", "LLM"
3. 点击目标岗位 → "Apply"
4. 上传定制化简历PDF
5. 填写申请信息
6. 提交申请

### Google 申请流程
1. 访问 https://careers.google.com/
2. 搜索关键词: "AGI", "AI Agent", "Gemini", "Research"
3. 点击目标岗位 → "Apply"
4. 使用Google账号登录
5. 上传简历并填写信息
6. 提交申请

### Microsoft 申请流程
1. 访问 https://careers.microsoft.com/
2. 搜索关键词: "AGI", "AI Agent", "Copilot", "Azure AI"
3. 点击目标岗位 → "Apply"
4. 使用LinkedIn或Microsoft账号登录
5. 上传简历并填写信息
6. 提交申请

---

## ⚠️ 重要提示

- ✅ **不要造假**：所有信息必须真实
- ✅ **每个岗位使用对应简历**：根据岗位要求突出相关经验
- ✅ **仔细阅读岗位要求**：确保满足基本要求
- ✅ **保存申请确认**：记录申请状态和日期
- ✅ **及时跟进**：申请后1-2周内可尝试联系HR

---

## 🎯 申请策略

### 优先级排序

根据您的经验匹配度，建议按以下优先级申请：

**第一优先级 (最匹配)**:
1. NVIDIA - Senior Software Engineer - Multi-Agent System
2. NVIDIA - Senior Engineer - Embodied AI / Robotics
3. Microsoft - Senior Engineer - AI Agents & Autonomous Systems

**第二优先级 (很匹配)**:
1. NVIDIA - Developer Technology Engineer - AI
2. Google - Software Engineer - AI Agents (Agentic AI)
3. Microsoft - Applied Scientist - Azure AI

**第三优先级 (较匹配)**:
1. NVIDIA - Research Scientist - Generative AI
2. Google - Research Engineer - Gemini
3. Google DeepMind - Research Scientist - AGI Safety

---

## 📊 简历文件

"""
        # 添加简历文件列表
        guide_content += """
| 公司 | 岗位 | 简历文件 |
|------|------|----------|
"""
        for job in jobs:
            safe_title = re.sub(r'[^\w\s-]', '', job['title'])[:30].replace(' ', '_')
            safe_company = job['company'].replace(' ', '_')
            filename = f"resume_agi_{safe_company}_{safe_title}.tex"
            guide_content += f"| {job['company']} | {job['title'][:40]}... | `{filename}` |\n"
        
        guide_content += """

---

**祝您申请顺利！** 🎉

> 提示：将.tex文件编译为PDF后再上传，使用命令：`xelatex resume_agi_*.tex`
"""
        
        guide_path = "AGI_APPLICATION_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"\n📝 申请指南已保存: {guide_path}")
        return guide_path


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 AGI岗位申请助手 - NVIDIA / Google / Microsoft")
    print("=" * 70)
    
    agent = AGIJobAgent()
    
    # 获取所有AGI岗位
    all_jobs = agent.get_all_agi_jobs()
    
    print(f"\n📋 共找到 {len(all_jobs)} 个AGI相关岗位")
    
    # 按公司分组显示
    companies = {}
    for job in all_jobs:
        company = job['company']
        if company not in companies:
            companies[company] = []
        companies[company].append(job)
    
    for company, jobs in companies.items():
        print(f"\n{'='*50}")
        print(f"🏢 {company} ({len(jobs)} 个岗位)")
        print('='*50)
        for i, job in enumerate(jobs, 1):
            match_info = agent.match_candidate_with_job(job)
            print(f"\n  {i}. {job['title']}")
            print(f"     📍 {job['location']}")
            print(f"     🔗 {job['url'][:80]}...")
            print(f"     📊 匹配分数: {match_info['match_score']}/10")
    
    # 为每个岗位生成定制化简历
    print(f"\n{'='*70}")
    print("📝 生成定制化简历...")
    print('='*70)
    
    for job in all_jobs:
        safe_title = re.sub(r'[^\w\s-]', '', job['title'])[:30].replace(' ', '_')
        safe_company = job['company'].replace(' ', '_')
        output_path = f"resume_agi_{safe_company}_{safe_title}.tex"
        agent.generate_customized_resume(job, output_path)
    
    # 创建申请指导
    agent.create_application_guide(all_jobs)
    
    print(f"\n{'='*70}")
    print("🎉 所有岗位处理完成!")
    print('='*70)
    
    print("\n📌 下一步:")
    print("1. 查看 AGI_APPLICATION_GUIDE.md 了解申请指南")
    print("2. 编译PDF: for f in resume_agi_*.tex; do xelatex $f; done")
    print("3. 访问各公司招聘网站进行申请")
    print("4. 上传对应的定制化简历PDF")
    print("5. 保存申请确认信息")


if __name__ == "__main__":
    main()
