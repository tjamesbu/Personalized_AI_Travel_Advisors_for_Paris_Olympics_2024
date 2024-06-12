from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import re
import json
from dotenv import load_dotenv
import textwrap
from websearch_crew import WebSearchCrew
from paris_advisor import ParisAdvisor

load_dotenv()

gpt_llm = ChatOpenAI(model='gpt-4o', temperature=0.1)
advisor = ParisAdvisor()

class Bot:
    def get_welcome_message(self):
        message = '''
        Welcome to your personal Paris assistant! I'm here to help you make the most of your visit. Whether you're looking for hidden gems, the best restaurants, public transport tips, or a sightseeing itinerary, I've got you covered.

        Need recommendations for unique spots, great dining, or must-see attractions? Seeking advice on getting around efficiently? Experiencing cultural surprises or feeling a bit overwhelmed? I'm here to assist you every step of the way. Let's explore Paris together! How can I help you today?
        '''
        return textwrap.dedent(message)


    def is_valid_json(self, json_string):
        try:
            json.loads(json_string)
        except json.JSONDecodeError:
            return False
        return True


    def remove_json_from_text(self, text):
        # Define the regular expression pattern to match potential JSON objects
        json_pattern = re.compile(r'\{.*?\}', re.DOTALL)        
        # Find all matches of potential JSON objects
        matches = json_pattern.findall(text)        
        # Iterate over each match
        for match in matches:
            try:
                # Try to load the match as JSON
                json.loads(match)
                # If successful, replace the match with an empty string
                text = text.replace(match, '').strip()
            except ValueError:
                # If not a valid JSON, skip it
                continue        
        return text


    def get_prompt_template(self):
        prompt_file = open('prompt_template.txt', 'r')
        prompt_content = prompt_file.read()
        return prompt_content.strip()



    def create_csv_rag_chain(self, csv_filename):
        embedding_function = OpenAIEmbeddings()

        loader = CSVLoader(csv_filename)
        documents = loader.load()

        db = Chroma.from_documents(documents, embedding_function)
        retriever = db.as_retriever()

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        model = ChatOpenAI()
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        return chain



    def create_chain(self):
        template = self.get_prompt_template()
        prompt = PromptTemplate(input_variables=["history", "input"], template=template)
        #print(template)
        memory = ConversationBufferWindowMemory(memory_key="history", k=6, return_only_outputs=True)
        chain = ConversationChain(llm=gpt_llm, memory=memory, prompt=prompt, verbose=False)
        return chain, memory

    
    def inject_memory(self, input, output):
        self.memory.save_context({"input": input}, {"output": output})

    
    def chat(self, user_message):
        if advisor.is_session_in_progress():
            advisor.save_answer(user_message)
            if advisor.has_more_questions():
                advisor_response = advisor.get_next_question()
            else:
                advisor_response = advisor.get_recommendation()
            return advisor_response
        else:
            llm_response = self.chain.predict(input=user_message)
            if self.is_valid_json(llm_response):
                data = json.loads(llm_response)
                if data["category"] == 'cultural_shock':
                    advisor.start_session()
                    llm_response = advisor.get_next_question()
                    self.inject_memory(user_message, llm_response)
                    return llm_response
                elif data["category"] == 'restaurant':
                    restaurant_chain=self.create_csv_rag_chain('restaurants.csv')
                    rag_input = f'{data["request"]}'
                    rag_response = restaurant_chain.invoke(rag_input)
                    # Inject the RAG response to converstaion memory
                    self.inject_memory(rag_input, rag_response)
                    return rag_response
                else:
                    crew = WebSearchCrew(data["request"])
                    websearch_response = crew.kickoff()
                    self.inject_memory(data["request"], websearch_response)
                    return websearch_response
            else:
                return self.remove_json_from_text(llm_response)
    
    
    def __init__(self) -> None:
        self.chain, self.memory = self.create_chain()



def main():
    mybot = Bot()
    print('\n\nAI: ' + mybot.get_welcome_message())
    while True:
        res = mybot.chat(input('\n\nHuman: '))
        print(f'AI: {res}')
     


if __name__ == '__main__':
    main()