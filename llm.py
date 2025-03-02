import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# LLM Configuration
DEFAULT_MODEL = "TinyLlama-1.1B-Chat-v1.0"
API_URL = "http://localhost:1234/v1"
API_KEY = "type-anything"

# Load Master Dataset
MASTER_FILE = "Master_Datasheet.csv"

def get_llm(model_name):
    return ChatOpenAI(
        model_name=model_name, 
        base_url=API_URL, 
        api_key=API_KEY,
        temperature=0.2,  # Low randomness for structured, fact-based compliments
        max_tokens=35,  # Strict length control to avoid unnecessary details
        top_p=0.8,  # Keeps responses precise while allowing slight creativity
        frequency_penalty=0.2,  # Slight repetition reduction for uniqueness
        presence_penalty=0.1  # Ensures relevant yet varied outputs
    )

def generate_mail(llm, bio):
    query = f"""Generate a concise and structured compliment based strictly on the given biography.

### Format:
- The sentence **must** start with **'Your [expertise/focus] in [industry/niche], along with your [unique element], establishes/highlights/positions your brand as [value proposition].'**

### Guidelines:
- **Max 25 words.**
- **Use only the information present in the biography.** No assumptions or added details.
- **Be specific.** Avoid vague terms like 'high-quality' without explaining why.
- **Keep it natural and engaging.** It should sound professional yet personalized.
- **Maintain the structured format.**

#### Example Outputs:
- Your expertise in nutrition and diet planning, along with your focus on Cordyceps Militaris, establishes your brand as a valuable resource for health-conscious individuals.
- Your focus on pet training, boarding, and walking, combined with personalized care, highlights your commitment to enhancing pets' well-being in Gurgaon.
- Your comprehensive offering of veterinary needs, from vaccines to surgical instruments, positions your brand as an essential resource for veterinarians and pet care professionals.
- Your comprehensive services and commitment to pet health and safety make your hospital in Ahmedabad a trusted resource for all pet care needs.

Now, generate a concise and structured compliment based on this biography:
"{bio}"
"""


    response = llm.invoke(query)
    return response.content.strip()

# Authentication
PASSWORD = "kharagpur420"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    password_input = st.text_input("Enter Password:", type="password")
    if st.button("Login"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Incorrect password. Try again.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("Didi, aap kya karna chahte ho")
option = st.sidebar.radio("Select One", ["Upload Data", "Filter Data", "Generate Compliments", "Master Dataset"])

# Upload Data
if option == "Upload Data":
    st.title("Upload & Filter Data")
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx", "xls"])
    followers_limit = st.slider("Max Followers", 100, 10000, 8000)
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        
        # Apply initial filters
        df = df[(df['Is business'] == 'YES') & (df['Public email'].notna()) & 
                (df['Followers count'] < followers_limit) & (df['Phone country code'] == 91.0)]
        
        # Load Master Dataset if exists
        try:
            master_df = pd.read_csv("Master_Datasheet.csv")
        except FileNotFoundError:
            master_df = pd.DataFrame(columns=df.columns)  # Create empty DF with same structure
        
        # Remove duplicates by checking with Master Dataset
        df = df[~df['Public email'].isin(master_df['Public email'])]
        
        # Store filtered unique contacts in session state
        st.session_state.uploaded_df = df.drop_duplicates(subset=['Public email'])
        
        st.success(f"{len(st.session_state.uploaded_df)} new unique contacts loaded!")
        st.dataframe(st.session_state.uploaded_df)


# Filter & Select Rows
elif option == "Filter Data":
    st.title("Select Rows")
    if "uploaded_df" not in st.session_state:
        st.warning("Please upload data first.")
    else:
        num_rows = st.slider("Select number of rows to process", 1, len(st.session_state.uploaded_df), 100)
        selected_data = st.session_state.uploaded_df.head(num_rows).copy()
        st.session_state.selected_data = selected_data
        st.dataframe(selected_data)
        if st.button("Add to Master Data"):
            try:
                master_df = pd.read_csv(MASTER_FILE)
            except FileNotFoundError:
                master_df = pd.DataFrame(columns=selected_data.columns)
            
            # Remove duplicates based on Public email
            combined_df = pd.concat([selected_data,master_df]).drop_duplicates(subset=['Public email'], keep='first')
            combined_df.to_csv(MASTER_FILE, index=False)
            st.success("Unique data added to Master Dataset!")

# Generate Personalized Compliments
elif option == "Generate Compliments":
    st.title("Generate Personalized Compliments")
    if "selected_data" not in st.session_state or len(st.session_state.selected_data) == 0:
        st.warning("Please select rows first.")
    else:
        model_name = st.text_input("Enter LLM Model (default: TinyLlama-1.1B-Chat-v1.0)", DEFAULT_MODEL)
        num_to_process = st.slider("Number of rows to process", 1, len(st.session_state.selected_data), 5)
        selected_data = st.session_state.selected_data.head(num_to_process).copy()
        llm = get_llm(model_name)
        if st.button("Generate Compliments"):
            progress_bar = st.progress(0)
            total_rows = len(selected_data)
            for idx, row in selected_data.iterrows():
                selected_data.loc[idx, "Compliment"] = generate_mail(llm, row["Biography"])
                progress_bar.progress(min((idx + 1) / total_rows, 1.0))
            st.success("Compliments generated!")
            st.dataframe(selected_data[["Username", "Public email", "Followers count", "Compliment", "Profile link"]])
            csv_data = selected_data.to_csv(index=False)
            st.download_button("Download CSV", data=csv_data, file_name="Personalized_Compliments.csv", mime="text/csv")

# Master Dataset View
elif option == "Master Dataset":
    st.title("Master Contact List")
    try:
        master_df = pd.read_csv(MASTER_FILE)
        st.dataframe(master_df)
    except FileNotFoundError:
        st.warning("No master dataset found. Please add data first.")
