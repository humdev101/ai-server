import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..models.response import APIResponse as Response
from fastapi import status
from langchain_ollama import OllamaEmbeddings
from ..llms.llmSelector import getLLMFromModelName

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")

def generateEmbeddingsFromTextFile(inputFileName,outputFolderName):
    try:
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "rag_train_data", inputFileName)
        persistent_directory = os.path.join(current_dir, "embeddings_db", outputFolderName)

        # Check if the Chroma vector store already exists
        if not os.path.exists(persistent_directory):
            print("Persistent directory does not exist. Initializing vector store...")

            # Ensure the text file exists
            if not os.path.exists(file_path):
                response = Response(status.HTTP_404_NOT_FOUND,inputFileName+" not found","")
                return response
                # raise FileNotFoundError(
                #     f"The file {file_path} does not exist. Please check the path."
                # )

            # Read the text content from the file
            loader = TextLoader(file_path)
            documents = loader.load()

            # Split the document into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)

            # Display information about the split documents
            print("\n--- Document Chunks Information ---")
            print(f"Number of document chunks: {len(docs)}")
            print(f"Sample chunk:\n{docs[0].page_content}\n")

            # Create embeddings
            print("\n--- Finished creating embeddings ---")

            # Create the vector store and persist it automatically
            print("\n--- Creating vector store ---")
            db = Chroma.from_documents(
                docs, embeddings, persist_directory=persistent_directory)
            print("\n--- Finished creating vector store ---")
            response = Response(status.HTTP_201_CREATED,"Successfully Created Vector Store","Chroma db written to "+persistent_directory)
            return response
        else:
            print("Vector store already exists. No need to initialize.")
            response = Response(status.HTTP_409_CONFLICT,"vetor store in "+outputFolderName + " already exists","")
            return response
            
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        response = Response(status.HTTP_500_INTERNAL_SERVER_ERROR,"Something unexpected occured","")
        return response


def retrieveDataFromEmbeddings(query,vector_store_name,search_type,search_kwargs):
    try:
        current_dir = os.getcwd()
        persistent_directory = os.path.join(current_dir, "embeddings_db", vector_store_name)
        db = Chroma(persist_directory=persistent_directory,
                embedding_function=embeddings)

        # Retrieve relevant documents based on the query
        retriever = db.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )
        relevant_docs = retriever.invoke(query)
        print(relevant_docs)
        # Display the relevant results with metadata
        print("\n--- Relevant Documents ---")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"Document {i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")
        response = Response(200,"Successfully Retrieved from Vector Store",relevant_docs)
        return response
    except:
        print("Unexpected error occured while retrieving data")
        response = Response(500,"Unexpected Error",{})


def chatgptPlusRagRetriever(query,vector_store_name,search_type,search_kwargs,llmModel):
    try:
        current_dir = os.getcwd()
        persistent_directory = os.path.join(current_dir, "embeddings_db", vector_store_name)
        db = Chroma(persist_directory=persistent_directory,
                embedding_function=embeddings)

        # Retrieve relevant documents based on the query
        retriever = db.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )
        relevant_docs = retriever.invoke(query)
        print(relevant_docs)
        # Display the relevant results with metadata
        print("\n--- Relevant Documents ---")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"Document {i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")
        combined_input = (
            "Here are some documents that might help answer the question: "
            + query
            + "\n\nRelevant Documents:\n"
            + "\n\n".join([doc.page_content for doc in relevant_docs])
        )
        model = getLLMFromModelName(llmModel)
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=combined_input),
        ]
        # Invoke the model with the combined input
        result = model.invoke(messages)
        print("\n--- Model Response ---")
        print(result)
        response = Response(200,"Successfully Retrieved response from ChatGPT",result)
        return response
    except:
        print("Unexpected error occured while retrieving data")
        response = Response(500,"Unexpected Error",{})
        return response
