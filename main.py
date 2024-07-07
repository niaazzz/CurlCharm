import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from PIL import Image
import json
import google.generativeai as genai

# Configure OpenAI API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Define hair types and problems
hair_types = ["2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "4C"]
hair_problems = ["Frizz", "Dryness", "Breakage", "Scalp Irritation"]


# Function to generate recommendations using OpenAI
def generate_recommendations(hair_type, problems):
    prompt = f"Provide a hair care routine for hair type {hair_type} with the following problems: {', '.join(problems)} using Shea Moisture products."
    response = client.chat.completions.create(model="gpt-4",
                                              messages=[{
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=500)
    recommendations = response.choices[0].message.content.strip()
    return recommendations.split('\n')


# Function to generate hairstyle recommendation based on hair type
def generate_hairstyle_recommendation(hair_type):
    prompt = f"Suggest a suitable hairstyle for hair type {hair_type}."
    response = client.chat.completions.create(model="gpt-4",
                                              messages=[{
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=150)
    recommendation = response.choices[0].message.content.strip()
    return recommendation


# Function to fetch product images and links using web scraping
def fetch_product_images_and_links(product_name):
    search_url = f"https://www.google.com/search?q=Shea+Moisture+{product_name.replace(' ', '+')}&tbm=shop"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_link = None

    product_element = soup.find("div", class_="sh-dgr__content")
    if product_element:
        link_element = product_element.find("a", href=True)
        if link_element:
            product_link = "https://www.google.com" + link_element['href']

    return product_link


# Title and page configuration
st.set_page_config(page_title="CurlCharm Companion", page_icon=":haircut:")
st.markdown(
    "<h1 style='text-align:center; color:#b33f15;font-size:50px; font-weight:bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>CurlCharm Companion</h1>",
    unsafe_allow_html=True)

# Sidebar navigation
st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            background-color: #a64a30; 
        }
        .css-1vgnld7 {
            color: white;
        }
    </style>
""",
            unsafe_allow_html=True)

option = st.sidebar.selectbox(
    'Choose an option:',
    ['CurlCharm - Hair Care Routine & Products', 'Hairstyle Generator'])

if option == 'CurlCharm - Hair Care Routine & Products':
    # Select Hair Type
    st.markdown("<h3 style='color:#702a11;'>Select Your Hair Type</h3>",
                unsafe_allow_html=True)
    hair_type = st.selectbox(
        "",
        hair_types,
        index=0,
        help="Select the curl type that best describes your hair.",
        key="hair_type")

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
        routine = generate_recommendations(hair_type, selected_problems)
        st.subheader("Your Personalized Hair Care Routine")
        for step in routine:
            st.write(step)
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Recommended Products")
        # Extract product names from the generated routine
        product_names = []
        for step in routine:
            if "Shea Moisture" in step:
                product_name = step.split("Shea Moisture")[1].strip()
                product_names.append(product_name)

        # Fetch product links
        for product_name in product_names:
            product_link = fetch_product_images_and_links(product_name)

            if product_link:
                st.markdown(f"[{product_name}]({product_link})")
            else:
                st.write(f"{product_name}")

            st.write("---")

elif option == 'Hairstyle Generator':
    # Select Hair Type
    st.markdown("<h3 style='color:#702a11;'>Select Your Hair Type</h3>",
                unsafe_allow_html=True)
    hair_type = st.selectbox(
        "",
        hair_types,
        index=0,
        help="Select the curl type that best describes your hair.",
        key="hairstyle_hair_type")

    # Generate hairstyle button
    if st.button("Generate Suitable Hairstyle"):
        st.write("Generating hairstyle...")
        recommendation = generate_hairstyle_recommendation(hair_type)
        st.write(f"**Recommended Hairstyle:** {recommendation}")

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
    .css-1vgnld7 {
        color: white;
    }
</style>
""",
            unsafe_allow_html=True)
