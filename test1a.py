import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.llms import Cohere
from TestEmotionDetector1 import emotion_pred
import time

st.set_page_config(page_title="EmoBot")
COHERE_API_KEY="8KReZCCVi0qqxDPNH2Fze81khJEgzv1orPZdRHTY"

# Sidebar contents
with st.sidebar:
    st.title('EmoBot🤖')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot 
    
    
    ''')
    add_vertical_space(5)
    st.write('Made for better understanding')

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm Emobot, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='Enter Your Questions', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    chatbot = Cohere(cohere_api_key= COHERE_API_KEY, model="command-xlarge-nightly")
    response = chatbot(prompt)
    
    
    return response


## Conditional display of AI generated responses as a function of user provided prompts
j=0


def process_user_input(user_input):
    n1=0
    n2=1
    with response_container:
        if user_input:
            response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response) 
            n1=0

        display_generated_responses1(st.session_state.generated, st.session_state.past,n1)
        if len(st.session_state.past)>1:
            time.sleep(3)
            #b = emotion_pred()
        
            #process_emotion_input(b,st.session_state.generated,st.session_state.past)

def process_emotion_input(b,generated,past):

    if b not in ["Happy","Neutral"]:
        response = generate_response("can you explain "+user_input+" more clearly")
        message("Wait..... I will regenerate")
        n2=3
    else:
        response = generate_response("i am satisfied with your answer")
        n2=2

        past.append(b)
        generated.append(response) 
            
        
    display_generated_responses2(generated, past,n2)
    
    


def display_generated_responses1(generated_responses, past_responses, n):
    i = 0
    message(past_responses[-1], is_user=True, key=str(i) + '_user_' + str(n))
    message(generated_responses[-1], key=str(i) + '_response_' + str(n))

def display_generated_responses2(generated_responses, past_responses, n):
    i = 0
    message(generated_responses[-1], key=str(i) + '_response_' + str(n))
    if n == 3:
        time.sleep(3)
        b1 = emotion_pred()
        process_emotion_input(b1, generated_responses, past_responses)
    

process_user_input(user_input)