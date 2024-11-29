import json
import os
from openai import OpenAI
from pathlib import Path


class RealtimeChatApp:
    def __init__(self, model="gpt-4o-mini"):
        # Initialize OpenAI client with custom endpoint
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ["GITHUB_TOKEN"],
        )
        self.model = model
        self.memory_file = "selective_memory.json"

        # Create memory file if it doesn't exist
        if not Path(self.memory_file).exists():
            self.save_memory([])

    def load_memory(self):
        """Load chat history from JSON file in real-time"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("\nWarning: Invalid JSON in memory file. Starting with empty history.")
            return []
        except Exception as e:
            print(f"\nError reading memory file: {str(e)}")
            return []

    def save_memory(self, messages):
        """Save chat history to JSON file"""
        with open(self.memory_file, 'w') as f:
            json.dump(messages, f, indent=2)

    def add_message(self, role, content):
        """Add a message to the chat history"""
        messages = self.load_memory()
        messages.append({"role": role, "content": content})
        self.save_memory(messages)

    def chat(self, user_input):
        """Send message to OpenAI API and stream the response"""
        # Add user message to memory
        self.add_message("user", user_input)

        try:
            # Load the latest messages for each API call
            current_messages = self.load_memory()

            # Get streaming response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=current_messages,
                stream=True
            )

            # Storage for complete assistant response
            full_response = ""

            # Process the stream
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    print(content, end='', flush=True)

            # Add assistant's complete response to memory
            self.add_message("assistant", full_response)
            print()  # New line after response

        except Exception as e:
            error_message = f"Error during API call: {str(e)}"
            print(f"\n{error_message}")
            self.add_message("system", error_message)

    def display_chat_history(self):
        """Display current chat history from file"""
        messages = self.load_memory()
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"]
            print(f"\n{role}: {content}")

    def get_message_count(self):
        """Get current number of messages in chat history"""
        messages = self.load_memory()
        return len(messages)


def main():
    # Initialize chat app
    chat_app = RealtimeChatApp()

    print("Realtime Chat App! (Commands: 'exit', 'history', 'count')")
    print("You can modify selective_memory.json at any time to see changes in real-time")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'history':
                chat_app.display_chat_history()
            elif user_input.lower() == 'count':
                count = chat_app.get_message_count()
                print(f"\nCurrent message count: {count}")
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
