import openai
import pandas as pd
import time
import os
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser



GOOGLE_API_KEY = ''


parser = StrOutputParser()
prompt1 = ChatPromptTemplate.from_template(
    "Translate the following poem from Nepalese into English delimited by backticks:```{poem}```"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key = GOOGLE_API_KEY
    
)

chain1 = prompt1 | llm | StrOutputParser()


input_file = 'nepali_poems.csv' 
output_file = './data/processed/translated_poems.csv'


df = pd.read_csv(input_file)


translated_poems = []


for index, row in df.iterrows():
    title = row['Title']
    poem = row['Content']
    
    answer = chain1.invoke({"poem": poem})
    
    print(answer)
    

    time.sleep(10)
    

    translated_poems.append({"Title": title, "Content": answer})


translated_df = pd.DataFrame(translated_poems)


translated_df.to_csv(output_file, index=False)
