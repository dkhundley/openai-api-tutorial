# Importing the necessary Python libraries
import yaml
import openai
import gradio as gr



## OPENAI CONNECTION
## ---------------------------------------------------------------------------------------------------------------------
# Loading the API key and organization ID from file (NOT pushed to GitHub)
with open('../keys/openai-keys.yaml') as f:
    keys_yaml = yaml.safe_load(f)

# Applying our API key and organization ID to OpenAI
openai.organization = keys_yaml['ORG_ID']
openai.api_key = keys_yaml['API_KEY']

# Setting the OpenAI model selection (may adjust later to be user changeable for those lucky folks out there with GPT-4 access ;) )
openai_model = 'gpt-3.5-turbo'



## PROMPT ENGINEERING
## ---------------------------------------------------------------------------------------------------------------------
# Setting options to select from for philosophers
PHILOSOPHERS = [
    'Alan Watts',
    'Anne Lamott',
    'Brene Brown',
    'Duncan Trussell',
    'Eckhart Tolle',
    'Joseph Campbell',
    'Pete Holmes',
    'Ram Dass',
    'Socrates'
]

# Setting a list of comedians, just to be able to get better results from the model
COMEDIANS = [
    'Duncan Trussell',
    'Pete Holmes'
]



## GRADIO HELPER FUNCTIONS
## ---------------------------------------------------------------------------------------------------------------------
def converse_amongst_philosophers(philosopher_1, philosopher_2, convo_topic, convo_chatbot, rounds = 4):
    '''
    Simulates a conversation between two phiosopher using Generative AI

    Inputs:
        - philosopher_1 (str): The name of the first philosopher, who will begin the conversation
        - philosopher_2 (str): The name of the second philosopher
        - convo_topic (str): The topic of conversation about to take place between the philosophers
        - convo_chatbot (Gradio Chatbot): The chatbot interface that will hold the dialogue betweent the two philosophers
        - rounds (int): The number of rounds of conversation that will take place (default = 4)

    Returns:
        - convo_chatbot (Gradio Chatbot): The chatbot interface that holds the dialogue betweent the two philosophers
    '''

    # Checking if the philosopher is also a comedian
    if philosopher_1 in COMEDIANS:
        philosopher_1 = 'and comedian ' + philosopher_1
    if philosopher_2 in COMEDIANS:
        philosopher_2 = 'and comedian ' + philosopher_2

    # Instantiating chat flows for each respective philosopher
    philosopher_1_chat_flow = []
    philosopher_2_chat_flow = []

    # Prompt engineering the opening from philosopher 1
    philosopher_1_opener_prompt = f'''
    You are philosopher {philosopher_1} and are about to have a conversation with another philosopher, {philosopher_2}.
    The topic of conversation is {convo_topic}.
    You are first to speak.
    Please give your opening as {philosopher_1}
    Do not continue as {philosopher_2}.
    Please keep your opening concise.
    '''

    # Simulating the opening of the dialogue with philsopher 1 kicking things off
    philosopher_1_chat_flow.append({'role': 'user', 'content': philosopher_1_opener_prompt})
    philosopher_1_opener = openai.ChatCompletion.create(
        model = openai_model,
        messages = philosopher_1_chat_flow
    )['choices'][0]['message']['content']
    philosopher_1_chat_flow.append({'role': 'assistant', 'content': philosopher_1_opener})

    # Prompt engineering the opening from philosopher 2
    philosopher_2_opener_prompt = f'''
    You are philosopher {philosopher_2} and are about to have a conversation with another philosopher, {philosopher_1}.
    The topic of conversation is {convo_topic}.
    The other person has opened the conversation with the following:
    "{philosopher_1_opener}"
    Respond back accordingly.
    Do not continue as {philosopher_1}.
    Please keep your response concise.
    '''

    # Simulating the opening response from philosopher 2 on hearing philosopher 1's opening
    philosopher_2_chat_flow.append({'role': 'user', 'content': philosopher_2_opener_prompt})
    philosopher_2_opener = openai.ChatCompletion.create(
        model = openai_model,
        messages = philosopher_2_chat_flow
    )['choices'][0]['message']['content']
    philosopher_2_chat_flow.append({'role': 'assistant', 'content': philosopher_2_opener})

    # Appending the opening interaction to the chatbot
    convo_chatbot.append((philosopher_1_opener, philosopher_2_opener))

    return convo_chatbot



## GRADIO UI LAYOUT & FUNCTIONALITY
## ---------------------------------------------------------------------------------------------------------------------
# Defining the building blocks that represent the form and function of the Gradio UI
with gr.Blocks(title = 'Philosophy Conversation Simulator', theme = 'base') as convo_sim:
    
    # Setting the overall header for the page
    gr.Markdown('''
    # Philosophy Conversation Simulator
    
    This interface allows you to simulate a conversation between two philosophers about whatever you want them to talk about!
    ''')

    # Setting a side-by-side selector for conversators
    with gr.Row():

        with gr.Column():

            # Enabling a dropdown to select the first participant
            philosopher_1 = gr.Dropdown(choices = PHILOSOPHERS, label = 'Philosopher 1', allow_custom_value = True)

        with gr.Column():
            # Enabling a dropdown to select the second participant
            philosopher_2 = gr.Dropdown(choices = PHILOSOPHERS, label = 'Philosopher 2')

    # Creating a freeform textbox allowing the user to submit any topic they would like the participants to converse about
    convo_topic = gr.Textbox(label = 'Please enter an idea for a topic of conversation.',
                             placeholder = 'e.g. Chicago Style Pizza')
    
    # Creating the button to simulate the conversation
    simulate_conversation_button = gr.Button('Simulate Conversation')

    # Instantiating the chatbot interface to hold the back-and-forth of the conversation
    convo_chatbot = gr.Chatbot(label = 'Simulated Conversation')

    # Defining the behavior for when the user clicks the "Simulate Conversation" button
    simulate_conversation_button.click(fn = converse_amongst_philosophers,
                                       inputs = [philosopher_1, philosopher_2, convo_topic, convo_chatbot],
                                       outputs = [convo_chatbot],
                                       queue = False)




## SCRIPT INVOCATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Instantiating the initial chat flow used as a global variable
    chat_flow = []

    # Launching the Gradio UI
    convo_sim.launch()