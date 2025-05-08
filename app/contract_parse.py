# -*- coding: utf-8 -*-
# @Time    : 2025/4/14 15:15
# @Author  : cz
# @File    : contract_parse.py
# @Software: PyCharm
from logger import logger
class ContractParse:
    def __init__(self,stucture_data,company):
        self.stucture_data = stucture_data
        self.contract_count = self.get_count(company)
        self.contract_info = self.get_contract_info(company)
        logger.info(f"**{company}所有合同解析成功**")

    def get_count(self,company):
        doc_title = set()
        count = 0
        for doc in self.stucture_data:
            doc_title.add(doc.metadata['doc_title'])

        for doc in doc_title:
            if company in doc:
                count += 1

        return count

    def get_contract_info(self,company):
        doc_content = {}
        content_prompt = ""
        for doc in self.stucture_data:
            if company in doc.metadata['doc_title']:
                if doc_content.get(doc.metadata['doc_title']) is None:
                    doc_content[doc.metadata['doc_title']] = doc.page_content
                else:
                    doc_content[doc.metadata['doc_title']] += doc.page_content

        for doc_title,doc_content in doc_content.items():
            content_prompt += f"**合同名称**：{doc_title}\n合同内容：{doc_content}\n\n"

        return content_prompt