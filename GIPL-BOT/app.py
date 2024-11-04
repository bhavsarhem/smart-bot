import os
from dotenv import load_dotenv
import requests
import PyPDF2
from bs4 import BeautifulSoup
import streamlit as st
from groq import Groq
import zlib  # Import zlib for compression

load_dotenv()

# Set your Groq API key
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text.strip()

# Function to fetch content from a website URL
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join([para.get_text() for para in paragraphs])
    except Exception as e:
        return f"Error fetching content: {str(e)}"

# Load knowledge base from multiple PDFs and websites
def load_knowledge_base(pdf_paths, website_urls): #
    knowledge_base = ""
    
    # Extract text from PDFs
    for pdf_path in pdf_paths:
        knowledge_base += extract_text_from_pdf(pdf_path) + " "
    
    # Fetch content from websites
    for url in website_urls:
        knowledge_base += fetch_website_content(url) + " "
    
    return knowledge_base.strip()

# Function to compress data
def compress_data(data):
    return zlib.compress(data.encode('utf-8'))

# Function to decompress data (if needed)
def decompress_data(data):
    return zlib.decompress(data).decode('utf-8')

# Initialize chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define the chatbot's name
chatbot_name = "GIPL Assistant"

# Streamlit UI setup
st.set_page_config(page_title=f"{chatbot_name}", page_icon="img/gipl_header_logo.png")
st.title(f"Welcome to {chatbot_name}!")
st.caption("Ask me anything about our website! ©(https://gipl.in)")

# User input field
user_prompt = st.chat_input("Type your message here...")

# Specify your PDF document paths and website URLs here
pdf_paths = [
    'BoardofDirectors_20240925.pdf',
    'CSRPolicytoBoardofDirectors.pdf',
    'ShriMaheshGohel.pdf'  # Replace with your actual PDF paths
]
website_urls = [
    'https://gipl.in',
    'https://gipl.in/Detail/AwardList',
    # 'https://gipl.in/Content/Assets/BoardofDirectors_20240925.pdf',
    # 'https://gipl.in/Detail/Content/3387' # Replace with your actual website URLs
]

knowledge_base = load_knowledge_base(pdf_paths, website_urls) #

if user_prompt:
    # Display user message in a styled format
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Check for simple greetings and respond accordingly
    simple_greetings = ["hi", "hi!", "hello", "hello!", "hey", "hi there!", "greetings"]
    if user_prompt.lower() in simple_greetings:
        assistant_response = f"Hello! I am {chatbot_name}. How can I assist you today?"
    else:
        # Compress the knowledge base before sending it to the API
        compressed_knowledge_base = compress_data(knowledge_base)

        # Prepare messages for Groq API for more complex queries
        messages = [
            {"role": "system", "content": f"You are an assistant named {chatbot_name} knowledgeable about multiple documents and websites."},
            {"role": "system", "content": f"Knowledge Base: {decompress_data(compressed_knowledge_base)}"},  # Decompress before sending if needed.
            {"role": "user", "content": user_prompt}
        ]
        
        # Generate a response using the Groq API
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
        )
        
        assistant_response = chat_completion.choices[0].message.content

    # Display assistant response in a styled format
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

# Display chat history in a chatbot-like format with improved styling
for chat in st.session_state.chat_history:
    if chat['role'] == 'user':
        st.markdown(
            f"<div style='text-align: right; background-color: #FF6666; border-radius: 10px; padding: 10px; margin: 5px; display: inline-block;'>"
            f"<b>User:</b> {chat['content']}</div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #FFA500; border-radius: 10px; padding: 10px; margin: 5px; display: inline-block;'>"
            f"<b>{chatbot_name}:</b> {chat['content']}</div>",
            unsafe_allow_html=True)

# Add some CSS to style the chat interface (optional)
st.markdown("""
<style>
div.stTextInput {
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)















# import os
# import requests
# import PyPDF2
# from bs4 import BeautifulSoup
# import streamlit as st
# from groq import Groq

# # Set your Groq API key
# GROQ_API_KEY = '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'
# os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# # Initialize the Groq client
# client = Groq(api_key=GROQ_API_KEY)

# # # Function to extract text from a PDF file
# # def extract_text_from_pdf(pdf_path):
# #     text = ""
# #     with open(pdf_path, "rb") as file:
# #         reader = PyPDF2.PdfReader(file)
# #         for page in reader.pages:
# #             text += page.extract_text() + " "
# #     return text.strip()

# # Function to fetch content from a website URL
# def fetch_website_content(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = soup.find_all('p')
#         return ' '.join([para.get_text() for para in paragraphs])
#     except Exception as e:
#         return f"Error fetching content: {str(e)}"

# # Load knowledge base from multiple PDFs and websites
# def load_knowledge_base(website_urls): #pdf_paths,
#     knowledge_base = ""
    
#     # # Extract text from PDFs
#     # for pdf_path in pdf_paths:
#     #     knowledge_base += extract_text_from_pdf(pdf_path) + " "
    
#     # Fetch content from websites
#     for url in website_urls:
#         knowledge_base += fetch_website_content(url) + " "
    
#     return knowledge_base.strip()

# # Initialize chat history if not present
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Define the chatbot's name
# chatbot_name = "GIPL Assistant"

# # Streamlit UI setup
# st.set_page_config(page_title=f"{chatbot_name}", page_icon="img/gipl_header_logo.png")
# st.title(f"Welcome to {chatbot_name}!")
# st.caption("Ask me anything about our website! ©(https://gipl.in)")

# # User input field
# user_prompt = st.chat_input("Type your message here...")

# # Specify your PDF document paths and website URLs here
# # pdf_paths = [
# #     'GIPL-BOT/src/BoardofDirectors_20240925.pdf',
# #     'GIPL-BOT/src/CSRPolicytoBoardofDirectors.pdf',
# #     'GIPL-BOT/src/ShriMaheshGohel.pdf'  # Replace with your actual PDF paths
# # ]
# website_urls = [
#     'https://gipl.in',
#     'https://gipl.in/Detail/AwardList',
#     'https://gipl.in/Detail/Content/3387',
#     'https://gipl.in/Content/Assets/BoardofDirectors_20240925.pdf',
#     # Replace with your actual website URLs
# ]

# knowledge_base = load_knowledge_base(website_urls) #pdf_paths,

# if user_prompt:
#     # Display user message in a styled format
#     st.session_state.chat_history.append({"role": "user", "content": user_prompt})

#     # Check for simple greetings and respond accordingly
#     simple_greetings = ["hi", "hi!", "hello", "hello!", "hey", "hi there!", "greetings"]
#     if user_prompt.lower() in simple_greetings:
#         assistant_response = f"Hello! I am {chatbot_name}. How can I assist you today?"
#     else:
#         # Prepare messages for Groq API for more complex queries
#         messages = [
#             {"role": "system", "content": f"You are an assistant named {chatbot_name} knowledgeable about multiple documents and websites."},
#             {"role": "system", "content": f"Knowledge Base: {knowledge_base}"},
#             {"role": "user", "content": user_prompt}
#         ]
        
#         # Generate a response using the Groq API
#         chat_completion = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=messages,
#         )
        
#         assistant_response = chat_completion.choices[0].message.content

#     # Display assistant response in a styled format
#     st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

# # Display chat history in a chatbot-like format with improved styling
# for chat in st.session_state.chat_history:
#     if chat['role'] == 'user':
#         st.markdown(
#             f"<div style='text-align: right; background-color: #FF6666; border-radius: 10px; padding: 10px; margin: 5px; display: inline-block;'>"
#             f"<b>User:</b> {chat['content']}</div>",
#             unsafe_allow_html=True)
#     else:
#         st.markdown(
#             f"<div style='text-align: left; background-color: #FFA500; border-radius: 10px; padding: 10px; margin: 5px; display: inline-block;'>"
#             f"<b>{chatbot_name}:</b> {chat['content']}</div>",
#             unsafe_allow_html=True)

# # Add some CSS to style the chat interface (optional)
# st.markdown("""
# <style>
# div.stTextInput {
#     margin-bottom: 25px;
# }
# </style>
# """, unsafe_allow_html=True)
