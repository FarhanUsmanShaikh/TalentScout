import streamlit as st
import re
import google.generativeai as genai
import nltk
from nltk.tokenize import word_tokenize
from googletrans import Translator
import json
import os

# Download NLTK punkt tokenizer
nltk.download('punkt')

# Manually set the Gemini API key
api_key = "AIzaSyA65E9whaAne8bb5WzsJ-jfR-PkBslbxFs"
genai.configure(api_key=api_key)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'candidate_info' not in st.session_state:
    st.session_state['candidate_info'] = None
if 'questions' not in st.session_state:
    st.session_state['questions'] = None

# Initialize the translator
translator = Translator()

# Language options dictionary (you can add more languages here)
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'hi': 'Hindi'
}

# File for simulated data storage
data_file = "candidate_data.json"

# Ensure the data file exists
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump([], f)

# Helper function to save candidate data
def save_candidate_data(candidate_info):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        data.append(candidate_info)
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving candidate data: {str(e)}")

# Translate text function
def translate_text(text, target_language):
    try:
        translation = translator.translate(text, src='en', dest=target_language)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text  # Return the original text if translation fails

# Greet user function
def greet_user(language='en'):
    greeting = "👋 Hello! I'm **TalentScout**, your AI hiring assistant. Let's get started by gathering some information."
    return translate_text(greeting, language)

# Validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Validate phone number
def validate_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone) is not None

# Collect candidate information
def collect_candidate_info():
    st.markdown("### 📋 Candidate Information")
    with st.form(key='candidate_form'):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("✉️ Email Address", placeholder="Enter your email address")
            phone = st.text_input("📞 Phone Number", placeholder="Enter your phone number")
            position = st.text_input("💼 Desired Position(s)", placeholder="Enter position(s) you're applying for")
            tech_stack = st.text_area("🛠 Tech Stack", placeholder="E.g., Python, Django, React")
        with col2:
            experience = st.slider("📅 Years of Experience", 0, 40, 1)
            location = st.text_input("📍 Current Location", placeholder="Enter your location")

        st.markdown("---")
        submit_button = st.form_submit_button(label="📤 Submit")

        if submit_button:
            errors = []
            if not full_name:
                errors.append("Full Name is required.")
            if not email or not validate_email(email):
                errors.append("Enter a valid Email Address.")
            if not phone or not validate_phone(phone):
                errors.append("Enter a valid Phone Number.")
            if not tech_stack:
                errors.append("Tech Stack cannot be empty.")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                st.session_state['candidate_info'] = {
                    'Full Name': full_name,
                    'Email': email,
                    'Phone': phone,
                    'Experience': experience,
                    'Position': position,
                    'Location': location,
                    'Tech Stack': tech_stack.split(', ')
                }
                save_candidate_data(st.session_state['candidate_info'])
                st.success("✅ Information collected successfully!")
                
                # Automatically trigger question generation and rerun
                tech_stack = st.session_state['candidate_info']['Tech Stack']
                st.info("Generating interview questions for your tech stack... 🧑‍💻")
                questions = generate_questions(tech_stack)
                st.session_state['questions'] = questions
                st.session_state['conversation'].append("Candidate information collected and questions generated.")
                
                # Trigger a rerun to display questions without needing a second click
                st.experimental_rerun()
                return True  # Returning True triggers a rerun to display questions
    return False

# Enhanced prompt design for generating technical questions
def enhanced_prompt_for_questions(tech):
    return (f"You are an expert interviewer. Generate 3-5 highly specific, challenging, and contextually relevant "
            f"technical interview questions for a candidate proficient in {tech}. The questions should test deep understanding "
            f"and practical application of {tech} in real-world scenarios. Additionally, explain why each question is important "
            f"and how it tests practical skills with respect to {tech}. Ensure the questions cover various aspects of {tech}, "
            f"including theory, application, and problem-solving approaches.")

# Generate questions using Gemini API
def generate_questions(tech_stack):
    questions = {}
    for tech in tech_stack:
        try:
            prompt = enhanced_prompt_for_questions(tech)
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            generated_text = response.text.strip()
            
            # Ensure that the response text is split into lines and cleaned up
            if generated_text:
                question_list = [line.strip() for line in generated_text.split('\n') if line.strip()]
                questions[tech] = question_list[:5]  # Extract up to 5 questions
            else:
                questions[tech] = ["No questions generated. Please try again."]
        except Exception as e:
            st.error(f"Error generating questions for {tech}: {str(e)}. Using fallback questions.")
            questions[tech] = generate_questions_nltk([tech])[tech]
    return questions

# Fallback question generator using NLTK
def generate_questions_nltk(tech_stack):
    questions = {}
    for tech in tech_stack:
        questions[tech] = [
            f"What is your experience with {tech}?",
            f"Can you explain the basics of {tech}?",
            f"How do you approach problems using {tech}?",
            f"What are some challenges you've faced while using {tech}?",
            f"Can you give an example of a real-world application of {tech}?"
        ]
    return questions


# Display generated questions
def display_questions(questions):
    st.markdown("## 🔧 Technical Questions")
    for tech, qs in questions.items():
        if qs:
            st.markdown(f"### 📂 {tech}:")
            for q in qs:
                st.markdown(f"- {q}")
        else:
            st.markdown(f"**No questions available for {tech}.**")

# End the conversation and show summary
def end_conversation():
    candidate_info = st.session_state['candidate_info']
    st.markdown("## 📋 Summary of Your Information")
    st.markdown(f"**👤 Full Name:** {candidate_info['Full Name']}")
    st.markdown(f"**✉️ Email:** {candidate_info['Email']}")
    st.markdown(f"**📞 Phone:** {candidate_info['Phone']}")
    st.markdown(f"**📅 Experience:** {candidate_info['Experience']} years")
    st.markdown(f"**💼 Position:** {candidate_info['Position']}")
    st.markdown(f"**📍 Location:** {candidate_info['Location']}")
    st.markdown(f"**🛠 Tech Stack:** {', '.join(candidate_info['Tech Stack'])}")
    st.success("Thank you for using TalentScout! We'll reach out to you soon. Goodbye! 👋")
    st.session_state.clear()

# Main function
def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🎯", layout="wide")
    st.sidebar.image("Logo.webp", use_column_width=True)
    st.sidebar.title("TalentScout")
    st.sidebar.markdown("#### Your AI Hiring Assistant 🎯")
    st.sidebar.markdown("---")

    st.title("🎯 TalentScout Hiring Assistant")

    selected_language = st.sidebar.selectbox("🌐 Select Your Language", options=list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])

    st.write(greet_user(selected_language))

    if not st.session_state['candidate_info']:
        if collect_candidate_info():
            tech_stack = st.session_state['candidate_info']['Tech Stack']
            st.info("Generating interview questions for your tech stack... 🧑‍💻")
            questions = generate_questions(tech_stack)
            st.session_state['questions'] = questions
            st.session_state['conversation'].append("Candidate information collected and questions generated.")
    else:
        display_questions(st.session_state['questions'])

    if st.sidebar.button("End Conversation 👋"):
        end_conversation()

if __name__ == "__main__":
    main()