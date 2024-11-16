from openai import OpenAI
import streamlit as st

class Model:
    @staticmethod
    def openai_chatgpt(transcript, prompt, extra=""):
        client = OpenAI(api_key=st.session_state['openai_api_key'])
        model = "gpt-3.5-turbo"
        message = [{"role": "system", "content": prompt + extra + transcript}]
        try:
            response = client.chat.completions.create(model=model, messages=message)
            return response.choices[0].message.content
        except Exception as e:
            return "⚠️ There is a problem with the API key or with python module."
