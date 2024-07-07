import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from PIL import Image
import json

# Configure OpenAI API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define hair types and problems
hair_types = ["1A","1B","1C","2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "4C"]
hair_porosities = ["Low Porosity", "Normal Porosity", "High Porosity"]
hair_problems = ["Frizz", "Dryness", "Breakage", "Scalp Issues", "Curl Definition", "Color Protection", "Damage"]


# Function to generate recommendations using OpenAI
def generate_recommendations(hair_type, porosity, problems):
        prompt = f"Provide a hair care routine for hair type {hair_type} with {porosity} porosity and the following problems: {', '.join(problems)} using Shea Moisture products."
        response = client.chat.completions.create(model="gpt-4o",
                                                  messages=[{
                                                      "role": "user",
                                                      "content": prompt
                                                  }],
                                                  max_tokens=700)
        recommendations = response.choices[0].message.content.strip()
        return recommendations.split('\n')


def generate_hairstyle_recommendation(hair_type):
    prompt = f"Suggest a suitable hairstyle for hair type {hair_type}."
    response = client.chat.completions.create(model="gpt-4o",
                                              messages=[{
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=200)
    recommendation = response.choices[0].message.content.strip()

    # List of hairstyles to bold (add more as needed)
    hairstyles = [
        "Pixie Cut", "Bob", "Layered Cut", "Curly Bangs", "Afro", "Twists",
        "Braids", "Bantu Knots", "Wash and Go", "Updo"
    ]

    # Bold the hairstyles in the recommendation text
    for style in hairstyles:
        recommendation = recommendation.replace(style, f"**{style}**")

    return recommendation


def fetch_product_images_and_links(product_name):
    search_url = f"https://www.google.com/search?q=Shea+Moisture+{product_name.replace(' ', '+')}&tbm=shop"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        product_link = None
        product_image_url = None

        # Find the first product element
        product_element = soup.find("div", class_="sh-dgr__content")

        if product_element:
            # Find the link to the product
            link_element = product_element.find("a", href=True)
            if link_element:
                product_link = "https://www.google.com" + link_element['href']

                # Fetch the product page to extract the image URL
                product_page_response = requests.get(product_link, headers=headers)
                product_page_response.raise_for_status()

                product_page_soup = BeautifulSoup(product_page_response.text, 'html.parser')

                # Find the product image element
                image_element = product_page_soup.find("img", class_="sh-div__image")
                if image_element and 'src' in image_element.attrs:
                    product_image_url = image_element['src']

        return product_link, product_image_url

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

# Title and page configuration
st.set_page_config(page_title="CurlCharm Companion", page_icon=":haircut:")
# Styling the title with HTML and CSS
st.markdown(
    "<h1 style='text-align:center; color:#b33f15; font-size:60px; font-weight:bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>CurlCharm Companion</h1>",
    unsafe_allow_html=True)

# Sidebar navigation
st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            background-color: #fc8665; 
        }
    </style>
""",
            unsafe_allow_html=True)

# Example image URL
image_url = "images/CurlCharm.png"

# Display image in the sidebar
st.sidebar.image(image_url, caption='', width=250)

option = st.sidebar.selectbox(
    'Choose an option:',
    ['Hair Care Routine & Products', 'Hairstyle Generator'])

images_url = 'https://hips.hearstapps.com/hmg-prod/images/elle-curl-guide-chart-1629731282.png?resize=980:*'

# HTML code to center the image
html_code = f"""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
    <img src="{images_url}" alt="Image" width="550">
</div>
"""

# Display the image using Streamlit's HTML component
st.markdown(html_code, unsafe_allow_html=True)

if option == 'Hair Care Routine & Products':
    # Select Hair Type
    st.markdown("<h3 style='color:#702a11;'>Select Your Hair Type</h3>",
                unsafe_allow_html=True)
    hair_type = st.selectbox(
        "",
        hair_types,
        index=0,
        help="Select the curl type that best describes your hair.",
        key="hair_type")

    # Select Hair Porosity
    st.markdown("<h3 style='color:#702a11;'>Select Your Hair Porosity</h3>", unsafe_allow_html=True)
    porosity = st.selectbox(
        "",
        hair_porosities,
        index=0,
        help="Select the porosity of your hair.",
        key="porosity")

    # Select Hair Problems
    st.markdown("<h3 style='color:#702a11;'>Select Your Hair Problems</h3>",
                unsafe_allow_html=True)
    selected_problems = st.multiselect(
        "Choose all that apply:",
        hair_problems,
        help="Select the hair problems you are experiencing.")

    # Generate Routine Button
    st.markdown("<div>", unsafe_allow_html=True)
    if st.button("Generate Hair Care Routine"):
        # Generate routine and recommendations
        routine = generate_recommendations(hair_type, selected_problems, porosity)
        st.subheader("Your Personalized Hair Care Routine")
        for step in routine:
            st.write(step)
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Recommended Products")
        col1, col2, col3 = st.columns(3)

        # Extract product names from the generated routine
        product_names = []
        for step in routine:
            words = step.split()
            for word in words:
                if word.startswith("Shea") or word.startswith("shea"):
                    product_name = ' '.join(words[words.index(word):])
                    product_names.append(product_name.strip())
                    break

        # Fetch product links and images
        for i, product_name in enumerate(product_names):
            product_link, product_image_url = fetch_product_images_and_links(product_name)

            # Display product in columns
            if i % 3 == 0:
                with col1:
                    if product_link and product_image_url:
                        st.image(product_image_url, width=300, use_column_width=True)
                        st.markdown(f"[{product_name}]({product_link})")
                    else:
                        st.write(f"{product_name}")
            elif i % 3 == 1:
                with col2:
                    if product_link and product_image_url:
                        st.image(product_image_url, width=300, use_column_width=True)
                        st.markdown(f"[{product_name}]({product_link})")
                    else:
                        st.write(f"{product_name}")
            else:
                with col3:
                    if product_link and product_image_url:
                        st.image(product_image_url, width=300, use_column_width=True)
                        st.markdown(f"[{product_name}]({product_link})")
                    else:
                        st.write(f"{product_name}")

elif option == 'Hairstyle Generator':
    # Select Hair Type
    st.markdown(
        "<h3 style='color:#702a11;'>Select the curl type that best describes your hair</h3>",
        unsafe_allow_html=True)
    hair_type = st.selectbox(
        "",
        hair_types,
        index=0,
        help="Select the curl type that best describes your hair.",
        key="hairstyle_hair_type")

    # Generate hairstyle button
    if st.button("Generate Suitable Hairstyle"):
        recommendation = generate_hairstyle_recommendation(hair_type)
        st.markdown(f"**Recommended Hairstyle:** {recommendation}",
                    unsafe_allow_html=True)

# Add custom CSS for the button and body background
st.markdown("""
<style>
    body {
        background-color: #F5F5DC;
    }
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton > button {
        background-color: #702a11;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        width: 500px;
    }
    .stButton > button:hover {
        background-color: #f0825b;
        color: white;
    }
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        background-color: #702a11; 
    }
    h1 {
        text-align: center;
        color: #b33f15;
        font-size: 60px;
        font-weight: bold;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.5);
    }
    h3 {
        color: #702a11;
    }
</style>
""",
            unsafe_allow_html=True)
