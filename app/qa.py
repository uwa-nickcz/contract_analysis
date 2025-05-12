# -*- coding: utf-8 -*-
# @Time    : 2025/4/14 14:58
# @Author  : cz
# @File    : qa.py
# @Software: PyCharm
import sys

# 添加根路径
root_path = '/data/ai/project/dongying/generative-ai'
sys.path.append(root_path)

from prompt import QUERY_PROMPT,QUERY_COMPANY_PROMPT,FINAL_QUERY_PROMPT,OVERTIME_FINAL_QUERY_PROMPT
from config import FRAMEWORK,COLLECTION_NAME
from llm.llm import LLM
from retriever.retriever import PGContractRetriever
from contract_parse import ContractParse
from logger import logger
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Generator,List,Optional


app = FastAPI()

class Item(BaseModel):
    model: Optional[str] = None
    messages: List[dict]  # Specify the type of list elements, e.g., dict
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stream: Optional[bool] = None


@app.post('/get_is_overtime')
def get_is_overtime(item:Item):

    message = item.messages[0]['content']
    stream = item.stream

    prompt_query = QUERY_PROMPT.format(usr_question=message)
    conpany_prompt_query = QUERY_COMPANY_PROMPT.format(usr_question=message)
    query = LLM._call(prompt_query).json()['choices'][0]['message']['content']
    company = LLM._call(conpany_prompt_query).json()['choices'][0]['message']['content']
    retriever = PGContractRetriever(collection_name=COLLECTION_NAME)
    results = retriever.document_filtered_search(
        '%'+'双方合同签订时间、日期'+'%',
        top_k=8,
        doc_titles=['%'+company+'%']
    )
    # 解析合同
    contract_parse = ContractParse(results,company)

    final_query = OVERTIME_FINAL_QUERY_PROMPT.format(company=company,
                                            usr_question='所有合同的签订时间分别是多久，简明扼要阐述，json输出',
                                            count=contract_parse.contract_count,
                                            contract_info=contract_parse.contract_info)

    date = LLM._call(final_query).json()['choices'][0]['message']['content']

    overtime_info = retriever.document_filtered_search(
        '%'+'产品交付日期、违约日期'+'%',
        top_k=5,
        doc_titles=['%'+company+'%']
    )
    contract_overtime = ContractParse(overtime_info,company)
    real_query = OVERTIME_FINAL_QUERY_PROMPT.format(
                                                    company=company,
                                                    usr_question=message+'仅回答结论',
                                                    count=contract_overtime.contract_count,
                                                    contract_info=contract_overtime.contract_info
                                                )
    # 打印最终结果
    if stream:
        def generate() -> Generator[str, None, None]:
            try:
                for chunk in LLM.steam_call(real_query,engine=FRAMEWORK,show=False):
                    chunk_json = chunk.__dict__
                    chunk_json['choices'][0] = chunk_json['choices'][0].__dict__
                    chunk_json['choices'][0]['delta'] = chunk_json['choices'][0]['delta'].__dict__
                    print(chunk_json)
                    # yield json.dumps(chunk_json)  # 逐步返回数据
                    yield f"data: {json.dumps(chunk_json)}\n\n"
            except Exception as e:
                logger.error(f"Error during streaming: {str(e)}")
                yield "Error occurred during processing."

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    else:
        return LLM._call(final_query)

@app.post('/query')
def query(item:Item):

    message = item.messages[0]['content']
    stream = item.stream

    prompt_query = QUERY_PROMPT.format(usr_question=message)
    conpany_prompt_query = QUERY_COMPANY_PROMPT.format(usr_question=message)
    query = LLM._call(prompt_query).json()['choices'][0]['message']['content']
    company = LLM._call(conpany_prompt_query).json()['choices'][0]['message']['content']

    logger.info(f"【公司】{company}")
    logger.info(f"【查询】{query}")

    # 执行查询
    retriever = PGContractRetriever(collection_name=COLLECTION_NAME)
    results = retriever.document_filtered_search(
        '%'+query+'%',
        top_k=15,
        doc_titles=['%'+company+'%']
    )

    # 解析合同
    contract_parse = ContractParse(results,company)
    if contract_parse.contract_count == 0:
        final_query = FINAL_QUERY_PROMPT.format(company=' ',
                                                usr_question=query,
                                                count=contract_parse.contract_count,
                                                contract_info='暂无相关合同信息，请忽略参考，直接回答问题')
    else:
        final_query = FINAL_QUERY_PROMPT.format(company=company,
                                                usr_question=query,
                                                count=contract_parse.contract_count,
                                                contract_info=contract_parse.contract_info)



    # 打印最终结果
    if stream:
        def generate() -> Generator[str, None, None]:
            try:
                for chunk in LLM.steam_call(final_query, engine=FRAMEWORK, show=False):
                    chunk_json = chunk.__dict__
                    chunk_json['choices'][0] = chunk_json['choices'][0].__dict__
                    chunk_json['choices'][0]['delta'] = chunk_json['choices'][0]['delta'].__dict__
                    print(chunk_json)
                    # yield json.dumps(chunk_json)  # 逐步返回数据
                    yield f"data: {json.dumps(chunk_json)}\n\n"
            except Exception as e:
                logger.error(f"Error during streaming: {str(e)}")
                yield "Error occurred during processing."

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    else:
        return LLM._call(final_query)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("qa:app", host="0.0.0.0", port=9010, reload=True)