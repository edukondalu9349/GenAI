import os
import json
import  pandas as pd
import traceback 

import PyPDF2

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error while reading pdf file")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("unsupported file format use pdf or text supported")
    

def get_table_data(quiz_str):
    try:
        quiz = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz.items():
            mcq = value["mcq"]
            options = " | ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                    ]
                )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    
    except Exception as e:
        raise Exception("quiz str is not properly send")


