import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from re import search
from dotenv import load_dotenv
from openai import OpenAI

PDF_PATH = "app/data/dental_benefits_summary.pdf"
# =====================================================
# Environment & OpenAI
# =====================================================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_rag_chain():
    #Create the loader
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages from PDF")

    #Chunk document
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks=splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")


    # Create the embeddings + FAISS index

    embeddings=OpenAIEmbeddings()

    vectorstore=FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    retriever=vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.25, "k": 8})
    
    ## Create the Dental QA chain
    llm=ChatOpenAI(model_name="gpt-4o-mini",
                temperature=0) #We want deterministic answers so Temperature=0)

#Prompt:
    prompt = ChatPromptTemplate.from_template("""
You are a dental benefits expert.

Use ONLY the provided policy text.
If multiple rules apply, combine them carefully.
If coverage depends on conditions, state those conditions explicitly.
If information is missing, say "Not specified in policy."
Use this tool to answer questions about a patient's dental coverage,
including benefits, coverage percentages, exclusions, deductibles,
and annual limits.
Return page numbers as citations.

Policy text:
{context}

Question:
{question}

Answer clearly and precisely:
""")

    ## Create the Dental QA chain
    llm=ChatOpenAI(model_name="gpt-4o-mini",
                temperature=0) #We want deterministic answers so Temperature=0
    
    
    return (
        {
            "context": retriever,
            "question": lambda x: x
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    
rag_chain=build_rag_chain()
   