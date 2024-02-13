from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import os

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = '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'

# Initialize the database and language model
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Prompt the user for a question
question = input("What is your question: ")

# Generate the SQL query from the question
write_query = create_sql_query_chain(llm, db)
query_result = write_query.invoke({"question": question})

if 'query' not in query_result:
    print("Failed to generate SQL query.")
    exit()

sql_query = query_result['query']
print(f"Generated SQL Query: {sql_query}")

# Execute the generated SQL query
execute_query = QuerySQLDataBaseTool(db=db)
execution_result = execute_query.invoke({"query": sql_query})
print(f"SQL Query Result: {execution_result}")

# Assuming you want to further process or answer based on the query result,
# here we simulate the process to generate a final answer.
# Replace this part with your actual logic to generate the final answer.
# For example, you can use another prompt with the LLM to generate a natural language answer
# based on the question, SQL query, and its result.
# This step is missing in your code but you would typically do something like this:

final_answer_prompt = f"""
Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {sql_query}
SQL Result: {execution_result}
Answer:
"""

# Generate the final answer using the language model
final_answer_result = llm.invoke({"prompt": final_answer_prompt})
print(f"Final Answer: {final_answer_result['choices'][0]['message']['content']}")
