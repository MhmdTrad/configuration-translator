from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

def process_configuration(user_input):
    template = """
                You are a configuration translator. Convert the given Cisco firewall configuration into an XML format suitable for importing. Ensure the XML adheres to this structure:
                
                <generic_import_export build="11575" update_package_version="1773">
                    <network name="name" broadcast="true/false" db_key="key" ipv4_network="network/prefix"/>
                </generic_import_export>

                For reference, here are examples of conversions:

                Example 1:
                Input:
                object network internet
                subnet 10.10.10.0 255.255.255.0

                Output:
                <generic_import_export build="11575" update_package_version="1773">
                    <network name="internet" broadcast="true" db_key="1195" ipv4_network="10.10.10.0/24"/>
                </generic_import_export>

                Example 2:
                Input:
                object network server
                host 192.168.1.1

                Output:
                <generic_import_export build="11575" update_package_version="1773">
                    <network name="server" broadcast="false" db_key="1196" ipv4_network="192.168.1.1/32"/>
                </generic_import_export>

                Now process the following Cisco configuration:

                {user_input}

                Return the XML output only.
                """
    # Create the prompt with user input
    prompt = ChatPromptTemplate.from_template(template)
    prompt_value = prompt.format_prompt(user_input=user_input)

    # Initialize the language model
    llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=os.getenv("GOOGLE_API_KEY"),
                                 temperature=0.7, convert_system_message_to_human=True,)
    # Create a runnable with the prompt and the language model
    response = llm.invoke(prompt_value.to_string())  # Pass the formatted string
    # Return the processed XML
    return response


import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)

def main():
    st.title('Cisco Config to XML Converter')
    uploaded_file = st.file_uploader("Upload your Cisco configuration file", type=['txt'])
    if uploaded_file is not None:
        user_input = uploaded_file.read().decode("utf-8")
        if st.button("Convert"):
            try:
                result = process_configuration(user_input)
                st.markdown(result.content)
            except Exception as e:
                st.error("Failed to convert the file.")
                logging.error("Error processing the configuration: %s", e)
                
if __name__ == "__main__":
    main()
