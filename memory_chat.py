import json
import os
from openai import OpenAI
from pathlib import Path


class ChatApp:
    def __init__(self, model="gpt-4o-mini"):
        # Initialize OpenAI client with custom endpoint
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ["GITHUB_TOKEN"],
        )
        self.model = model
        self.memory_file = "chat_memory.json"
        self.messages = self.load_memory()

    def load_memory(self):
        """Load chat history from JSON file"""
        if Path(self.memory_file).exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return []

    def save_memory(self):
        """Save chat history to JSON file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.messages, f, indent=2)

    def add_message(self, role, content):
        """Add a message to the chat history"""
        self.messages.append({"role": role, "content": content})
        self.save_memory()

    def chat(self, user_input):
        """Send message to OpenAI API and stream the response"""
        # Add user message to memory
        self.add_message("user", user_input)

        try:
            # Get streaming response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )

            # Storage for complete assistant response
            full_response = ""

            # Process the stream
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # Print without newline for streaming effect
                    print(content, end='', flush=True)

            # Add assistant's complete response to memory
            self.add_message("assistant", full_response)
            print()  # New line after response

        except Exception as e:
            error_message = f"Error during API call: {str(e)}"
            print(f"\n{error_message}")
            self.add_message("system", error_message)

    def display_chat_history(self):
        """Display all messages in chat history"""
        for msg in self.messages:
            role = msg["role"].upper()
            content = msg["content"]
            print(f"\n{role}: {content}")


def main():
    # Initialize chat app
    chat_app = ChatApp()

    print("Welcome to the Chat App! (Type 'exit' to quit, 'history' to see chat history)")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'history':
                chat_app.display_chat_history()
            elif user_input:
                print("\nAssistant: ", end='')
                chat_app.chat(user_input)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
