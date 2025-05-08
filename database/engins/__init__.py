# -*- coding: utf-8 -*-
# @Time    : 2025/4/9 16:16
# @Author  : cz
# @File    : __init__.py.py
# @Software: PyCharm

import os
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import openai

from config import PG_DATABASE_URL


# 初始化数据库连接
pg_engine = create_engine(PG_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
