# Importing the necessary Python libraries
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

# Establishing a bit of regex to catch social security numbers
ssn_regex = r'\b(?!000)(?!666)(?!9\d{2})\d{3}[-]?(?!00)\d{2}[-]?(?!0000)\d{4}\b'


## SCRIPT INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print('Welcome to my ChatGPT Python script! Enter a prompt to begin the conversation.')

    user_prompt = input('What would you like to ask?\n')
    print(user_prompt)

    next_choice = [
        inquirer.List(
            'selected_choice',
            message = 'Would you like to continue the conversation?',
            choices = ['Yes', 'Start New Conversation', 'End Program']
        )
    ]

    selected_choice = inquirer.prompt(next_choice)

    print(selected_choice['selected_choice'])