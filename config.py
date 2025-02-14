import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PDF_DIRECTORY = "./pdf_temp" # PDF存储路径
    RESULT_DIRECTORY = "./result" # 输出储存路径

    # LLM设置
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    LLM_MODEL = "deepseek-v3"

    # Arxiv搜索设置
    ARXIV_SEARCH_QUERY = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL" 
    ARXIV_SEARCH_DAYS = 1
    ARXIV_SEARCH_NUM = 2

    # LLM提示
    LLM_FILTER_PROMPT = """
    请根据以下论文信息判断是否与生成模型、分布变换方法（如流匹配、最优传输、薛定谔桥等等）相关，若相关回复Y，不相关回复N。你的回复只能包括Y或N，不能有任何其他文字。
    标题: {title}
    摘要: {summary}
    你的回复[Y/N]:
    """
    LLM_SUMMARY_PROMPT = "请模仿猫娘的语气，用中文总结这篇论文的核心贡献和技术方法。不要写得太长，尽可能简洁，200字以内即可。论文内容：{content}"
