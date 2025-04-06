from google import genai

client = genai.Client(api_key="AIzaSyCTzfZbtjZSxmWrLY68ZdZW0R5PXhxn7cg")

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="howe to make a tea"
# )

def ansTheQuery(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=text
    )
    return response.text

ansTheQuery("how to make a tea")