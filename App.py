import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from html_template import css, bot_template, user_template

# def get_pdf_text(pdf_docs):
#  loaders = []
#  for pdf in pdf_docs:
#    loaders.append(PyPDFLoader('pdf'))
#  text = []
#  for loader in loaders:
#    text.extend(loader.load())
#  return text

def get_pdf_text(pdf_docs):
  text = ""
  for pdf in pdf_docs:
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
      text += page.extract_text()
  return text

def get_text_splits(text):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
  )
  text_splits = text_splitter.split_text(text)
  return text_splits

def get_vectorstore(text_splits):
  embeddings = OpenAIEmbeddings()
  vectordb = FAISS.from_texts(texts=text_splits, embedding=embeddings)
  return vectordb

def get_conversation_chain(vectordb):
  llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
  memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
  )
  conversation_chain = ConversationalRetrievalChain.from_llm(
    llm = llm,
    retriever = vectordb.as_retriever(),
    memory = memory
  )
  return conversation_chain

def handle_userinput(user_question):
  response = st.session_state.conversation({'question': user_question})
  st.session_state.chat_history = response['chat_history']

  for i, message in enumerate(st.session_state.chat_history):
    if i%2 == 0:
      st.write(user_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)
    else:
      st.write(bot_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)

    

def main():
  load_dotenv()
  st.set_page_config(page_title="Chat with your PDFs", page_icon=":books:")
  st.write(css, unsafe_allow_html=True)

  if "conversation" not in st.session_state:
    st.session_state.conversation = None

  if "chat_history" not in st.session_state:
    st.session_state.chat_history = None


  st.header("Chat with your PDFs :books:")
  user_question = st.text_input("Ask a question about your documents:")
  if user_question:
    handle_userinput(user_question)

  with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
      with st.spinner("Processing..."):
        # get pdf text
        raw_text = get_pdf_text(pdf_docs)

        # split text into chunks
        text_splits = get_text_splits(raw_text)

        # create vector store
        vectordb = get_vectorstore(text_splits)

        # create conversation chain
        st.session_state.conversation = get_conversation_chain(vectordb)

 


if __name__ == '__main__':
  main()