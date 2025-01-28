from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch


def create_vectordb(documents, k: int):
    try:
        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)

        # Define embeddings using OpenAI
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

        # Create a vector database from the document chunks and embeddings
        db = DocArrayInMemorySearch.from_documents(chunks, embeddings)

        # Define a retriever to search the vector database
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        return retriever

    except Exception as e:
        print(f"An error occurred: {e}")
