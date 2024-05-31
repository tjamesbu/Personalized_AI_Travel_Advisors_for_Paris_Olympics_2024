from llama_index.llms.groq import Groq
import gradio as gr
from gradio_calendar import Calendar
import time
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the API keys from the environment variables
api_key = os.getenv('GROQ_API_KEY')

# Initialize the Groq LLM with your API key
llm = Groq(model="llama3-70b-8192", api_key=api_key)

# Initialize the conversation history and last saved conversation
conversation_history = []

def chat_with_llm(user_input, origin, destinations, start_date, end_date, conversation_html):
    global conversation_history

    start_time = time.time()
    llm_response = ""
    try:
        # Include conversation history and travel details in the next query
        full_conversation = "\n".join([f"**{speaker}:** {message}" for speaker, message in conversation_history])
        travel_details = f"Start destination: {origin}, Destinations: {destinations}, Dates: {start_date} to {end_date}"
        full_query = f"{full_conversation}\n\n**User:** {user_input}\n\n{travel_details}"

        response = llm.stream_complete(full_query)
        for r in response:
            llm_response += r.delta
    except Exception as e:
        llm_response = f"Failed to get response from GROQ. Error: {e}"
    response_time = time.time() - start_time
    print(f"Response time: {response_time} seconds")

    # Update the conversation history
    conversation_history.append(("User", user_input))
    conversation_history.append(("Bot", llm_response))

    # Markdown formatting for chat bubbles
    conversation_markdown = "\n\n".join([f"**{speaker}:** {message}" for speaker, message in conversation_history])

    return conversation_markdown, ""

def reset_conversation(conversation_html):
    global conversation_history

    # Save the current conversation before resetting
    last_conversation = conversation_history.copy()

    # Clear the current conversation history
    conversation_history = []

    # Display last saved conversation
    last_conversation_markdown = "\n\n".join([f"**{speaker}:** {message}" for speaker, message in last_conversation])

    return "", last_conversation_markdown

# Get absolute path of image file
image_path = 'paris-screenshot.png'  # Replace with your image file path
absolute_path = os.path.abspath(image_path)

css = """
.gradio-container {
    background: url('file=paris-screenshot.png');
    background-size: cover;
}
"""

with gr.Blocks(css=css) as app:
    gr.HTML("<h1 style='text-align: center; color: #0033A0;'>Paris Trip Advisor</h1>", elem_classes="background")

    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(label="Your Question", elem_id="user-input")
            origin_input = gr.Textbox(label="Type your Origin City (City, State, Country)", placeholder="Type city name...", elem_id="origin-input")
            destinations_input = gr.Textbox(label="Type your Destination Cities (separated by commas)", placeholder="Type city names...", elem_id="destinations-input")
            start_date = Calendar(type="datetime", label="Start Date (mm/dd/yyyy)", elem_id="start-date")
            end_date = Calendar(type="datetime", label="End Date (mm/dd/yyyy)", elem_id="end-date")
            submit_button = gr.Button("Ask", elem_id="submit-button")
            reset_button = gr.Button("Start Fresh Conversation", elem_id="reset-button")

        with gr.Column(scale=2):
            conversation_html = gr.Markdown(value='', elem_id="conversation-html")
            last_conversation_html = gr.Markdown(value='', elem_id="last-conversation-html")

    submit_button.click(
        chat_with_llm,
        inputs=[user_input, origin_input, destinations_input, start_date, end_date, conversation_html],
        outputs=[conversation_html, user_input]
    )

    reset_button.click(
        reset_conversation,
        inputs=[conversation_html],
        outputs=[conversation_html, last_conversation_html]
    )

app.launch(debug=True, allowed_paths=[absolute_path])