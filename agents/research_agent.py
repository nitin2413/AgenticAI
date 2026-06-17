from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tools.web_search import web_search
from config.settings import settings

def run_research_agent(query):
    try:
        model = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model = settings.OPENAI_MODEL,
            base_url=settings.BASE_URL,
            temperature=0,
            max_tokens=2048

        )

        web_search_findings = web_search.run(query)
        prompt = ChatPromptTemplate.from_template("""
            You are a research assistant. Using the web search results below, provide a clear and concise summary.
            Only use information present in the search results.
            If sources or URLs are present in the results, mention them.
            If no sources are visible, do not make them up.
            Question : {question}
            WEB_finding: {web_search}  
        """)
        chain = prompt|model|StrOutputParser()
        return chain.invoke({"web_search":web_search_findings , "question":query})
    except Exception as e:
        return f"Error occurred while running search agent {e}"