from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.gmail_tools import fetch_recent_emails
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings

def run_gmail_agent(max_email = 10) -> str:
    try:
        emails = fetch_recent_emails(max_email)

        if not emails:
            return ("No email found in your inbox")

        formatted = "\n\n".join(
            f"Email {i +1}:\nFrom: {email['sender']}\nDate: {email['date']}\nSubject: {email['subject']}\nPreview: {email['snippet']}"
            for i , email in enumerate(emails)
        )

        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            base_url=settings.BASE_URL,
            api_key=settings.OPENAI_API_KEY,
            max_tokens=2048
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an email assistant. Read the provided emails and create a concise summary for each email. "
             "Highlight the main purpose, important details, and any action items. "
             "Return the response in the exact format below:\n\n"
             "Email 1:\n"
             "From: <sender>\n"
             "Date: <date>\n"
             "Subject: <subject>\n"
             "Summary: <2-3 sentence summary>\n"
             "Action Required: <Yes/No and brief reason>\n\n"
             "Repeat the same structure for all emails. "
             "Do not add markdown, bullet points, or extra explanations."
             ),
            ("human", "{query}")
        ])

        chain = prompt | llm | StrOutputParser()

        response = chain.invoke({"query": formatted})
        return response

    except Exception as e:
        return f"Error occurred while running gmail agent {e}"
