import re
import PyPDF2
import requests
import os
import json


def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)



def extract_text_from_pdf(pdf_file_path):
    # Open the PDF file in binary mode
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        
        # Iterate through all the pages and extract text
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        
    return text


def preprocess_text(raw_text):

    clean_text = re.sub(r'[()]', '', raw_text)
    clean_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean_text)
    clean_text = re.sub(r'(\d+)([A-Z])', r'\1 \2', clean_text)
    time_pattern = re.compile(r'(AM|PM)([^\d\s])')
    clean_text = time_pattern.sub(r'\1\n\2', clean_text)
    return clean_text



def create_diet_chart_dict(preprocessed_text):
    # Split the text into sections by "DAY" or "ADDITIONAL NOTES"
    sections = re.split(r'(DAY \d+ [A-Z]+DAY |ADDITIONAL NOTES)', preprocessed_text)
    diet_chart = {}
    current_day = None
    
    for section in sections:
        # Match and identify "DAY" sections with the weekday name
        day_match = re.match(r'DAY \d+ ([A-Z]+DAY)', section)
        if day_match:
            # Extract the weekday name and format it
            current_day = day_match.group(1).capitalize()
            diet_chart[current_day] = ""
        # Identify the "ADDITIONAL NOTES" section
        elif re.match(r'ADDITIONAL NOTES', section):
            current_day = "AdditionalNotes"
            diet_chart[current_day] = ""
        elif current_day:
            # Append content to the current day
            diet_chart[current_day] += section.strip() + " "
    
    # Clean up any leading or trailing spaces in the values
    diet_chart = {key: value.strip() for key, value in diet_chart.items()}

    return diet_chart


def get_diet_plan_and_additional_notes(id, current_day):
    path = "./diet_chart_pdfs"
    file_name = f"{id}.pdf"

    # combine path and file name  
    file_path = os.path.join(path, file_name) 
    if not os.path.isfile(file_path):
        with open('queries.json', 'r') as json_file:  
            json_object = json.load(json_file)

        pdf_url = json_object[id]['profile_context']['diet_chart_url']
        download_pdf(pdf_url, file_path)

    raw_text = extract_text_from_pdf(file_path)
    clean_text = preprocess_text(raw_text)
    diet_chart = create_diet_chart_dict(clean_text)

    return diet_chart[current_day], diet_chart["AdditionalNotes"]



def get_chat_history(id):
    
    with open('queries.json', 'r') as json_file:  
        json_object = json.load(json_file)

    chat_history = json_object[id]['chat_context']['chat_history']
    latest_query = json_object[id]['latest_query']

    formatted_chat = []  
    previous_role = None  
    content = ""  

    for chat in chat_history:  
        role = "user" if chat["role"] == "User" else "assistant"  
        message = chat["message"]  
        
        if role != previous_role and previous_role is not None:  
            formatted_chat.append({"role": previous_role, "content": content.strip()})  
            content = ""  
        
        content += message + "\n\n"  
        previous_role = role  

    # Append the last chat  
    formatted_chat.append({"role": previous_role, "content": content.strip()}) 
    
    return formatted_chat, latest_query




# pdf_file_path = '42470.pdf'
# raw_text = extract_text_from_pdf(pdf_file_path)


# # print(raw_text)
# # Step 1: Preprocess the raw text
# clean_text = preprocess_text(raw_text)

# # print(clean_text)

# # # Step 2: Create the diet chart dictionary
# diet_chart = create_diet_chart_dict(clean_text)

# # Print the resulting dictionary
# for day, chart in diet_chart.items():
#     print(f"{day}:")
#     print(chart)
#     print("\n" + "-"*50 + "\n")
# pdf_url = json_object[0]['profile_context']['diet_chart_url']
# save_path = f"{json_object[0]['profile_context']['diet_chart']['id']}.pdf"

# download_pdf(pdf_url, save_path)

# # Example usage
# pdf_file_path = '42470.pdf'
# text = extract_text_from_pdf(pdf_file_path)
# print(text)
