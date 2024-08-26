


## Task 1. Configure your environment and project

copy this command:
```bash
PROJECT_ID=$(gcloud config get-value project)
REGION=europe-west4
echo "PROJECT_ID=${PROJECT_ID}"
echo "REGION=${REGION}"
```
```bash
gcloud services enable cloudbuild.googleapis.com cloudfunctions.googleapis.com run.googleapis.com logging.googleapis.com storage-component.googleapis.com aiplatform.googleapis.com
```

## Task 2. Set up the application environment

change dir
```bash
mkdir ~/gemini-app
cd ~/gemini-app
```

Set up a Python virtual environment

```bash
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
```

Install application dependencies

```bash
cat > ~/gemini-app/requirements.txt <<EOF
streamlit
google-cloud-aiplatform==1.38.1
google-cloud-logging==3.6.0

EOF
```
```bash
pip install -r requirements.txt
```

## Task 3. Develop the app
```bash
cat > ~/gemini-app/app.py <<EOF
import os
import streamlit as st
from app_tab1 import render_story_tab
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import logging
from google.cloud import logging as cloud_logging

# configure logging
logging.basicConfig(level=logging.INFO)
# attach a Cloud Logging handler to the root logger
log_client = cloud_logging.Client()
log_client.setup_logging()

PROJECT_ID = os.environ.get('PROJECT_ID')   # Your Qwiklabs Google Cloud Project ID
LOCATION = os.environ.get('REGION')         # Your Qwiklabs Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)

@st.cache_resource
def load_models():
    text_model_pro = GenerativeModel("gemini-pro")
    multimodal_model_pro = GenerativeModel("gemini-pro-vision")
    return text_model_pro, multimodal_model_pro

st.header("Vertex AI Gemini API", divider="rainbow")
text_model_pro, multimodal_model_pro = load_models()

tab1, tab2, tab3, tab4 = st.tabs(["Story", "Marketing Campaign", "Image Playground", "Video Playground"])

with tab1:
    render_story_tab(text_model_pro)

EOF
cat ~/gemini-app/app.py
```
Develop tab1 - Story

```bash
cat > ~/gemini-app/app_tab1.py <<EOF
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from response_utils import *
import logging

# create the model prompt based on user input.
def generate_prompt():
    # Story character input
    character_name = st.text_input("Enter character name: \n\n",key="character_name",value="Mittens")
    character_type = st.text_input("What type of character is it? \n\n",key="character_type",value="Cat")
    character_persona = st.text_input("What personality does the character have? \n\n",
                                      key="character_persona",value="Mitten is a very friendly cat.")
    character_location = st.text_input("Where does the character live? \n\n",key="character_location",value="Andromeda Galaxy")

    # Story length and premise
    length_of_story = st.radio("Select the length of the story: \n\n",["Short","Long"],key="length_of_story",horizontal=True)
    story_premise = st.multiselect("What is the story premise? (can select multiple) \n\n",["Love","Adventure","Mystery","Horror","Comedy","Sci-Fi","Fantasy","Thriller"],key="story_premise",default=["Love","Adventure"])
    creative_control = st.radio("Select the creativity level: \n\n",["Low","High"],key="creative_control",horizontal=True)
    if creative_control == "Low":
        temperature = 0.30
    else:
        temperature = 0.95

    prompt = f"""Write a {length_of_story} story based on the following premise: \n
    character_name: {character_name} \n
    character_type: {character_type} \n
    character_persona: {character_persona} \n
    character_location: {character_location} \n
    story_premise: {",".join(story_premise)} \n
    If the story is "short", then make sure to have 5 chapters or else if it is "long" then 10 chapters. 
    Important point is that each chapter should be generated based on the premise given above.
    First start by giving the book introduction, chapter introductions and then each chapter. It should also have a proper ending.
    The book should have a prologue and an epilogue.
    """

    return temperature, prompt

# function to render the story tab, and call the model, and display the model prompt and response.
def render_story_tab (text_model_pro: GenerativeModel):
    st.write("Using Gemini 1.0 Pro - Text only model")
    st.subheader("Generate a story")

    temperature, prompt = generate_prompt()

    config = {
        "temperature": temperature,
        "max_output_tokens": 2048,
        }

    generate_t2t = st.button("Generate my story", key="generate_t2t")
    if generate_t2t and prompt:
        # st.write(prompt)
        with st.spinner("Generating your story using Gemini..."):
            first_tab1, first_tab2 = st.tabs(["Story response", "Prompt"])
            with first_tab1: 
                response = get_gemini_pro_text_response(text_model_pro, prompt, generation_config=config)
                if response:
                    st.write("Your story:")
                    st.write(response)
                    logging.info(response)
            with first_tab2: 
                st.text(prompt)

EOF
```
Develop response_utils
```bash
cat > ~/gemini-app/response_utils.py <<EOF

from vertexai.preview.generative_models import (Content,
                                            GenerationConfig,
                                            GenerativeModel,
                                            GenerationResponse,
                                            Image,
                                            HarmCategory, 
                                            HarmBlockThreshold,
                                            Part)

def get_gemini_pro_text_response( model: GenerativeModel,
                                  prompt: str, 
                                  generation_config: GenerationConfig,
                                  stream=True):

    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    responses = model.generate_content(prompt,
                                   generation_config = generation_config,
                                   safety_settings = safety_settings,
                                   stream=True)

    final_response = []
    for response in responses:
        try:
            final_response.append(response.text)
        except IndexError:
            final_response.append("")
            continue
    return " ".join(final_response)

EOF
```
## Task 4. Run and test the app locally

run the app
```bash
streamlit run app.py \
--browser.serverAddress=localhost \
--server.enableCORS=false \
--server.enableXsrfProtection=false \
--server.port 8080
```
Test the app - Story tab
app
test generate story

Develop tab2 - Marketing Campaign
```bash
cat > ~/gemini-app/app_tab2.py <<EOF
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from response_utils import *
import logging

# create the model prompt based on user input.
def generate_prompt():
    st.write("Using Gemini 1.0 Pro - Text only model")
    st.subheader("Generate your marketing campaign")

    product_name = st.text_input("What is the name of the product? \n\n",key="product_name",value="ZomZoo")
    product_category = st.radio("Select your product category: \n\n",["Clothing","Electronics","Food","Health & Beauty","Home & Garden"],key="product_category",horizontal=True)

    st.write("Select your target audience: ")
    target_audience_age = st.radio("Target age: \n\n",["18-24","25-34","35-44","45-54","55-64","65+"],key="target_audience_age",horizontal=True)
    # target_audience_gender = st.radio("Target gender: \n\n",["male","female","trans","non-binary","others"],key="target_audience_gender",horizontal=True)
    target_audience_location = st.radio("Target location: \n\n",["Urban", "Suburban","Rural"],key="target_audience_location",horizontal=True)

    st.write("Select your marketing campaign goal: ")
    campaign_goal = st.multiselect("Select your marketing campaign goal: \n\n",["Increase brand awareness","Generate leads","Drive sales","Improve brand sentiment"],key="campaign_goal",default=["Increase brand awareness","Generate leads"])
    if campaign_goal is None:
        campaign_goal = ["Increase brand awareness","Generate leads"]
    brand_voice = st.radio("Select your brand voice: \n\n",["Formal","Informal","Serious","Humorous"],key="brand_voice",horizontal=True)
    estimated_budget = st.radio("Select your estimated budget ($): \n\n",["1,000-5,000","5,000-10,000","10,000-20,000","20,000+"],key="estimated_budget",horizontal=True)

    prompt = f"""Generate a marketing campaign for {product_name}, a {product_category} designed for the age group: {target_audience_age}. 
    The target location is this: {target_audience_location}.
    Aim to primarily achieve {campaign_goal}. 
    Emphasize the product's unique selling proposition while using a {brand_voice} tone of voice. 
    Allocate the total budget of {estimated_budget}.  
    With these inputs, make sure to follow following guidelines and generate the marketing campaign with proper headlines: \n
    - Briefly describe the company, its values, mission, and target audience.
    - Highlight any relevant brand guidelines or messaging frameworks.
    - Provide a concise overview of the campaign's objectives and goals.
    - Briefly explain the product or service being promoted.
    - Define your ideal customer with clear demographics, psychographics, and behavioral insights.
    - Understand their needs, wants, motivations, and pain points.
    - Clearly articulate the desired outcomes for the campaign.
    - Use SMART goals (Specific, Measurable, Achievable, Relevant, and Time-bound) for clarity.
    - Define key performance indicators (KPIs) to track progress and success.
    - Specify the primary and secondary goals of the campaign.
    - Examples include brand awareness, lead generation, sales growth, or website traffic.
    - Clearly define what differentiates your product or service from competitors.
    - Emphasize the value proposition and unique benefits offered to the target audience.
    - Define the desired tone and personality of the campaign messaging.
    - Identify the specific channels you will use to reach your target audience.
    - Clearly state the desired action you want the audience to take.
    - Make it specific, compelling, and easy to understand.
    - Identify and analyze your key competitors in the market.
    - Understand their strengths and weaknesses, target audience, and marketing strategies.
    - Develop a differentiation strategy to stand out from the competition.
    - Define how you will track the success of the campaign.
    - Use relevant KPIs to measure performance and return on investment (ROI).
    Provide bullet points and headlines for the marketing campaign. Do not produce any empty lines. Be very succinct and to the point.
    """

    return prompt

# function to render the story tab, and call the model, and display the model prompt and response.
def render_mktg_campaign_tab (text_model_pro: GenerativeModel):
    st.write("Using Gemini 1.0 Pro - Text only model")
    st.subheader("Generate a marketing campaign")

    prompt = generate_prompt()

    config = {
        "temperature": 0.8,
        "max_output_tokens": 2048,
        }

    generate_t2m = st.button("Generate campaign", key="generate_t2m")
    if generate_t2m and prompt:
        # st.write(prompt)
        with st.spinner("Generating a marketing campaign using Gemini..."):
            first_tab1, first_tab2 = st.tabs(["Campaign response", "Prompt"])
            with first_tab1: 
                response = get_gemini_pro_text_response(text_model_pro, prompt, generation_config=config)
                if response:
                    st.write("Marketing campaign:")
                    st.write(response)
                    logging.info(response)
            with first_tab2: 
                st.text(prompt)

EOF
```
Modify the main app entry point
```bash
cat >> ~/gemini-app/app.py <<EOF

from app_tab2 import render_mktg_campaign_tab

with tab2:
    render_mktg_campaign_tab(text_model_pro)

EOF
```

Test the app - Marketing campaign tab
```bash
streamlit run app.py \
--browser.serverAddress=localhost \
--server.enableCORS=false \
--server.enableXsrfProtection=false \
--server.port 8080
```
