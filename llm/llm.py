# -*- coding: utf-8 -*-
# @Time    : 2025/4/14 14:06
# @Author  : cz
# @File    : llm.py
# @Software: PyCharm
import requests
from config import LLM_API_URL,OPENAI_API_URL,MODEL
from requests.exceptions import RequestException
from openai import OpenAI
from logger import logger
import re
import json

class LLM:
    def __init__(self, model_name):
        self.model_name = model_name

    @staticmethod
    def _call(input, model=MODEL):
        # 请求数据
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": input
                }
            ],
            "temperature":0,
            "max_tokens":4096,
            "stream":False
        }

        try:
            response = requests.post(LLM_API_URL, json=payload)

            # 检查响应状态码
            if response.status_code == 200:
                result = response.json()
                try:
                    message = result['choices'][0]['message']['content']
                    logger.debug(message)
                    return response
                except:
                    message = re.sub(r'<think>[\s\S]*?<\/think>', '', result['response'], flags=re.DOTALL)
                    logger.debug(message)
                    return message.strip()
            else:
                raise RequestException(f"请求失败，状态码：{response.status_code}")

        except Exception as e:
            print("发生错误：", str(e))



    @staticmethod
    def steam_call(input, model=MODEL,engine='vllm',show=False):
        response_message = ''
        if engine == 'vllm':
            # 配置客户端连接本地vLLM服务
            client = OpenAI(
                base_url=OPENAI_API_URL,  # vLLM的API地址
                api_key="token-abc123"  # 任意非空字符串（vLLM默认不验证API密钥）
            )

            # 发起流式请求
            stream = client.chat.completions.create(
                model=model,  # 与启动命令中的--served-model-name一致
                messages=[
                    {"role": "user", "content": input}
                ],
                stream=True,  # 启用流式传输
                # max_tokens=1024,
                temperature=0
            )

            # 实时打印流式输出
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    response_message += content
                    if show:
                        print(content, end="", flush=True)
                yield chunk
                # 返回完整响应内容
            logger.debug(response_message)
            # return response_message
        elif engine == 'ollama':
            headers = {"Content-Type": "application/json"}

            data = {
                "model": model,
                "prompt": input,
                "max_tokens": 1024,
                "stream": True  # 关键参数：启用流式传输
            }

            with requests.post(LLM_API_URL, headers=headers, json=data, stream=True) as response:
                try:
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line.decode("utf-8"))
                            if chunk.get("done") != 'true':
                                if show:
                                    print(chunk.get("response", ""), end="", flush=True)
                                response_message += chunk.get("response", "")  # 持续返回生成的文本片段
                                yield chunk # 持续返回生成的文本片段
                except requests.exceptions.ChunkedEncodingError as e:
                    print(f"Stream interrupted: {str(e)}")
                logger.debug(re.sub(r'<think>[\s\S]*?<\/think>', '', response_message, flags=re.DOTALL).strip())
                return re.sub(r'<think>[\s\S]*?<\/think>', '', response_message, flags=re.DOTALL).strip()
if __name__ == '__main__':
    input = "你好"
    message = LLM._call(input)
