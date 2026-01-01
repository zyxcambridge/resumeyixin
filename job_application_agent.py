#!/usr/bin/env python3
"""
自动找工作Agent - NVIDIA岗位申请助手
功能：
1. 搜索NVIDIA岗位（AI Agent相关，上海）
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

class NVIDIAJobAgent:
    def __init__(self, resume_path: str = "resume.tex"):
        self.resume_path = resume_path
        self.base_url = "https://nvidia.wd5.myworkdayjobs.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def search_jobs(self, keywords: List[str] = ["AI Agent", "Multi-Agent"], 
                   location: str = "Shanghai, China", max_results: int = 20) -> List[Dict]:
        """
        搜索NVIDIA岗位
        """
        print(f"🔍 搜索NVIDIA岗位: {keywords}, 地点: {location}")
        
        jobs = []
        search_url = f"{self.base_url}/en-US/NVIDIAExternalCareerSite/jobs"
        
        # 这里需要实际的搜索逻辑
        # 由于Workday网站需要JavaScript，我们提供手动搜索指导
        print("\n📋 搜索指导：")
        print(f"1. 访问: {self.base_url}/en-US/NVIDIAExternalCareerSite")
        print(f"2. 搜索关键词: {' OR '.join(keywords)}")
        print(f"3. 筛选地点: {location}")
        print(f"4. 将找到的岗位URL保存到 jobs.json 文件中")
        
        return jobs
    
    def parse_job_description(self, job_url: str) -> Dict:
        """
        解析岗位描述和要求
        """
        print(f"\n📖 解析岗位描述: {job_url}")
        
        try:
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取岗位信息
            job_info = {
                'title': '',
                'location': '',
                'description': '',
                'requirements': [],
                'responsibilities': [],
                'url': job_url
            }
            
            # 尝试提取标题
            title_elem = soup.find('h1') or soup.find('title')
            if title_elem:
                job_info['title'] = title_elem.get_text(strip=True)
            
            # 提取描述和要求
            # Workday网站结构复杂，需要根据实际HTML调整
            desc_sections = soup.find_all(['div', 'section'], class_=re.compile(r'description|requirement|qualification', re.I))
            
            for section in desc_sections:
                text = section.get_text(strip=True)
                if 'requirement' in section.get('class', []) or 'qualification' in section.get('class', []):
                    job_info['requirements'].append(text)
                else:
                    job_info['description'] += text + "\n"
            
            return job_info
            
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            print("💡 提示: 请手动复制岗位描述到 job_description.txt")
            return {'url': job_url, 'title': '需要手动输入', 'requirements': []}
    
    def extract_keywords(self, job_description: str) -> List[str]:
        """
        从岗位描述中提取关键词
        """
        # 技术关键词
        tech_keywords = [
            'AI Agent', 'Multi-Agent', 'LLM', 'Large Language Model', 'NLP',
            'Deep Learning', 'Machine Learning', 'PyTorch', 'TensorFlow',
            'CUDA', 'GPU', 'Distributed Systems', 'Cloud Computing',
            'Autonomous Vehicle', 'Robotics', 'Computer Vision',
            'Reinforcement Learning', 'Transformer', 'Agent Framework'
        ]
        
        found_keywords = []
        desc_lower = job_description.lower()
        
        for keyword in tech_keywords:
            if keyword.lower() in desc_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def match_resume_sections(self, job_requirements: List[str], resume_content: str) -> Dict:
        """
        匹配简历内容与岗位要求
        """
        matches = {
            'relevant_experience': [],
            'relevant_skills': [],
            'relevant_projects': [],
            'match_score': 0
        }
        
        requirements_text = ' '.join(job_requirements).lower()
        
        # 检查工作经验匹配
        experience_keywords = self.extract_keywords(requirements_text)
        
        # 从简历中提取相关部分
        # 这里需要根据实际简历结构进行解析
        
        return matches
    
    def generate_customized_resume(self, job_info: Dict, output_path: str) -> str:
        """
        根据岗位要求生成定制化简历
        """
        print(f"\n✏️  生成定制化简历: {output_path}")
        
        # 读取原始简历
        with open(self.resume_path, 'r', encoding='utf-8') as f:
            resume_content = f.read()
        
        # 提取岗位关键词
        all_requirements = ' '.join(job_info.get('requirements', []))
        keywords = self.extract_keywords(all_requirements)
        
        print(f"📌 岗位关键词: {', '.join(keywords)}")
        
        # 生成定制化版本
        customized_resume = resume_content
        
        # 在简历开头添加岗位匹配说明（注释形式）
        job_match_comment = f"""
% ============================================
% 定制化简历 - 针对岗位: {job_info.get('title', 'NVIDIA Position')}
% 岗位URL: {job_info.get('url', '')}
% 匹配关键词: {', '.join(keywords)}
% 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
% ============================================
"""
        customized_resume = job_match_comment + customized_resume
        
        # 保存定制化简历
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(customized_resume)
        
        print(f"✅ 定制化简历已保存: {output_path}")
        
        return output_path
    
    def create_application_guide(self, job_info: Dict, resume_path: str) -> str:
        """
        创建申请指导文档
        """
        guide = f"""
# NVIDIA岗位申请指导

## 岗位信息
- **职位**: {job_info.get('title', 'N/A')}
- **URL**: {job_info.get('url', 'N/A')}
- **地点**: {job_info.get('location', 'Shanghai, China')}

## 申请步骤

### 1. 准备材料
- ✅ 定制化简历: {resume_path}
- ✅ 英文简历: resume_en.pdf
- ✅ 求职信（可选）

### 2. 申请流程
1. 访问岗位URL: {job_info.get('url', '')}
2. 点击 "Apply" 按钮
3. 填写个人信息
4. 上传简历: {resume_path.replace('.tex', '.pdf')}
5. 回答申请问题
6. 提交申请

### 3. 简历定制要点
- 强调与岗位相关的项目经验
- 突出匹配的技术栈
- 量化成果和影响

### 4. 注意事项
- ⚠️ 确保信息真实，不要造假
- ⚠️ 每个岗位使用定制化简历
- ⚠️ 仔细阅读岗位要求
- ⚠️ 保存申请确认信息

## 岗位要求摘要
{chr(10).join(f'- {req[:200]}...' if len(req) > 200 else f'- {req}' for req in job_info.get('requirements', [])[:5])}

---
生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        guide_path = f"application_guide_{job_info.get('title', 'job').replace(' ', '_')[:30]}.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"📝 申请指导已保存: {guide_path}")
        return guide_path


def main():
    """
    主函数 - 自动化申请流程
    """
    print("=" * 60)
    print("🚀 NVIDIA岗位申请助手")
    print("=" * 60)
    
    agent = NVIDIAJobAgent()
    
    # 示例：处理特定岗位
    job_urls = [
        "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Senior-Software-Engineer--Multi-Agent-System---AV-Infrastructure_JR2010348",
        "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Developer-Technology-Engineer--AI_JR2000017"
    ]
    
    print("\n📋 处理岗位列表:")
    for i, url in enumerate(job_urls, 1):
        print(f"{i}. {url}")
    
    # 处理每个岗位
    for i, job_url in enumerate(job_urls, 1):
        print(f"\n{'='*60}")
        print(f"处理岗位 {i}/{len(job_urls)}")
        print(f"{'='*60}")
        
        # 解析岗位描述
        job_info = agent.parse_job_description(job_url)
        
        # 生成定制化简历
        job_title_safe = re.sub(r'[^\w\s-]', '', job_info.get('title', f'job_{i}'))[:50]
        resume_output = f"resume_customized_{job_title_safe.replace(' ', '_')}.tex"
        
        agent.generate_customized_resume(job_info, resume_output)
        
        # 编译PDF
        print(f"\n📄 编译PDF...")
        import subprocess
        try:
            subprocess.run(['xelatex', '-interaction=nonstopmode', resume_output], 
                         check=True, capture_output=True)
            print(f"✅ PDF已生成: {resume_output.replace('.tex', '.pdf')}")
        except Exception as e:
            print(f"⚠️  PDF编译失败: {e}")
            print("💡 请手动运行: xelatex resume_customized_*.tex")
        
        # 创建申请指导
        agent.create_application_guide(job_info, resume_output)
        
        print(f"\n✅ 岗位 {i} 处理完成!")
        time.sleep(2)  # 避免请求过快
    
    print("\n" + "=" * 60)
    print("🎉 所有岗位处理完成!")
    print("=" * 60)
    print("\n📌 下一步:")
    print("1. 检查生成的定制化简历")
    print("2. 访问岗位URL进行申请")
    print("3. 上传对应的定制化简历PDF")
    print("4. 保存申请确认信息")


if __name__ == "__main__":
    main()
