# Importing required libraries  
import streamlit as st 
import json
from prompt import prompt2
from datetime import datetime  
from diet_chart import get_diet_plan_and_additional_notes, get_chat_history
from chat_completion import get_completion




# Get current date and time  
current_datetime = datetime.now()  
datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  
current_day = current_datetime.strftime("%A") 


def get_ids():
    # Load your JSON from a file  
    with open('queries.json', 'r') as json_file:  
        json_object = json.load(json_file)
    
    chat_ids = [i for i in range(len(json_object))]
    return chat_ids


def get_context(id):
    # Load your JSON from a file  
    with open('queries.json', 'r') as json_file:  
        json_object = json.load(json_file)
    
    diet_plan, additional_notes = get_diet_plan_and_additional_notes(id, current_day)

    System_message = [{"role": "system", "content": prompt2.format(patient_profile=json_object[id]['profile_context']['patient_profile'], health_program=json_object[id]['profile_context']['program_name'], datetime=datetime_str+" "+current_day, diet_plan=diet_plan, additional_note=additional_notes)}]

    chat_history, latest_query = get_chat_history(id)

    return System_message, chat_history, latest_query



def get_response():
    message  = st.session_state.messages.copy()
    response = get_completion(messages=message)
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    return response.content

    
def start_new_session():
    st.session_state.messages = []
    for message in st.session_state.messages[1:]:
        try:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                # st.markdown(message.content)
        except:
            continue


def generate_all_response():
    with open('queries.json', 'r') as json_file:  
        json_object = json.load(json_file)
    
    response_list = []
    
    for i in range(len(json_object)):
        message = []
        System_message, chat_history, latest_query = get_context(id=i)
        message = System_message + chat_history
        response = get_completion(messages=message)

        response_dict = {"ticket_id": json_object[i]['chat_context']['ticket_id'],
                         "latest_query": json_object[i]['latest_query'],
                         "generated_response": response.content,
                         "ideal_response": json_object[i]['ideal_response']}
        
        response_list.append(response_dict)
    
    # Use json.dump to write the data to a file  
    with open('output.json', 'w') as f:  
        json.dump(response_list, f)
    
    return response_list


def download_json(data):
    json_data = json.dumps(data)
    json_bytes = json_data.encode('utf-8')
    
    return json_bytes




st.title('AI Dietitian Assistant -by Curelink')

# Initializing chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    try:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # st.markdown(message.content)
    except:
        continue


# Defining the layout of the sidebar  
st.sidebar.markdown("## Options")  

# Adding a button in the upper half of the sidebar  
if st.sidebar.button('Generate & Download all response'):
    with st.spinner('Generating Response, Please wait...'):
        response_data = generate_all_response()
    st.sidebar.success("Done!")

    st.sidebar.download_button(
    label="Download output.json",
    data=download_json(response_data),
    file_name="output.json",
    mime='application/json'
)

st.sidebar.markdown("---")

# Adding a dropdown menu in the lower half of the sidebar  
ids = ["None"] + get_ids() # You can replace these with actual IDs  
selected_id = st.sidebar.selectbox('Select ID', ids)  
if selected_id == "None":  
    st.write("## How to Use This App")  
    st.markdown("""  
    This app allows you to generate and download an `output.json` file, and continue chat conversations.   
  
    Here's how you can use it:  
  
    1. **Generate and Download Output.json**: Select the 'Generate & Download all response' option in the sidebar. This will generate all the response, create the `output.json` file and start the download.  
  
    2. **Continue a Chat Conversation**: Select an ID from the dropdown in the sidebar. This will load the chat conversation associated with that ID, and allow you to continue the conversation.  
    """)  


if st.sidebar.button('Submit'):
    if selected_id != "None":

        System_message, chat_history, latest_query = get_context(id=selected_id)
        
        start_new_session()
        st.session_state.messages = System_message + chat_history
        
        get_response()

        # Display chat messages from history on app rerun
        for message in st.session_state.messages[1:]:
            try:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    # st.markdown(message.content)
            except:
                continue

    st.sidebar.success("Context Updated")






if __name__ == "__main__":  
      
    # Accept user input
    if prompt := st.chat_input("Enter your query here."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        answer = get_response()

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
