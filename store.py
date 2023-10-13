import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings, CohereEmbeddings
from langchain.document_loaders import PyPDFLoader, DirectoryLoader

import os
from utils import logtime

STORE_DIR = "db/"
EMBEDDINGS = "embeddings"
embeddings = None
chunks = None

@logtime
def load_chunks():
    global chunks
    if not chunks:
        #load the pdf files from the path
        loader = DirectoryLoader('docs/',glob="*.pdf",loader_cls=PyPDFLoader)
        documents = loader.load()

        #split text into chunks
        text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        chunks = text_splitter.split_documents(documents) 
    
    return chunks

def load_hf_embeddings():
    global embeddings
    if not embeddings:
        #create embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                    model_kwargs={'device':"cpu"})
    return embeddings

@logtime
def init_vector_store(index):

    embeddings = load_hf_embeddings()
    #check if vector store exists
    if os.path.exists(STORE_DIR+index+".faiss"):
        #load Vector store locally
        store = FAISS.load_local(STORE_DIR,embeddings,index)
        return store
    
    #vectorstore
    store = FAISS.from_documents(load_chunks(),embeddings)
    store.save_local(STORE_DIR,index)
    return store