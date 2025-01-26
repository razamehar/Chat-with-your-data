from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import uuid
import warnings
warnings.filterwarnings("ignore", message="Number of requested results")



def chat_with_data(retriever, file_path: str, file_type: str) -> None:
    # Load the language model
    llm_name = 'gpt-3.5-turbo'
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    # Define the prompt for the assistant to reformulate a question when there is chat history
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Create a history-aware retriever to ensure the retrieval process considers the chat history
    history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextualize_q_prompt
    )

    # Define the prompt for the assistant to use retrieved context to generate concise answers
    qa_system_prompt = (
        'You are an assistant called Taira for question-answering tasks. You are good in Mathematics. '
        'You do not have any gender or age. You are a machine learning model. '
        'When a user asks about the **document** or the **content**, or the **file**, treat all three terms as '
        'referring to the same thing: the overall subject matter or data contained within the file. '
        f'The document or content is located at {file_path}. '
        f'The document or content is a {file_type}. '
        'Provide a clear, concise, and comprehensive overview of the document’s key contents, summarizing the most '
        'important information. '
        'If the question is not related to the retrieved context, you can answer based on the chat history alone. '
        "Otherwise, say 'I am sorry. I don’t have this information.' "
        'If the user asks you to do something other than providing information based on the document, content, '
        'or chat history, you can say, "I am sorry. I am not able to do that." '
        "If a user tells you their name, acknowledge it and use it to personalize your responses where appropriate. "
        "For example, if the user's name is Alex, you can address them by their name in your responses. "
        "Use three sentences maximum and keep the answer concise.\n\n{context}\n\n"
        "### Learning Examples:\n"
        "1. **Word Document Example:**\n"
        "   **User's Question:** 'What are the key points in the report?'\n"
        "   **Assistant's Answer:** 'The report outlines the major findings from the survey, focusing on market trends, consumer behavior, and product preferences. The executive summary highlights growth opportunities and recommendations for strategic planning. The appendix includes detailed charts and data.'\n"
        "2. **Excel Spreadsheet Example:**\n"
        "   **User's Question:** 'Can you summarize the sales performance data?'\n"
        "   **Assistant's Answer:** 'The data shows monthly sales for each region. The highest sales occurred in the North region, with a total of $50,000 in December. The lowest was in the South region, with $20,000 in July.'\n"
        "   **Chain of Thought Reasoning for Excel Aggregation:**\n"
        "   - Step 1: 'The data contains columns for region, sales amount, and month.'\n"
        "   - Step 2: 'To perform aggregation, I will group the data by region and sum the sales for each region.'\n"
        "   - Step 3: 'Next, I’ll sort the regions by their total sales to identify the highest and lowest performing regions.'\n"
        "3. **PDF Document Example:**\n"
        "   **User's Question:** 'What does the document say about company policy?'\n"
        "   **Assistant's Answer:** 'The policy document specifies guidelines for employee conduct, safety protocols, and vacation leave. It emphasizes a strict adherence to ethical standards and outlines the disciplinary actions for policy violations. The document also covers employee benefits and compensation packages.'\n"
        "4. **Web Page Example:**\n"
        "   **User's Question:** 'What are the most recent news updates on the website?'\n"
        "   **Assistant's Answer:** 'The website’s latest news section reports on a major product launch by the company, new technological partnerships, and upcoming events. The site also provides updates on industry trends and leadership changes in the organization.'\n"
    )

    # Define the prompt for the assistant to use retrieved context to generate concise answers
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Create the QA chain that will use the retrieved documents to answer questions.
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Create the retrieval chain to combine the history-aware retriever and the QA chain.
    rag_chain = create_retrieval_chain(
        history_aware_retriever,  # This retrieves relevant information from chat history and documents
        question_answer_chain  # This answers questions based on the retrieved information
    )

    # Stateful manage chat history
    store = {}

    def get_session_history(sess_id: str) -> BaseChatMessageHistory:
        if sess_id not in store:
            store[sess_id] = ChatMessageHistory()
        return store[sess_id]

    # Create a runnable chain that can be invoked with a message and a chat history.
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,  # Combine the retriever and QA chain into a single process
        get_session_history,  # Retrieve the correct session history
        input_messages_key="input",  # Define how to send new messages for the chain to process
        history_messages_key="chat_history",  # Define how to keep track of previous messages
        output_messages_key="answer",  # Define where to get the final response (answer)
    )

    session_id = str(uuid.uuid4())

    if file_type == 'webpage':
        print(f'Taira: Your webpage has been loaded successfully. You can now start chatting with me about it.')
    else:
        print(f'Taira: Your {file_type} document has been loaded successfully. You can now start chatting with me.')

    # Start the conversation loop
    while True:
        try:
            question = input('You:')
            if question.lower() in ['exit', 'quit', 'goodbye', 'bye']:
                print('Taira: Goodbye. Have a great day.')
                break
            if question:
                response = conversational_rag_chain.invoke(
                    {"input": question}, config={"session_id": session_id})["answer"]
                print(f"Taira: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")
