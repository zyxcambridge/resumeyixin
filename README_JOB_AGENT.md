# NVIDIA岗位申请助手

自动找工作Agent - 帮助您快速申请NVIDIA相关岗位。

## 功能特点

1. **岗位搜索**: 搜索NVIDIA AI Agent相关岗位（上海）
2. **岗位解析**: 自动解析岗位描述和要求
3. **简历定制**: 根据岗位要求生成定制化简历
4. **申请指导**: 生成详细的申请步骤指导

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行助手

```bash
python job_application_agent.py
```

### 3. 手动搜索岗位（推荐）

由于Workday网站需要JavaScript，建议手动搜索：

1. 访问: https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite
2. 搜索关键词: "AI Agent" OR "Multi-Agent" OR "LLM"
3. 筛选地点: Shanghai, China
4. 将找到的岗位URL添加到脚本中

### 4. 处理岗位

脚本会：
- 解析岗位描述和要求
- 提取关键词
- 生成定制化简历
- 编译PDF
- 创建申请指导文档

## 岗位URL示例

```python
job_urls = [
    "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Senior-Software-Engineer--Multi-Agent-System---AV-Infrastructure_JR2010348",
    "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/details/Developer-Technology-Engineer--AI_JR2000017"
]
```

## 输出文件

- `resume_customized_*.tex`: 定制化简历LaTeX源文件
- `resume_customized_*.pdf`: 定制化简历PDF
- `application_guide_*.md`: 申请指导文档

## 注意事项

⚠️ **重要提示**:
- 不要造假，确保信息真实
- 每个岗位使用对应的定制化简历
- 仔细阅读岗位要求
- 保存申请确认信息

## 快速申请流程

1. **准备阶段**
   - 运行脚本生成定制化简历
   - 检查简历内容

2. **申请阶段**
   - 访问岗位URL
   - 点击"Apply"按钮
   - 填写个人信息
   - 上传定制化简历PDF
   - 回答申请问题

3. **提交确认**
   - 确认所有信息正确
   - 点击"Submit"
   - 保存申请确认信息

## 定制化策略

针对每个岗位，简历会：
- 强调相关项目经验
- 突出匹配的技术栈
- 量化成果和影响
- 调整描述顺序和重点

## 技术支持

如有问题，请检查：
- Python版本 >= 3.8
- 依赖包已安装
- LaTeX环境已配置（用于PDF生成）
