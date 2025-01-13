from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

def process_configuration(user_input):
    prompt = """
    You are an expert in networking and firewall configurations. Your primary role is to convert Cisco host configurations into XML format. Focus exclusively on converting host objects from the input configuration.

    **Important Instructions:**
    1. Only process 'object network' entries that define hosts
    2. Maintain the exact XML structure shown in the examples
    3. Include all mandatory XML elements and attributes
    4. Each host must include the mvia_address and third_party_monitoring elements
    5. Preserve the original host names from the Cisco configuration

    Here are examples of the expected conversion:

    Example 1:
    Cisco Input:
    object network host-4.4.4.4
    host 4.4.4.4
    object network host-5.5.5.5
    host 5.5.5.5
    object network host-6.6.6.6
    host 6.6.6.6

    XML Output:
    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE generic_import_export SYSTEM "generic_import_export_v7.2.dtd">
    <generic_import_export build="11575" update_package_version="1773">
        <host name="host-4.4.4.4">
            <mvia_address address="4.4.4.4"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
        <host name="host-5.5.5.5">
            <mvia_address address="5.5.5.5"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
        <host name="host-6.6.6.6">
            <mvia_address address="6.6.6.6"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
    </generic_import_export>

    Example 2:
    Cisco Input:
    object network DC-Server
    host 192.168.0.201
    object network FileServer
    host 192.168.0.200
    object network Finance-Host
    host 172.16.1.12

    XML Output:
    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE generic_import_export SYSTEM "generic_import_export_v7.2.dtd">
    <generic_import_export build="11575" update_package_version="1773">
        <host name="DC-Server">
            <mvia_address address="192.168.0.201"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
        <host name="FileServer">
            <mvia_address address="192.168.0.200"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
        <host name="Finance-Host">
            <mvia_address address="172.16.1.12"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
    </generic_import_export>

    Now convert the following Cisco configuration to XML, maintaining the exact format shown above:

    {user_input}

    Return only the properly formatted XML output, starting with the XML declaration.
    """
    # Create the prompt with user input
    prompt = ChatPromptTemplate.from_template(prompt)
    prompt_value = prompt.format_prompt(user_input=user_input)

    # Initialize the language model
    llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=os.getenv("GOOGLE_API_KEY"),
                                 temperature=0.1, convert_system_message_to_human=True, max_output_tokens=10000)
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
                # Download button for the XML output
                st.download_button(label="Download XML",
                                   data=result.content,
                                   file_name="configuration.xml",
                                   mime="text/xml")
            except Exception as e:
                st.error("Failed to convert the file.")
                logging.error("Error processing the configuration: %s", e)

if __name__ == "__main__":
    main()
