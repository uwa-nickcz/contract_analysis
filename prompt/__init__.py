# -*- coding: utf-8 -*-
# @Time    : 2025/4/14 11:33
# @Author  : cz
# @File    : __init__.py.py
# @Software: PyCharm
from prompt.final_query_prompt import FINAL_QUERY_PROMPT
from prompt.final_query_prompt_overtime import OVERTIME_FINAL_QUERY_PROMPT
QUERY_COMPANY_PROMPT = """你是一个只能助手，你的思考应该简洁快速
你的任务是从一下用户问题中提取公司名称。只输出公司名称，不要输出任何其他信息。
用户问题: {usr_question}"""

QUERY_PROMPT = """你是一个智能助手。
你的任务是从用户的问题中提取出真实的问题，并去除其中的公司相关信息，你不需要回答用户的问题。
将真实问题和用户提供的背景信息合并成一句话，背景信息中不要包含公司信息。
只输出最后一句话，不带任何其他提示。如果问题中没有与公司合同相关的，请直接输出用户问题，保持主谓语与用户原文一致。
user_question: {usr_question}"""





