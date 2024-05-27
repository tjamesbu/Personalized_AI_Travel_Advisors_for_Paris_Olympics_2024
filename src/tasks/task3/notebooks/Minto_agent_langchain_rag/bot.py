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
import json
from dotenv import load_dotenv

from websearch_crew import WebSearchCrew

load_dotenv()

gpt_llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.1)


def get_welcome_message():
    message = '''Hello! I'm an AI assistant here to help visitors exploring the city of Paris.
    Feel free to let me know how I can assist you.'''
    return message


def is_valid_json(json_string):
    try:
        json.loads(json_string)
    except json.JSONDecodeError:
        return False
    return True



def get_prompt_template():
    prompt_file = open('prompt_template.txt', 'r')
    prompt_content = prompt_file.read()
    return prompt_content.strip()



def create_csv_rag_chain(csv_filename):
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



def create_chain():
    template = get_prompt_template()
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    #print(template)
    memory = ConversationBufferWindowMemory(memory_key="history", k=6, return_only_outputs=True)
    chain = ConversationChain(llm=gpt_llm, memory=memory, prompt=prompt, verbose=False)
    return chain, memory



def main():
    chain, memory = create_chain()
    print('\n\nAI (Fixed Msg): ' + get_welcome_message())
    while True:
        res = chain.predict(input=input('\n\nHuman: '))
        if is_valid_json(res):
            print(f'---\n{res}\n---')
            data = json.loads(res)
            print("\n\nAI (thought): I have identifed user's need. I will use a tool to find data for the below details:")
            print("   Category:", data["category"])
            print("   Subcategory:", data["subcategory"])
            print("   Info:", data["info"])
            print("   Topic:", data["topic"])
            if data["category"] == 'restaurant':
                cuisine = data["subcategory"]
                restaurant_chain=create_csv_rag_chain('restaurants.csv')
                rag_input = f'Return three {cuisine} restaurants with top rating.'
                rag_output = restaurant_chain.invoke(rag_input)
                # Inject the RAG response to converstaion memory
                memory.save_context({"input": rag_input}, {"output": rag_output})
                print('\n\nAI (RAG): ' + rag_output)
            else:
                crew = WebSearchCrew(data["topic"])
                websearch_response = crew.search()
                memory.save_context({"input": data["topic"]}, {"output": websearch_response})
                print('\n\nAI (SearchCrew): ' + websearch_response)
        else:
            print('\n\nAI (Langchain/LLM): ' + res)
     


if __name__ == '__main__':
    main()