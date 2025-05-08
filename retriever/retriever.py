# -*- coding: utf-8 -*-
# @Time    : 2025/4/8 16:44
# @Author  : cz
# @File    : retriever.py
# @Software: PyCharm
import numpy as np
from embedding.embedding import Embedding
from vector_store.vectorstore import PGVectorStore
from data_loader.data_loader import ContractParser,ContractChunker,get_files


# 修改后的检索模块
class PGContractRetriever:
    def __init__(self,collection_name):
        self.store = PGVectorStore(collection_name=collection_name)
        self.retriever = self.store.get_retriever()

    def document_filtered_search(self, query, doc_titles=None, top_k=10):
        if doc_titles:
            filter = {"doc_title": {"$ilike": doc_titles[0]}}

        return self.retriever.invoke(
            query,
            k=top_k,
            filter=filter
        )

