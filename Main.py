# CIT- 95 (Mohle) Spring 2026

# to do:
    # this is where we add chatbot memory

    # This is where we use a localserver like streamlit

    # modify streamlit with HTML to make a nice looking chat bot

# optional?:
    # use langchain framework to read .pdf file

    #use an open source LLm (llsomething) that doesn't cost tokens

import google.generativeai as genai

#user-defined functions go here, before the main() function (is a python coding convention)
def generate_response(user_input):
    try:
        #call the open ai api to generate a response
        completion =genai.ChatCompletion.create(
            #find the model pricing page at open ai and examine your token usage with different models.
            model="gpt-3.5-turbo"
        # (replace with ai actually using)

            messages= [{"role": "system", "content": "Assume the role of a Python teacher, and think step by step. Your name is Skippy Py."},
                   {"role": "user", "content": user_input}]
        )

        response_text = completion["choices"][0]["message"]["content"]
        return response_text

    except Exception as e:
        # print an error message if the API call fails
        print("Error generating response:", e)
        return "I'm sorry, I couldn't generate a response."


def main():
    # my API key from Gemini
    # i think I did this correctly but not sure

    genai.configure(api_key="AIzaSyCj0C1oH5keToqOv0pVmbw-XiKnZReTMrw")

    print("\nWelcome to the Python Study Bot! Type 'quit' to exit.\n")

    # this loop will run until the break after user input 'quit'
    while True:
        #get user input
        user_input = input ("Python student question: ")

        # check if user wants to quit the chatbot
        if user_input == "quit":
            print("Exiting Python Study Bot.")
            break

        # Gererate a response using OpenAI's GPT-3.5-turbo (Gemini?)
        response = generate_response(user_input)

        #print the response
        print("Python Study Bot: ", response)

if __name__ == '__main__':
    main()