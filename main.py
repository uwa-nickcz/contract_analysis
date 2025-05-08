# -*- coding: utf-8 -*-
# @Time    : 2025/4/8 15:03
# @Author  : cz
# @File    : main.py
# @Software: PyCharm

from data_loader.data_loader import ContractParser,ContractChunker, get_files
from retriever.retriever import PGContractRetriever
from llm.llm import LLM
from prompt import QUERY_PROMPT,QUERY_COMPANY_PROMPT


if __name__ == '__main__':
    # ================= 元数据检索使用示例 =================
    # 处理文档（沿用之前的ContractParser和ContractChunker）
    # parser = ContractParser()
    # chunker = ContractChunker()
    # all_chunks = []
    # documents = get_files(r"D:\chenzhu\generative-ai-for-beginners\example_data\东营算力中心合同")
    # for doc_file in documents:
    #     structured_data = parser.parse_document_by_chunk(doc_file)
    #     all_chunks.extend(chunker.generate_chunks(structured_data))

    # 创建向量存储
    # vector_store = PGVectorStore().create_store(all_chunks)
    usr_question = "成都共佳创艺数字艺术发展有限公司的合同总金额是多少"
    prompt_query = QUERY_PROMPT.format(usr_question=usr_question)
    conpany_prompt_query = QUERY_COMPANY_PROMPT.format(usr_question=usr_question)
    query = '%'+LLM._call(prompt_query)+'%'
    company = '%'+LLM._call(conpany_prompt_query)+'%'
    # 执行查询
    retriever = PGContractRetriever()
    results = retriever.document_filtered_search(
        query,
        doc_titles=[company]
    )

    # 打印结果（格式与之前兼容）
    for doc in results:
        print(f"【文档】{doc.metadata['doc_title']}")
        print(f"【章节】{doc.metadata['section_hierarchy']}")
        print(doc.page_content+ "...\n")
