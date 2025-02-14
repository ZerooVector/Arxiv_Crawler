import requests
import os 
from PyPDF2 import PdfReader

class PDFProcessor:
    @staticmethod
    def download_pdf(directory, arxiv_url):
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        base = arxiv_url.split('/')[-1]
        if not base.endswith('.pdf'):
            base += '.pdf'
        save_path = os.path.join(directory, base)
        try:
            response = requests.get(arxiv_url, stream=True)
            response.raise_for_status()  
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: 
                        file.write(chunk)
            print(f"PDF 已成功下载到: {save_path}")
            return save_path
        except Exception as e:
            print(f"下载 PDF 时出错: {e}")
            return False

    @staticmethod
    def extract_text(pdf_path):
        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            print(f"读取 PDF 时出错: {e}")
            return ""