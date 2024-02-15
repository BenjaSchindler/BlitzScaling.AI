from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
import os
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

#Falta un async await para answer

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = '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'

db = SQLDatabase.from_uri("sqlite:///./User-Details.db")

question = input("What is you question: ")

llm = ChatOpenAI()


execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
query = write_query.invoke({"question": question})
chain = write_query | execute_query
result = chain.invoke({"question": question})

print(question, query, result)



answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

final_result = chain.invoke({"question": question})
print(final_result)