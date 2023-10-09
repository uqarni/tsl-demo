import streamlit as st
from functions import ideator, secret_message
import json
import os
import sys
from datetime import datetime
from supabase import create_client, Client

#connect to supabase database
urL: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(urL, key)
data, count = supabase.table("bots_dev").select("*").eq("id", "emily").execute()
bot_info = data[1][0]



def main():
    # Create a title for the chat interface
    st.title("FullHarvest Bot (named Emily)")
    st.write("To test, first select some fields then click the button below.")
  

    name = 'Emily'
    booking_link = 'fullharvestbooking.com'
    lead_first_name = st.text_input('Lead First Name', value = 'John')
    lead_type = st.selectbox("lead type",["supplier", "provider"])
    produce_type = st.selectbox("produce type", ["tomatoes", ]
    system_prompt = bot_info['system_prompt']
    initial_text = bot_info['initial_text']
    

    
    if st.button('Click to Start or Restart'):
        #variable inputs


        system_prompt.format(lead_first_name=lead_first_name, booking_link = booking_link, name=name)

        initial_text = initial_text.format(lead_first_name = lead_first_name, name=name)

        st.write(initial_text)


        #clear database to only first two lines
        with open('database.jsonl', 'w') as f:
        # Override database with initial json files
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": initial_text}            
            ]
            f.write(json.dumps(messages[0])+'\n')
            f.write(json.dumps(messages[1])+'\n')



    #initialize messages list and print opening bot message
    #st.write("Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?")

    # Create a text input for the user to enter their message and append it to messages
    userresponse = st.text_input("Enter your message")
    

    # Create a button to submit the user's message
    if st.button("Send"):
        #prep the json
        newline = {"role": "user", "content": userresponse}

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(newline) + '\n')

        #extract messages out to list
        messages = []

        with open('database.jsonl', 'r') as f:
            for line in f:
                json_obj = json.loads(line)
                messages.append(json_obj)

        #generate OpenAI response
        messages, count = ideator(messages)

        #append to database
        with open('database.jsonl', 'a') as f:
                for i in range(count):
                    f.write(json.dumps(messages[-count + i]) + '\n')



        # Display the response in the chat interface
        string = ""

        for message in messages[1:]:
            if 'This is a secret internal thought' not in str(message):
                string = string + message["role"] + ": " + message["content"] + "\n\n"
        st.write(string)

    if day.activation_date == 'no':
        if st.button("Toggle Activation"):
            if day.activation_date == "no":
                day.activation_date = "yes" 
            #extract messages out to list
            messages = []

            with open('database.jsonl', 'r') as f:
                for line in f:
                    json_obj = json.loads(line)
                    messages.append(json_obj)

            # Display the response in the chat interface
            string = ""

            for message in messages[1:]:
                if 'secret internal thought' not in str(message):
                    string = string + message["role"] + ": " + message["content"] + "\n\n"
            st.write(string)

    
    if st.button("Increment Day"):
        increment_variable(day)
        
        if int(day.my_var) <= 7:
            
            newline = secret_message(day.my_var, day.activation_date)
            with open('database.jsonl', 'a') as f:
                f.write(json.dumps(newline) + '\n')
        
            # Your existing code for reading the database, generating responses, and updating the database can remain here
            # extract messages out to list
            messages = []
    
            with open('database.jsonl', 'r') as f:
                for line in f:
                    json_obj = json.loads(line)
                    messages.append(json_obj)
    
            #generate OpenAI response
            messages, count = ideator(messages)
    
            #append to database
            with open('database.jsonl', 'a') as f:
                    for i in range(count):
                        f.write(json.dumps(messages[-count + i]) + '\n')
    
    
    
            # Display the response in the chat interface
            string = ""
    
            for message in messages[1:]:
                if "secret internal thought"  not in str(message):
                    string = string + message["role"] + ": " + message["content"] + "\n\n"
            st.write(string)
        else:
            st.write('Trial ended. Bot will not send messages. Please reset to start again.')

    # At the bottom of your Streamlit layout, you can show the current week
    st.write(f"*Currently in Day:* {day.my_var}")
    st.write(f"*is user activated?* {day.activation_date}")
        

if __name__ == '__main__':
    main()