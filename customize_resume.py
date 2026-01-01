#!/usr/bin/env python3
"""
简历定制化工具
根据岗位要求自动调整简历内容
"""

import re
import json
from pathlib import Path
from typing import Dict, List

class ResumeCustomizer:
    def __init__(self, base_resume_path: str = "resume.tex"):
        self.base_resume_path = base_resume_path
        self.resume_content = ""
        
    def load_resume(self):
        """加载基础简历"""
        with open(self.base_resume_path, 'r', encoding='utf-8') as f:
            self.resume_content = f.read()
        print(f"✅ 已加载简历: {self.base_resume_path}")
    
    def extract_job_keywords(self, job_description: str) -> Dict[str, List[str]]:
        """从岗位描述中提取关键词"""
        keywords = {
            'technologies': [],
            'skills': [],
            'domains': [],
            'requirements': []
        }
        
        # 技术栈关键词
        tech_patterns = [
            r'\b(PyTorch|TensorFlow|JAX|ONNX)\b',
            r'\b(CUDA|GPU|NVIDIA|TensorRT)\b',
            r'\b(LLM|Large Language Model|GPT|Transformer)\b',
            r'\b(AI Agent|Multi-Agent|Agent Framework)\b',
            r'\b(Reinforcement Learning|RL|RLHF)\b',
            r'\b(Computer Vision|CV|Object Detection)\b',
            r'\b(Autonomous Vehicle|AV|Self-Driving)\b',
            r'\b(Distributed Systems|Cloud Computing|Kubernetes)\b',
            r'\b(Python|C\+\+|Rust|Go)\b',
            r'\b(Deep Learning|Machine Learning|ML)\b'
        ]
        
        # 领域关键词
        domain_patterns = [
            r'\b(Clinical|Biomedical|Healthcare)\b',
            r'\b(Robotics|Embodied AI)\b',
            r'\b(Autonomous|Self-Driving|ADAS)\b',
            r'\b(Perception|Sensor Fusion)\b'
        ]
        
        desc_lower = job_description.lower()
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            keywords['technologies'].extend(matches)
        
        for pattern in domain_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            keywords['domains'].extend(matches)
        
        # 去重
        for key in keywords:
            keywords[key] = list(set(keywords[key]))
        
        return keywords
    
    def customize_section(self, section_name: str, job_keywords: Dict, 
                         emphasis_items: List[str] = None) -> str:
        """定制化简历特定部分"""
        # 这里可以根据岗位关键词调整简历内容
        # 实际实现需要解析LaTeX结构
        
        customization_notes = f"""
% 定制化说明 - {section_name}
% 匹配关键词: {', '.join(job_keywords.get('technologies', [])[:10])}
% 重点强调: {', '.join(emphasis_items or [])}
"""
        return customization_notes
    
    def generate_customized_resume(self, job_info: Dict, output_path: str):
        """生成定制化简历"""
        print(f"\n✏️  生成定制化简历...")
        print(f"   岗位: {job_info.get('title', 'N/A')}")
        
        # 提取关键词
        job_desc = ' '.join(job_info.get('requirements', [])) + ' ' + job_info.get('description', '')
        keywords = self.extract_job_keywords(job_desc)
        
        print(f"📌 提取关键词:")
        print(f"   技术栈: {', '.join(keywords['technologies'][:5])}")
        print(f"   领域: {', '.join(keywords['domains'][:3])}")
        
        # 生成定制化版本
        customized = self.resume_content
        
        # 添加定制化注释
        header_comment = f"""
% ============================================
% 定制化简历 - 针对岗位
% 职位: {job_info.get('title', 'NVIDIA Position')}
% URL: {job_info.get('url', '')}
% 生成时间: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}
% 
% 匹配关键词:
% - 技术栈: {', '.join(keywords['technologies'][:8])}
% - 领域: {', '.join(keywords['domains'][:5])}
% ============================================
"""
        customized = header_comment + customized
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(customized)
        
        print(f"✅ 已保存: {output_path}")
        
        # 保存关键词信息
        keywords_file = output_path.replace('.tex', '_keywords.json')
        with open(keywords_file, 'w', encoding='utf-8') as f:
            json.dump({
                'job_info': job_info,
                'keywords': keywords
            }, f, ensure_ascii=False, indent=2)
        
        return output_path


def process_nvidia_jobs():
    """处理NVIDIA岗位"""
    customizer = ResumeCustomizer()
    customizer.load_resume()
    
    # NVIDIA岗位列表
    nvidia_jobs = [
        {
            'title': 'Senior Software Engineer - Multi-Agent System - AV Infrastructure',
            'url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Senior-Software-Engineer--Multi-Agent-System---AV-Infrastructure_JR2010348',
            'description': '''
            We are looking for a Senior Software Engineer to work on Multi-Agent System for Autonomous Vehicle Infrastructure.
            Requirements:
            - Experience with AI Agent frameworks and multi-agent systems
            - Strong background in autonomous vehicle development
            - Proficiency in PyTorch, CUDA, and distributed systems
            - Experience with LLM and agent orchestration
            ''',
            'requirements': [
                'AI Agent frameworks',
                'Multi-agent systems',
                'Autonomous Vehicle',
                'PyTorch',
                'CUDA',
                'Distributed Systems',
                'LLM',
                'Agent orchestration'
            ]
        },
        {
            'title': 'Developer Technology Engineer - AI',
            'url': 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Developer-Technology-Engineer--AI_JR2000017',
            'description': '''
            Developer Technology Engineer focused on AI technologies.
            Requirements:
            - Deep learning and machine learning expertise
            - GPU computing and CUDA programming
            - Experience with LLM and transformer models
            - Strong Python and C++ skills
            ''',
            'requirements': [
                'Deep Learning',
                'Machine Learning',
                'GPU Computing',
                'CUDA',
                'LLM',
                'Transformer',
                'Python',
                'C++'
            ]
        }
    ]
    
    print("=" * 60)
    print("🚀 NVIDIA岗位简历定制化")
    print("=" * 60)
    
    for i, job in enumerate(nvidia_jobs, 1):
        print(f"\n处理岗位 {i}/{len(nvidia_jobs)}: {job['title']}")
        
        # 生成定制化简历
        safe_title = re.sub(r'[^\w\s-]', '', job['title'])[:40].replace(' ', '_')
        output_path = f"resume_nvidia_{safe_title}.tex"
        
        customizer.generate_customized_resume(job, output_path)
        
        print(f"✅ 岗位 {i} 处理完成")
    
    print("\n" + "=" * 60)
    print("🎉 所有岗位处理完成!")
    print("=" * 60)
    print("\n📌 下一步:")
    print("1. 检查生成的定制化简历")
    print("2. 编译PDF: xelatex resume_nvidia_*.tex")
    print("3. 访问岗位URL进行申请")
    print("4. 上传对应的定制化简历PDF")


if __name__ == "__main__":
    process_nvidia_jobs()
