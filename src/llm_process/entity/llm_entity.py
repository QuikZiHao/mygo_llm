from src.llm_process.utils.load_model import load_model
from src.llm_process.utils.load_vectordb import load_vectordb
from langchain.prompts.chat import ChatPromptTemplate
from src.llm_process.utils.convert_jinjia import get_systemprompt_template
from src.llm_process.utils.get_img_db import get_image_db
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from PIL import Image
from jinja2 import Template
from typing import List
from ..constants import FRAME_DIR, NOT_FOUND_PATH, LLM_CONFIG
import re
import os


class LLMWrapper():
    def __init__(self):
        self.system_prompt_template:Template = get_systemprompt_template()
        self.llm:ChatOpenAI = load_model()
        self.vector_db: PGVector =  load_vectordb()
        self.retriever = self.vector_db.as_retriever()
        self.img_db = get_image_db()

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
        try_idx = 0
        while(True):
            answer = self.predict(prompt)
            try:
                if self.clean_speech(answer.split('speech: ')[1].strip()) in speech_list:
                    break
            except:
                continue
            
            if try_idx == 5:
                return "not found", Image.open(NOT_FOUND_PATH).convert("RGB")
            try_idx += 1
            prompt.append(AIMessage(content=answer))
            prompt.append(HumanMessage(content="The speech did not include the lines from the show. Please try again using the following format:\nspeech: (The selected line of dialogue)"))
            print(f"{answer.split('speech: ')[1].strip()} - reply no fulfill the condition... try again")
        cursor = self.img_db.cursor()
        search_speech = self.clean_speech(answer.split('speech: ')[1].strip())
        query = f"SELECT * FROM {LLM_CONFIG["img_db"]} WHERE speech = %s;"
        cursor.execute(query, (search_speech,))
        rows = cursor.fetchall()
        if rows:
            image_path = os.path.join(FRAME_DIR, str(rows[0][1]),rows[0][3])
            try:
                image = Image.open(image_path).convert("RGB")
            except:
                answer = "not found"
                image = Image.open(NOT_FOUND_PATH).convert("RGB")
        else:
            print(f"No records found for speech: {search_speech}")
        cursor.close()

        return answer, image
     
    def clean_speech(self, text: str) -> str:
        text = re.sub(r'[^\w\s]', '', text) 
        text = re.sub(r'\n', '', text)
        text = re.sub(r'\s+', '', text)   
        text = text.strip()                 
        return text
    
