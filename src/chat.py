# Importing the necessary Python libraries
import os
import re
import yaml
import openai
import inquirer



## API INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
# Loading the API key and organization ID from file (NOT pushed to GitHub)
with open('../keys/openai-keys.yaml') as f:
    keys_yaml = yaml.safe_load(f)

# Applying our API key and organization ID to OpenAI
openai.organization = keys_yaml['ORG_ID']
openai.api_key = keys_yaml['API_KEY']



## HELPER FUNCTIONS
## ---------------------------------------------------------------------------------------------------------------------
def initiate_chat_flow():
    '''
    Initiates a new chat flow

    Inputs:
        - N/A

    Returns:
        - chat_flow (list): A newly initiated chat flow
    '''

    chat_flow = [
        {'role': 'system', 'content': 'You are a classy butler, like Alfred from Batman.'}
    ]

    return chat_flow

def check_sensitive_data(user_prompt):
    '''
    Checks the user's prompt to see if any sensitive information has been pass in via the prompt

    Inputs:
        - user_prompt (str): The user's inputted prompt

    Returns:
        - has_sensitive_data (bool): A boolean value indicating if the prompt contains sensitive data
    '''

    # Establishing a bit of regex to catch social security numbers
    ssn_regex = r'\b(?!000)(?!666)(?!9\d{2})\d{3}[-]?(?!00)\d{2}[-]?(?!0000)\d{4}\b'

    # Checking to see if there is a match based on the regex
    has_sensitive_data = bool(re.search(ssn_regex, user_prompt))

    return has_sensitive_data



def prompt_next_choice():
    '''
    Prompts the user to continue the current conversation, start a new conversation, or end the program

    Inputs:
        - N/A

    Returns:
        - next_action (str): The choice selected by the user
    '''

    # Setting the list of options that the user can select from
    user_choices = [
        inquirer.List(
            'user_choices',
            message = 'Would you like to continue the conversation?',
            choices = ['Yes', 'Start New Conversation', 'End Program']
        )
    ]

    # Retreiving the selected option by the user
    next_action = inquirer.prompt(user_choices)['user_choices']

    return next_action


## SCRIPT INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Printing a welcome statement
    print('Welcome to my ChatGPT Python script! Enter a prompt to begin the conversation.')

    # Starting an initial chat flow
    chat_flow = initiate_chat_flow()

    # Starting a reiterating loop for the prompts
    while True:

        # Retrieving the prompt input from the user
        user_prompt = input('What would you like to ask?\n')

        # Checking the prompt for any sensitive data
        has_sensitive_data = check_sensitive_data(user_prompt)

        # Prompting the user to submit a new prompt without sensitive data if sensitive data is present
        if has_sensitive_data:
            print('Your prompt appears to have sensitive data in the body of the text. Please remove this sensitive data and submit a new prompt.')
            continue

        # Appending the user prompt to the chat flow
        chat_flow.append({'role': 'user', 'content': user_prompt})

        # Obtaining the response from the API
        chat_response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = chat_flow
        )

        # Printing ChatGPT's response back to the user
        print(f"\nChatGPT's response: {chat_response['choices'][0]['message']['content']}\n")

        # Prompting the user if they would like to continue the current chat, start a new one, or end the program
        next_action = prompt_next_choice()

        # Taking the appropriate action based on the user's next desired action
        if next_action == 'Yes':

            # Appending the result of the chat response to the chat flow for continued conversation
            chat_flow.append({'role': 'assistant', 'content': chat_response['choices'][0]['message']['content']})

        elif next_action == 'Start New Conversation':

            # Re-initiating the chat flow
            chat_flow = initiate_chat_flow()

        elif next_action == 'End Program':
            exit(0)