import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # This check ensures the key is loaded before proceeding
    raise ValueError("GEMINI_API_KEY not found in environment variables. Check your .env file.")

# Initialize the Gemini client using the loaded API key variable
client = genai.Client(api_key=api_key)

# Select the model you want to use
model_name = "gemini-2.5-flash"

# Start a chat session
chat = client.chats.create(model=model_name)

print(f"Chatbot initialized using {model_name}. Type 'exit' to end the conversation.")
print("-" * 50)


# --- Main Chat Loop Section ---

while True:
    try:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
            
        # Send the user's message and use the dedicated STREAMING method
        print("Chatbot: ", end="", flush=True)
        
        # FIX: Use send_message_stream() instead of send_message(..., stream=True)
        response_stream = chat.send_message_stream(user_input)
        
        # Iterate over the response parts (chunks) and print them immediately
        for chunk in response_stream:
            # We check for chunk.text to avoid errors on non-text chunks
            if chunk.text:
                print(chunk.text, end="", flush=True)
                
        print() # Add a newline after the full response is printed
        print("-" * 50) # Separator for next turn

    except APIError as e:
        # Catch specific API errors (like rate limits or invalid requests)
        print(f"\n[API Error] An error occurred while communicating with Gemini: {e}")
        print("-" * 50)
    except Exception as e:
        # Catch other unexpected errors
        print(f"\n[Fatal Error] An unexpected error occurred: {e}")
        print("-" * 50)
        break # Break the loop on a critical error