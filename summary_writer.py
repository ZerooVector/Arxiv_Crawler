import os
from datetime import datetime

class SummaryWriter:
    @staticmethod
    def create_mdfile(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        

        today_str = datetime.now().strftime('%Y-%m-%d')
        
        filename = f"{today_str}.md"
        file_path = os.path.join(directory, filename)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"# {today_str}\n\n")
        
        print(f"文件已创建: {file_path}")
        return file_path

    @staticmethod
    def append_content(directory, content):
        today_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{today_str}.md"
        file_path = os.path.join(directory, filename)
        

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n")
        

