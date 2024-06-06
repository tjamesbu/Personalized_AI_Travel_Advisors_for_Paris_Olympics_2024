import streamlit as st
from bot import Bot

if 'bot' not in st.session_state:
    st.session_state.bot = Bot()

st.title('Paris Travel Assistant')

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# initial_msg
initial_msg = st.session_state.bot.get_welcome_message()
# Display assistant response in chat message container
with st.chat_message('assistant'):
    st.markdown(initial_msg)
# Add assistant response to chat history
st.session_state.messages.append({'role': 'assistant', 'content': initial_msg})

# React to user input
if prompt := st.chat_input('Ask me your question about Paris.'):
    # Display user message in chat message container
    st.chat_message('user').markdown(f'User: {prompt}')
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    bot_reply = st.session_state.bot.chat(prompt)
    response = f'Bot: {bot_reply}'
    # Display assistant response in chat message container
    with st.chat_message('assistant'):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({'role': 'assistant', 'content': response})