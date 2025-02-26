import xml.etree.ElementTree as ET
import requests


# Load the POM.xml file from a URL (without downloading the file)
def load_pom_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful
    return ET.ElementTree(ET.fromstring(response.text))


# Extract properties from the <properties> block
def extract_properties(root):
    properties = []
    # Maven namespace
    namespaces = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    # Find the <properties> block in the XML file, considering the namespace
    properties_element = root.find(".//maven:properties", namespaces)
    if properties_element is not None:
        for prop in properties_element:
            # Clean up the namespace prefix in the tags
            tag_name = prop.tag.split('}', 1)[-1]  # Get the tag name without the namespace prefix
            properties.append(f"{tag_name}: {prop.text}")
    else:
        print("No <properties> block found in the XML file.")
    return properties


def main():
    # URL of the raw pom.xml file from the GitHub repository
    url = "https://raw.githubusercontent.com/apache/spark/master/pom.xml"
    # Load and parse the POM file
    tree = load_pom_from_url(url)
    root = tree.getroot()
    # Extract properties
    properties = extract_properties(root)
    # Display the extracted properties
    if properties:
        print("\nExtracted Properties:")
        for prop in properties:
            print(prop)
    else:
        print("\nNo properties found in the pom.xml file.")


if __name__ == "__main__":
    main()
