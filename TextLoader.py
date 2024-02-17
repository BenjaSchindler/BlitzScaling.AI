import os
import sys
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

APIKEY = os.getenv('OPENAI_API_KEY')
if not APIKEY:
    sys.exit("API key not found. Please set the OPENAI_API_KEY environment variable.")


question = input("Introduce your question: ")

os.environ["OPENAI_API_KEY"] = APIKEY

# Load the document, split it into chunks, embed each chunk and load it into the vector store.
raw_documents = TextLoader('Things.txt').load()
text_splitter = CharacterTextSplitter()
documents = text_splitter.split_documents(raw_documents)
db = Chroma.from_documents(documents, OpenAIEmbeddings())

query = question
docs = db.similarity_search(query)
print(docs[0].page_content)