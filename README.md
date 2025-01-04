# TalentScout
TalentScout: AI Hiring Assistant

Project Overview

TalentScout is an AI-powered hiring assistant designed to streamline the recruitment process for tech roles. This project demonstrates how AI can be used to:

1.Gather candidate information interactively.
2.Generate challenging, role-specific technical interview questions using advanced natural language processing (NLP).
3.Provide multilingual support for diverse user bases.
4.Implement data handling mechanisms while adhering to privacy best practices.


Features

-Interactive User Interface: A simple, user-friendly UI built with Streamlit to collect candidate information.
-Advanced Question Generation: Uses the Gemini API to generate highly tailored, real-world technical questions for the candidate's tech stack.
-Multilingual Support: Supports multiple languages via the Google Translate API, making it accessible to users across the globe.
-Simulated Data Storage: Candidate information is securely stored in a local JSON file.
-Data Validation: Ensures that email, phone numbers, and other fields are correctly formatted.
-Fallback Question Mechanism: In case of API failure, standard questions are generated using NLTK.


Technologies Used

1.Streamlit: For building the interactive user interface.
2.Google Gemini API: For generating technical interview questions.
3.Google Translate API: For multilingual support.
4.NLTK: For fallback question generation when the API is unavailable.
5.JSON: For local data storage.
6.Python: Programming language used.


Installation and Setup

Prerequisites
Python 3.9 or higher.
An active Google Cloud account for accessing the Gemini API.
pip installed for managing dependencies.

Installation Steps

Clone the repository:
git clone https://github.com/yourusername/TalentScout.git

cd TalentScout

Install dependencies:

Download the NLTK tokenizer:

import nltk
nltk.download('punkt')

Set up your Gemini API key:

Run the application:

streamlit run app.py


Usage Instructions

-Launch the Application: Open the Streamlit app in your browser.
-Language Selection: Choose your preferred language from the sidebar.
-Provide Candidate Information: Fill out the form with details such as name, email, phone number, experience, and tech stack.
-Generate Questions: The assistant will generate technical questions tailored to the provided tech stack.
-End Conversation: View a summary of the candidate's information and finalize the session.


Limitations

1.This is an assignment-level project and is not intended for production use.
2.Data storage is simulated with no encryption and should not be used for sensitive or real-world data.
3.Dependency on Google APIs may result in usage limitations based on your account quota.


Submission Guidelines Compliance

-Clear problem statement and scope defined.
-Complete code with inline comments.
-Detailed and concise documentation provided.
-Project structured to showcase the practical application of AI tools.

Future Enhancements

1.Integrate a database for scalable and secure data storage.
2.Add support for more languages to reach a wider audience.
3.Implement more sophisticated validation for user inputs.




Here are the titles of the completed tasks:

User Interface Development (Streamlit)

Greeting & Chatbot Introduction

Information Gathering

Tech Stack Declaration

Technical Question Generation

Context Handling

Fallback Mechanism

End Conversation

Prompt Design for Information Gathering

Prompt Design for Question Generation

Data Handling (Simulated Data)

Data Privacy Compliance

Documentation (README)

Code Quality (Structure & Readability)

Version Control (Git)

Multilingual Support

UI Enhancements

Performance Optimization

Demo (Live Link or Video)


Developed By: Farhan

Date: January 4, 2025
