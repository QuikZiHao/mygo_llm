from src.llm_process.utils.load_model import load_model
from src.llm_process.utils.load_vectordb import load_vectordb
from langchain.prompts.chat import ChatPromptTemplate
from src.llm_process.utils.convert_jinjia import get_systemprompt_template
from langchain.schema import HumanMessage, SystemMessage
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from jinja2 import Template
from typing import List
import re


class LLMWrapper():
    def __init__(self):
        self.system_prompt_template:Template = get_systemprompt_template()
        self.llm:ChatOpenAI = load_model()
        self.vector_db: PGVector =  load_vectordb()
        self.retriever = self.vector_db.as_retriever()

    def get_speechlist(self, query:str)-> List[str]:
        retrieved_documents = self.retriever.invoke(query)
        speech_list = []
        for doc in retrieved_documents:
            speech_list.append(doc.page_content)
        speech_list = self.get_speech(speech_list)
        return speech_list
    
    def predict(self, prompt: ChatPromptTemplate) -> str:
        response = self.llm.predict_messages(prompt.messages)
        return response.content
    
    def get_speech(self, speechs_list: List[str]) -> List[str]:
        results = []
        pattern = r"<(.*?)>(.*?)</\1>"
        for line in speechs_list:
            matches = re.findall(pattern, line)
            for _ ,content in matches:
                results.append(content.strip())
        return results
    
    def speak(self, query:str) :
        speech_list = self.get_speechlist(query=query)
        system_prompts = self.system_prompt_template.render(speech_list=speech_list)
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompts),
            HumanMessage(content=query)
            ])
        while(True):
            answer = self.predict(prompt)
            try:
                if answer.split(': ')[1].strip() in speech_list:
                    break
            except:
                continue
            print(f"{answer} - reply no fulfill the condition... try again")
        return answer, speech_list
     
    



