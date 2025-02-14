import time
from config import Config
from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.api_key = Config.LLM_API_KEY
        self.base_url = Config.LLM_BASE_URL

    def query(self, input_message):
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        max_retries = 3  
        delay = 2        

        for attempt in range(1, max_retries + 1):
            try:
                completion = client.chat.completions.create(
                    model=Config.LLM_MODEL, 
                    messages=[
                        {'role': 'system', 'content': 'You are a helpful assistant.'},
                        {'role': 'user', 'content': f'{input_message}'}
                    ],
                )
                content = completion.choices[0].message.content
                return content
            except Exception as e:
                print(f"尝试第 {attempt} 次请求失败，错误信息：{e}")
                if attempt == max_retries:
                    print("达到最大重试次数，退出。")
                    raise 
                else:
                    print(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)
