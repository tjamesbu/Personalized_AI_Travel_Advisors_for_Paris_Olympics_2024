##AI Travel Advisor - Omdena Paris Chapter
##Authors
##








####################################################################################################
#Importing dependencies
import os
import pathlib
import langchain





import streamlit as st
#from src

####################################################################################################



# Function to configure Google API
def configure_google_api():
    st.sidebar.subheader("Google API Configuration")
    api_key = st.sidebar.text_input("Enter Google API Key")
    # Additional AI advisor funtion import here
    return api_key

# Function to configure OpenAI API
def configure_openai_api():
    st.sidebar.subheader("OpenAI API Configuration")
    api_key = st.sidebar.text_input("Enter OpenAI API Key")
    model = st.sidebar.selectbox("Select Model", ["GPT-3.5", "GPT-4"])
    # Additional AI advisor funtion import here
    return api_key, model

# Function to configure Groq API
def configure_groq_api():
    st.sidebar.subheader("Groq API Configuration")
    api_key = st.sidebar.text_input("Enter Groq API Key")
    # Additional AI advisor funtion import here
    return api_key

# Main function to run the application
def main():
    st.title("AITravel Advisor")
    
    ####################################################################################################
    #Pages setup using st.pages (new method)
    ####################################################################################################
    
    # Ask user to select API
    st.sidebar.header("Select API")
    api_choice = st.sidebar.selectbox("Choose an API", ["Google API", "OpenAI API", "Groq API"])
    
    # Run the appropriate configuration function based on the user's choice
    if api_choice == "Google API":
        google_api_key = configure_google_api()
        st.write("Configured Google API with key:", google_api_key)
        # Continue with the rest of the application using Google API

    elif api_choice == "OpenAI API":
        openai_api_key, openai_model = configure_openai_api()
        st.write("Configured OpenAI API with key:", openai_api_key, "and model:", openai_model)
        # Continue with the rest of the application using OpenAI API

    elif api_choice == "Groq API":
        groq_api_key = configure_groq_api()
        st.write("Configured Groq API with key:", groq_api_key)
        # Continue with the rest of the application using Groq API
    
    # Here you can add the rest of your application logic
    st.write("This is where the main application functionality will go.")
    
    
    
    
    ##########################################################################
    #Additional
    
    
    
    ###########################################################################

if __name__ == "__main__":
    main()
