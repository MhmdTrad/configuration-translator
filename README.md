### README: Cisco Config to XML Converter

---

# Cisco Config to XML Converter

This application is designed to streamline the conversion of Cisco networking configurations into standardized XML format. It leverages cutting-edge AI from Google Generative AI (`gemini-pro`) to automate the process, ensuring accuracy and efficiency in transforming complex networking configurations. The app provides a user-friendly interface for uploading Cisco configuration files, processes them intelligently, and delivers well-structured XML outputs for seamless integration with other systems.

---

## Features

1. **Expert-Level Conversion**:
   - Utilizes a robust AI model to transform Cisco configurations into XML with precision and adherence to industry standards.
   - Incorporates networking and security expertise for accurate representation.

2. **Dynamic Prompt Engineering**:
   - Tailored AI prompts ensure proper handling of networking elements such as FQDNs, Hosts, and more.

3. **Streamlined User Experience**:
   - Simple file upload interface using Streamlit.
   - Instant conversion and preview of the XML output.

4. **Cleaned and Standardized Outputs**:
   - XML outputs are stripped of unnecessary markers, ensuring readiness for downstream applications.

5. **Downloadable Results**:
   - Provides an option to download the processed XML for further use.

6. **Secure and Configurable**:
   - Uses environment variables to manage API keys securely.

---

## Key Benefits

1. **Time-Saving**:
   - Eliminates the need for manual XML conversion, significantly reducing the time required for network configuration management.

2. **Accuracy**:
   - Ensures compliance with XML standards and reduces human error in configuration translation.

3. **Scalable Solution**:
   - Handles extensive configuration files with ease, making it suitable for large-scale deployments.

4. **Customizable and Extendable**:
   - Designed to accommodate additional networking elements and configurations with minimal adjustments.

5. **User-Friendly Interface**:
   - Even non-technical users can easily process configurations and download results.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/cisco-config-to-xml.git
   cd cisco-config-to-xml
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project directory and add your Google API key:
     ```
     GOOGLE_API_KEY=your_google_api_key
     ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Open the application in your browser.
2. Upload your Cisco configuration file (`.txt` format).
3. Click the **Convert** button to process the file.
4. View the resulting XML on the interface or download it directly.

---

## Example Outputs

### Input (Cisco Configuration):
```
object network Kaspersky10 fqdn v4 dnl-10.geo.kaspersky.com
object network 212.118.7.19 host 212.118.7.19
```

### Output (XML):
```xml
<generic_import_export build="11575" update_package_version="1773">
    <domain_name name="Kaspersky10" db_key="1201"/>
</generic_import_export>

<generic_import_export build="11575" update_package_version="1773">
    <host name="212.118.7.19" db_key="1204">
        <mvia_address address="212.118.7.19"/>
        <third_party_monitoring netflow="false" snmp_trap="false"/>
    </host>
</generic_import_export>
```

---

## Requirements

- Python 3.8+
- Streamlit
- Google Generative AI (`gemini-pro`) access
- Internet connection

---

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for enhancements or bug fixes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Key Takeaways

- Automate Cisco configuration translation for faster workflows.
- Ensure XML compliance with minimal effort.
- Boost productivity with cutting-edge AI-driven automation. 

---

