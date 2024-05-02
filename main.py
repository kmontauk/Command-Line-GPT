########################################################################################################################
# This is a very basic and simple implementation of a script that interfaces with the OpenAI API. It enables one to    #
# easily prevent the wasting of tokens when making API calls to GPT-3.5 and 4 as it will always be asking as if you are#
# beginning a new chat. I did this because I am too lazy to start a new chat on BetterGPT.chat every time I need to    #
# make an API call, which ends up costing me money by way of sending the AI more tokens. Planned features include      #
# holding the chat history in memory, optional ability to write those saved chats to disk, continue the file where it  #
# left off, and finally, to integrate the tool into my portfolio. - D. L. Devito 2024                                  #
########################################################################################################################

from openai import OpenAI
import json


#import config

# NEVER FORGET to delete this before commiting
my_key = ""  # This is your API key from OpenAI. You can get it from the dashboard.
client = OpenAI(api_key=my_key)

chat_history = []

# funky() is a function that takes a prompt and returns a response from the GPT-3.5 API.
def funky(prompt, model="gpt-4-turbo-2024-04-09", role=0, content=0):

    response = client.chat.completions.create(
        # Use the cheapest model for testing...
        model="gpt-3.5-turbo",
        messages=[
            # The first message is always by the system, and the second is always by the user. The "role" is really the content we want to initialize the API with.
            {
                "role": "system", "content": roles_dict[role_key]

            },
            {
                "role": "user", "content": prompt
            }
        ]
    )
    return response

def exit_and_save():
    save_to_disk = input("Would you like to save the chat history to disk? (y/n)")
    save_to_disk = save_to_disk.lower()
    if save_to_disk == "y":
        with open("chat_history.json", "w") as chat_file:
            json.dump(chat_history, chat_file)



# main() handles user input of custom roles and content, prints the response to the console.
def main():
    global roles_dict
    global role_key

    # Load the dictionary from disk.
    with open("my_dict_file.json", "r") as read_file:
        roles_dict = json.load(read_file)

    print("Welcome to my command-line GPT-API Interface! Type \"exit\" at any time to exit the program.")

    # Ask the user if they want to use a custom role.
    print("The default system role is \"Short and Sweet\". This is the role that the AI will assume when it begins a new chat.")
    print("If you want it to assume a custom role, enter a new key/value pair as a comma separated list, or select from a list of existing roles (Found in my_dict_file.json).")
    custom_role = input()
    if input == "exit":
        exit(0)
    role = custom_role.split(",", 1)

    # If the user wants to use a custom role, this will be our "content" for the System role in the API call.  
    if len(role) > 1:
        role[1] = role[1].strip()
        role[0] = role[0].strip()
        roles_dict[role[0]] = role[1]
        role_key = role[0] # This is what will be used in interactions with the API to reference the role.

        # If the user wants to save the role to disk, this block does this.
        add_to_dict = input("Do you want to add this role to the permanent dictionary? (y/n)")
        if add_to_dict == "exit":
            exit(0)
        add_to_dict = add_to_dict.lower()
        if add_to_dict == "y":
            roles_dict[role[0]] = role[1]
            with open("my_dict_file.json", "w") as my_file:
                json.dump(roles_dict, my_file)
    else:
        # Catch if user entered an existing role and use that. Otherwise, use SaS by default. 
        if role[0] in roles_dict:
            role_key = role[0]
        else:
            print("Using default role \"SaS\" for the system role.")
            role_key = "SaS"
        
    model = input("Using GPT-4-turbo-2024-04-09 by default, but if you want to use gpt-3.5 instead, enter \"3.5\" now.")

    # Main loop for the chat.
    while(True):
        to_prompt = input("Prompt: \n")
        if to_prompt == "exit":
            exit_and_save()
        response = funky(to_prompt)
        #  Print the responses to the console.
        for i in range(0, len(response.choices)):
            chat_history.append(response.choices[i].message.content)
            print(f"Response (#{i + 1} / {len(response.choices)}): {response.choices[i].message.content}")
        

if __name__ == '__main__':
    main()


# Lets make this! this sounds fun. Make two ChatGPTs talk to each other! Eventually, I think I'd love to scale a project
# up with selenium to parse the website for responses to user prompts. It wouldn't be that hard to do, and it's
# an easy little project I could manage that could see some real world usage, especially if I bought GPT4.
def funkier():
    conversation = {}


