from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader, WebBaseLoader, Docx2txtLoader
from vectordb import create_vectordb
from chatbot import chat_with_data
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*ValidationError.*")


def process_documents(loader, file_path, file_type) -> str:
    try:
        documents = loader.load()
        retriever = create_vectordb(documents, k=1)
        chat_with_data(retriever, file_path, file_type)
    except Exception as e:
        return f"An error occurred while processing the document: {str(e)}"


def load_pdf(file_path: str, file_type: str) -> str:
    try:
        loader = PyPDFLoader(file_path)
        process_documents(loader, file_path, file_type)
    except Exception:
        print('Invalid file format. Please provide a valid file format.')
        return


def load_excel(file_path: str, file_type: str) -> str:
    try:
        loader = UnstructuredExcelLoader(file_path, mode="single")
        process_documents(loader, file_path, file_type)
    except Exception:
        print('Invalid file format. Please provide a valid file format.')
        return


def load_url(file_path: str, file_type: str) -> str:
    loader = WebBaseLoader(file_path)
    process_documents(loader, file_path, file_type)


def load_word(file_path: str, file_type: str) -> str:
    try:
        loader = Docx2txtLoader(file_path)
        process_documents(loader, file_path, file_type)
    except Exception:
        print('Invalid file format. Please provide a valid file format.')
        return
