from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

def clean_xml_output(xml_content):
    # Clean up the XML content by removing unwanted code block markers
    cleaned_content = xml_content.replace("```xml", "").replace("```", "")
    return cleaned_content.strip()

def process_configuration(user_input):
    # Full prompt with both expert context and conversion examples including "Services"
    prompt = """
    You are an expert in networking and firewall configurations. Use your expertise to convert Cisco configurations into XML format efficiently. Key expertise areas include:

        1. **Networking Concepts:** Mastery of TCP/IP, OSI, VLANs, subnetting, and routing protocols (OSPF, BGP).
        2. **Firewall Basics:** Knowledge of packet filtering, stateful inspection, NAT, and VPNs.
        3. **Protocols and Ports:** Familiarity with protocols like HTTP, HTTPS, FTP, SSH, and their ports.
        4. **Configuration Management:** Skilled in setting up firewall rules, policies, ACLs, and managing high-availability systems.
        5. **Security Expertise:** Comprehensive understanding of cybersecurity, threat mitigation, and implementing security measures like IDS/IPS.
        6. **Automation:** Proficiency in scripting (Python) for automation of firewall tasks.
        7. **Compliance:** Understanding of standards like PCI DSS, GDPR, and HIPAA.
        8. **Continuous Learning:** Up-to-date with current networking and security trends.
        9. **Communication Skills:** Ability to clearly document and explain technical configurations.
        10. **Practical Experience:** Hands-on experience from real-world projects and troubleshooting. Given your expertise, here's how you should convert specific parts of Cisco configurations into XML:
    """
    # Append dynamic conversion examples
    prompt += """
    **FQDNs:** 
    Cisco Input: object network Kaspersky10 fqdn v4 dnl-10.geo.kaspersky.com
    XML Output:
    <generic_import_export build="11575" update_package_version="1773">
        <domain_name name="Kaspersky10" db_key="1201"/>
    </generic_import_export>

    **Hosts:**
    Cisco Input: object network 212.118.7.19 host 212.118.7.19
    XML Output:
    <generic_import_export build="11575" update_package_version="1773">
        <host name="212.118.7.19" db_key="1204">
            <mvia_address address="212.118.7.19"/>
            <third_party_monitoring netflow="false" snmp_trap="false"/>
        </host>
    </generic_import_export>
    """
    # Append further examples and notes dynamically as needed here.

    prompt += """
    Now process the following Cisco configuration using your expertise:
    {user_input}
    Return the XML output only. Adhere to the XML structure used in industry standards.
    """.format(user_input=user_input)

    # Create the prompt with user input
    prompt = ChatPromptTemplate.from_template(prompt)
    prompt_value = prompt.format_prompt(user_input=user_input)

    # Initialize the language model
    llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=os.getenv("GOOGLE_API_KEY"),
                                 temperature=0.1, convert_system_message_to_human=True, max_output_tokens=10000)
    # Create a runnable with the prompt and the language model
    response = llm.invoke(prompt_value.to_string())  # Pass the formatted string
    # Clean the XML output
    cleaned_output = clean_xml_output(response.content)
    # Return the processed and cleaned XML
    return cleaned_output

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
                st.markdown(result, unsafe_allow_html=True)
                # Download button for the cleaned XML output
                st.download_button(label="Download XML",
                                   data=result,
                                   file_name="configuration.xml",
                                   mime="text/xml")
            except Exception as e:
                st.error("Failed to convert the file.")
                logging.error("Error processing the configuration: %s", e)

if __name__ == "__main__":
    main()
