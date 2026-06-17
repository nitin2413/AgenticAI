from langchain_openai import ChatOpenAI
from config.settings import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import get_retriever

def run_rag_agent(query , top_k=4):
    try:
        model = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.BASE_URL,
            temperature=0,
            max_tokens=2048
        )

        def format_chunks(chunks):
            return "\n\n".join(chunk.page_content for chunk in chunks)
        retriever = get_retriever(top_k=top_k)
        context = format_chunks(retriever.invoke(query))

        prompt_template = ChatPromptTemplate.from_template("""
            Use the following context to answer the question.
            If the answer is not in the context, say "Insufficient context".
            
            Context : {context}
            Question : {question}
        """
        )

        chain = prompt_template | model | StrOutputParser()
        return chain.invoke({"context": context , "question": query})
    except Exception as e:
        return f"Error occurred while running rag agent {e}"

