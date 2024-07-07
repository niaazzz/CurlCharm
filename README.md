
## 🚀 CurlCharm Companion
CurlCharm is a Streamlit-based web application designed to provide personalized recommendations for hair care routines, products (specifically Shea Moisture), and hairstyles based on selected hair types and problems.


## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## Features

1. Personalized Hair Care Routine & Products
- Select Your Hair Type: Choose from a range of hair types (2A to 4C).
- Select Your Hair Problems: Pick specific issues such as frizz, dryness, breakage, or scalp irritation.
- Generate Hair Care Routine: Receive a personalized hair care routine tailored to your selected hair type and problems.
- Recommended Products: Explore recommended Shea Moisture products aligned with your personalized routine.

2.  Hairstyle Generator
- Select Your Hair Type: Choose your hair type to get hairstyle recommendations.
- Generate Suitable Hairstyle: Receive personalized hairstyle suggestions based on your selected hair type.

## Technologies Used
- Streamlit: For building the interactive web application.
- OpenAI GPT-4: To generate personalized hair care routines and hairstyle recommendations.
- Requests and BeautifulSoup: For web scraping to fetch product links.
  
## Installation Steps

Clone the Repository:

```bash
 git clone https://github.com/your/repository.git
cd repository
```
Install Dependencies:
```bash
pip install -r requirements.txt
```
Run the Application:
```bash
streamlit run app.py
```
Provide API Keys:
- Ensure you have API keys for OpenAI (GPT-4) and Google GenerativeAI. Store them securely in a secrets.toml file.

## Usages
- Select an option from the sidebar navigation (CurlCharm - Hair Care Routine & Products or Hairstyle Generator).
- Follow on-screen instructions to choose hair type, select problems, and generate recommendations.
- Click buttons to generate personalized hair care routines or hairstyle suggestions.
