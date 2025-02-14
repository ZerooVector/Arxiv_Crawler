from config import Config
from llm_client import LLMClient
from arxiv_client import ArxivClient
from pdf_processor import PDFProcessor
from summary_writer import SummaryWriter
from tqdm import tqdm
import os 
import shutil


if __name__ == "__main__":
    config = Config()
    arxiv_client = ArxivClient()
    llm_client = LLMClient()

    SummaryWriter.create_mdfile(config.RESULT_DIRECTORY)

    papers = arxiv_client.get_recent_papers()
    papers_len = len(papers)


    filtered_papers = []
    for paper in tqdm(papers):
        # print(paper)
        paper_title = paper["title"]
        paper_summary = paper["summary"]
        filled_filter_prompt = config.LLM_FILTER_PROMPT.format(title=paper_title, summary=paper_summary)
        filter_response = llm_client.query(input_message=filled_filter_prompt)
        if "Y" in filter_response:
            filtered_papers.append(paper)

    filtered_papers_len = len(filtered_papers)

    # SummaryWriter.append_content("./result", "\n")
    SummaryWriter.append_content(config.RESULT_DIRECTORY, f"今天共找到了 {papers_len} 篇指定领域内的论文，其中与指定关键词相关的有 {filtered_papers_len} 篇。以下给出每一篇文章的具体总结。")


    for paper in tqdm(filtered_papers) :
        paper_title = paper["title"]
        paper_summary = paper["summary"]
        paper_url = paper["download_url"]
        save_path = PDFProcessor.download_pdf(config.PDF_DIRECTORY, paper_url)

        paper_text = PDFProcessor.extract_text(save_path)

        summary_prompt = config.LLM_SUMMARY_PROMPT.format(content=paper_text)
        summary_response = llm_client.query(input_message=summary_prompt)

        SummaryWriter.append_content(config.RESULT_DIRECTORY, f"## {paper_title}")
        SummaryWriter.append_content(config.RESULT_DIRECTORY, f"**下载地址**：{paper_url}")
        SummaryWriter.append_content(config.RESULT_DIRECTORY, f"**AI总结**： \n{summary_response}")
        SummaryWriter.append_content(" ")

    for filename in os.listdir(config.PDF_DIRECTORY):
        file_path = os.path.join(config.PDF_DIRECTORY, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                print(f"已删除文件： {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"已删除目录及其内容： {file_path}")
        except Exception as e:
            print(f"删除 {file_path} 时出错：{e}")
        

