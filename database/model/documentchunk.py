# -*- coding: utf-8 -*-
# @Time    : 2025/4/9 16:31
# @Author  : cz
# @File    : documentchunk.py
# @Software: PyCharm
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, text
from pgvector.sqlalchemy import Vector
from config import EMBEDDING_DIM
from database.engins import pg_engine,SessionLocal
from embedding.embedding import Embedding

Base = declarative_base()

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM))  # pgvector向量列
    document_id = Column(String, index=True)    # 原始文档ID
    chunk_index = Column(Integer)               # 分块序号


# 创建数据库表
def create_tables():
    Base.metadata.create_all(bind=pg_engine)

# 启用pgvector扩展
def enable_pgvector():
    with pg_engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()




