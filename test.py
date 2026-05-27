import google.generativeai as genai

genai.configure(api_key="AIzaSyA7bQB4q1591ET8thrzm1rMtzzUWIssZX0")

for m in genai.list_models():
    print(m.name)