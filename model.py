from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_model():
    llm = GoogleGenerativeAI(
        model=os.getenv("MODEL_NAME"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1,
    )
    return llm
