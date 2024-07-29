import google.generativeai as genai
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from docx import Document
import requests

load_dotenv()
os.environ["GRPC_VERBOSITY"] = "ERROR"  # Or "FATAL" to suppress more logs

# Set up the AI model with a special key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {"temperature": 1.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

# Choose the AI model we want to use
model = genai.GenerativeModel('gemini-pro')

# This function reads PDF files
def read_pdf(file_path):
    try:
        print("Loading PDF file...")
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# This function reads DOCX files
def read_docx(file_path):
    try:
        print("Loading DOCX file...")
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return None
    
    # Function to read text from an online URL
def read_online(url):
    try:
        print("Loading online content...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except Exception as e:
        print("Error reading online content:", e)
        return None

# This function gets the text we want to summarize
def get_input():
    print("Welcome to BRIEF IT Article Summarizer")
    choice = input("Choose input method (type/file/url) [t/f/u]: ").lower()
    if choice == 't':
        print("\n" + "-" * 40)
        return input("Enter your text: ")
    elif choice == 'f':
        file_path = input("Enter the path to your file: ").strip().strip('"').strip("'")
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.pdf':
            return read_pdf(file_path)
        elif file_extension.lower() == '.docx':
            return read_docx(file_path)
        else:
            try:
                print("Loading file...")
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except Exception as e:
                print("Error reading file:", e)
                return None
    elif choice == 'u':
        url = input("Enter the URL: ").strip()
        return read_online(url)
    else:
        print("Invalid choice.")
        return None

# This function asks the AI to summarize the text
def summarize_text(text, length= 'summary_type'):
    try:
        print("Generating summary....(Take a Few seconds)")
        response = model.generate_content(f"Summarize the following text in a {length} format: {text}")
        return response.text
    except Exception as e:
        print(f"Error in summarization: {e}")
        return None

# This is the main function that runs everything
def main():
    while True:
        text = get_input()
        if text:
            print("\n" + "-" * 40)
            summary_type = input("Choose summarization type (short/long) [s/l]: ").lower()
            summary_length = 'short' if summary_type == 's' else 'long'
            summary = summarize_text(text, summary_length)
            if summary:
                print("\n" + "-" * 40)
                print("Start of Summary:\n")
                print(summary)
                print("\nEnd of Summary")
                print("-" * 40)
                
                save = input("Save summary to file? (y/n): ").lower()
                if save == 'y':
                    filename = input("Enter filename to save (without extension): ")
                    filename = os.path.splitext(filename)[0]  # Remove any extension if provided
                    filename += '.txt'  # Ensure the file is saved as a .txt
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(summary)
                    print(f"Summary saved to {filename}")
        else:
            print("No valid input provided.")

        # Ask if the user wants to continue or exit
        continue_choice = input("Do you want to summarize another text? (y/n): ").lower()
        if continue_choice != 'y':
            print("Thanks for Using BRIEF IT.")
            break

# Run the main function
if __name__ == "__main__":
    main()
