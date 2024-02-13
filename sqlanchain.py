from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
import os
from langchain_community.utilities import SQLDatabase

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = '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'

# Define the template for generating SQL queries
template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_template(template)

# Connect to the SQLite database
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")

# Function to get the database schema
def get_schema(_):
    return db.get_table_info()

# Function to run a query against the database
def run_query(query):
    return db.run(query)

# Initialize the language model with a specific model and temperature
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create a chain for generating SQL queries and getting responses
chain = create_sql_query_chain(llm, db)

# Invoke the chain to get a response for a specific question
response = chain.invoke({"question": "How many employees are there?"})
print(response)  # Print the response for debugging

# Initialize the main model for generating natural language responses
model = ChatOpenAI()

# Define the chain for SQL response parsing and query generation
sql_response = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | model.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

# Invoke the chain for a specific question and print the SQL query
sql_query_result = sql_response.invoke({"question": "How many employees are there?"})
print(sql_query_result)

# Template for generating natural language responses based on SQL query and response
template_response = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
    {schema}

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template_response)

# Chain for generating full natural language responses
full_chain = (
    RunnablePassthrough.assign(query=sql_response).assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response
    | model
)

# Invoke the full chain for a specific question and print the natural language response
final_response = full_chain.invoke({"question": "How many employees are there?"})
print(final_response)

