import os
import openai
import pinecone

from django.conf import settings

import langchain
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

PINECONE_API_KEY = settings.PINECONE_API_KEY
PINECONE_API_ENV = settings.PINECONE_API_ENV

openai_api_key = settings.OPENAI_API_KEY

def generate_ai_response(tone, language, message):
	prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
	{context}
	Question: {question}
	Answer in Italian:""".format(tone, language)
	qa_prompt = PromptTemplate(
		
		template=prompt_template, 
		input_variables=["context", "question"]
	)

	llm = OpenAI(temperature=0)
	index_file_path = os.path.join(settings.BASE_DIR, 'data')
	loader = DirectoryLoader(index_file_path, glob='**/*.pdf')
	loader = DirectoryLoader('PATH-TO-DRIVE-FOLDER/', glob='**/*.pdf')
	documents = loader.load()
	text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
	texts = text_splitter.split_documents(documents)
	embeddings = OpenAIEmbeddings()
	
	pinecone.init(
		
    	api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    	environment=PINECONE_API_ENV  
    )
	index_name = "mlqai"
	
	docsearch = Pinecone.from_documents(texts, embeddings, index_name=index_name)
	query = message
	docs = docsearch.similarity_search(query)
	chain = load_qa_chain(llm, chain_type="stuff")
	
	qa_chain = LLMChain(llm=llm, prompt=qa_prompt)

	answer = chain.run(input_documents=docs, question=query)
	
	return answer
"""

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(documents, embeddings)

llm = OpenAI(temperature=0)
question_generator = LLMChain(llm=llm, prompt=qa_prompt)
doc_chain = load_qa_chain(llm, chain_type="map_reduce")
doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

chain = ConversationalRetrievalChain(
    retriever=vectorstore.as_retriever(),
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
    memory=memory,
    return_source_documents=True,
)
chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = chain({"question": query, "chat_history": chat_history})
result['answer']
result['source_documents']

"""

	
