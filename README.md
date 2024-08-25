# AI Dietitian Assistant by Curelink  
   
## Overview  
The AI Dietitian Assistant is a AI application that uses Azure's OpenAI to provide personalized dietary advice and feedback to patients based on their individual health conditions and diet plans. The application uses Streamlit to provide an interactive user interface.  
   
## Folder Structure  
```  
Curelink_Assignment/    
│    
├── diet_chart_pdfs/         # Directory consists of diet chart pdf files  
├── main.py                  # Main python file to run the application    
├── app_secrets.py           # Azure openAI Credentials    
├── chat_completion.py       # File to request LLM for completion  
├── diet_chart.py            # file to get diet chart and specific context    
├── output.json              # Generated response output file    
├── prompt.py                # Prompt for LLM    
├── queries.json             # Dataset file    
│         
├── requirements             # requirements file  
│    
└── README.md    
```  
   
## Installation & Usage  
   
Clone the repository and navigate to the cloned directory.  
```bash  
git clone https://github.com/Vikash-2020/Curelink_Assignment.git  
cd Curelink_Assignment  
```  
   
Install the required packages.  
```bash  
pip install -r requirements.txt  
```  
   
Run the application.  
```bash  
streamlit run main.py  
```  
You can access the app in your web browser at `localhost:8501`.  
   
## Features  
   
* Personalized dietary advice based on the user's health profile, current diet plan, and any additional notes.  
* Evaluation of the user's meals and check for compliance based on their specific diet plan.  
* Generation of all responses and creation of an `output.json` file.  
* Capability to continue chat conversations.  
   
## Deployed App  
   
The app is deployed using Streamlit and can be accessed [curelink-ai-dietitian-assistant](https://curelink-ai-dietitian-assistant.streamlit.app/).  

## App Interface

![image](https://github.com/user-attachments/assets/3fd3f440-bc41-40e2-acff-f3bfa598ff25)

   
## Acknowledgements  
   
This project uses Azure's OpenAI for generating responses and Streamlit for creating the user interface.  
   
## Disclaimer  
   
This app is a demonstration of AI capabilities and should not replace professional medical advice. Always consult with a healthcare professional.  
