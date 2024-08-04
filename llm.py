import streamlit as st
import random
import time
import ollama
from ollama import Client
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.llms import Ollama

modelname = 'ch-doonoi-01:latest'
# client = Client(host="http://68.173.160.106:11434")

host="http://68.173.160.106:11434"

llm = Ollama(base_url=host, model="ch-doonoi-01:latest", num_gpu=2)

# Data Loading #######
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from sentence_transformers import SentenceTransformer


from langchain_core.messages import HumanMessage, SystemMessage
import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import BSHTMLLoader
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain




# Load, chunk and index the contents 
md_path = "./ComposTogether.md"

# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("post-content", "post-title", "post-header")
#         )
#     ),
# )

loader = TextLoader(md_path)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# ChromaDB 
vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_function)


# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()


# ### Contextualize question ###
# contextualize_q_system_prompt = (
#     "Given a chat history and the latest user question "
#     "which might reference context in the chat history, "
#     "formulate a standalone question which can be understood "
#     "without the chat history. Do NOT answer the question, "
#     "just reformulate it if needed and otherwise return it as is."
# )

# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ('human', "{input}")
#     ]
# )

# history_aware_retriever = create_history_aware_retriever(
#     llm, retriever, contextualize_q_prompt
# )


# ### Answer question ###
# # system_prompt = (
# #     "You are an assistant for question-answering tasks. "
# #     "Use the following pieces of retrieved context to answer "
# #     "the question. If you don't know the answer, say that you "
# #     "don't know. Use three sentences maximum and keep the "
# #     "answer concise."
# #     "\n\n"
# #     "{context}"
# # )

# system_prompt = """Use the following pieces of context to answer the question at the end. If you don't know the answer and the question is specifically regarding ComposTogether (the community composting program based in Fort Lee), just say that you don't know and to email the program, don't try to make up an answer. If you don't know the answer and the question is not specifically about ComposTogether, you can get the answer from the Internet but never make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
# {context}
# Question: {question}
# Helpful Answer:"""
# QA_CHAIN_PROMPT = PromptTemplate.from_template(system_prompt)

# qa_chain = RetrievalQA.from_chain_type(
#     llm,
#     retriever=retriever,
#     return_source_documents=True,
#     chain_type_kwargs={"prompt":QA_CHAIN_PROMPT}
# )

# qa_prompt = ChatPromptTemplate.from_messages(

#         [
#             ('system', system_prompt), 
#             MessagesPlaceholder("chat_history"),
#             ('human', "{input}")
#         ]
# )

# question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)



# ### Statefully manage chat history ###
# store = {}


# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]


# conversational_rag_chain = RunnableWithMessageHistory(
#     rag_chain,
#     get_session_history,
#     input_message_key="input",
#     history_messages_key="chat_history",
#     output_messages_key="answer"
# )



# prompt = hub.pull("rlm/rag-prompt")


# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )


# Load the sentence transformer model for computing similarities
# similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

# # Function to determine if the context contains a valid answer
# def is_answer_in_context(context_response, question, threshold=0.7):
#     question_embedding = similarity_model.encode(question, convert_to_tensor=True)
#     response_embedding = similarity_model.encode(context_response, convert_to_tensor=True)
#     simmiliarity_score =  similarity_model.similarity(question_embedding, response_embedding)
#     return simmiliarity_score > threshold

memory = ConversationBufferMemory(
    memory_key="chat_history", #chat history as a list instead of a string
    return_messages=True
)

qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory
)

# Streamed response emulator
def get_response(question):

    # response = rag_chain.invoke(question)

    # response = conversational_rag_chain.invoke(
    # {
    #     "input": question
    # },
    # config = {
    #     "configurable": {"session_id": "abc123"}
    # })['answer']

    # if is_answer_in_context(response, question):
    #     yield "## From Context:\n" + response

    # else:
    #     fallback_response = llm.invoke(question)
    #     yield "## From LLM: \n" + fallback_response

    result = qa({"question":question})
    return result["answer"]

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

st.title("Test AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(get_response(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


# for i in range(5):
#     question = input("Ask anything: ").split()
    # result = qa({"question":"What is ComposTogether?"})
    # print(result["answer"])