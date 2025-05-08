# -*- coding: utf-8 -*-
# @Time    : 2025/4/9 16:20
# @Author  : cz
# @File    : config.py
# @Software: PyCharm

# 数据库配置
PG_DATABASE_URL = "postgresql+psycopg2://user:password@localhost:port/postgres"
EMBEDDING_DIM = 1024
# 模型部署框架
FRAMEWORK = "vllm"
# 模型名称
# MODEL = "deepseek-r1:70b"
MODEL = "Qwen2.5-72B-Instruct-AWQ"
# Ollama Embedding API 的基础 URL
OLLAMA_API_URL = "http://localhost:11435/api/embed"

# llm API 的基础 URL
LLM_API_URL = "http://localhost:9300/v1/chat/completions"
# LLM_API_URL = "http://172.16.98.1:11434/api/generate"

#适配openai的llm api
OPENAI_API_URL = "http://localhost:9300/v1"