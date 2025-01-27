# Chat with you Data: Meet Taira, the conversational AI chatbot

Taira is a conversational AI chatbot capable of reading and interacting with various types of documents such as PDF, Word, Excel files, and webpages. Powered by a Retrieval-Augmented Generation (RAG) model, it provides answers based on document contents using in-context learning techniques, including few-shot learning and chain-of-thought reasoning.

## Features

- **Supports multiple document types**:
  - PDF
  - Word (DOCX)
  - Excel (XLSX)
  - Webpages (via URLs)
  
- **Chat history**: Taira remembers the conversation history and provides context-aware responses.
- **Vector Database**: Creates a vectorized database from document contents for efficient document retrieval and question answering.
- **In-context learning**: Uses few-shot learning and chain-of-thought reasoning to answer questions based on the document contents.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/taira.git
    cd taira
    ```
   
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Set up environment variables:
- Create a .env file and add the OPENAI_API_KEY key with your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Run the application:
   ```bash
   python src\main.py
   ```

## How It Works
1. Loading Documents: Taira can process the following document types:

- PDF: Loaded using the PyPDFLoader.
- Word (DOCX): Loaded using Docx2txtLoader.
- Excel: Loaded with UnstructuredExcelLoader.
- Webpages: URL input is processed with WebBaseLoader.

2. Interaction:

- After loading a document or webpage, you can interact with Taira by asking questions.
- Taira retrieves relevant information from the loaded documents using a vector database.
- It answers questions based on the document content or chat history.

## Examples Conversation
After loading a document, you can ask questions like:

- User: "What are the key points in the report?"
- Taira: "The report outlines the major findings, focusing on market trends, consumer behavior, and product preferences."

## Contact
For any questions or clarifications, please contact Raza Mehar at [raza.mehar@gmail.com].


