
import os
import json
import  pandas as pd
import traceback # type: ignore
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
# from langchain.callbacks import get_openai_callback

from langchain_community.callbacks import get_openai_callback
import PyPDF2

from src.mcqgenerator.utils import read_file ,get_table_data
from src.mcqgenerator.logger import logging

load_dotenv()

key_openai = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=key_openai,model_name="gpt-3.5-turbo",temperature=0.7)


TEMPLATE = """
Text:{text}
You are an export MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check the all questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as guide \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quize_prompt_template = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE
    
)

quize_chain = LLMChain(llm=llm,prompt=quize_prompt_template,output_key="quiz",verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evlution_prompt = PromptTemplate(input_variables=['subject',"quiz"],template=TEMPLATE2)
review_chian = LLMChain(llm=llm,prompt=quiz_evlution_prompt,output_key="review",verbose=True)

generate_evaluate_chain = SequentialChain(chains=[quize_chain,review_chian],input_variables=["text","number","subject","tone","response_json",'subject'],
                output_variables=["quiz","review"],verbose=True)





