import openai

openai.api_key = "12345667"

# pylint: disable=no-member
response = openai.ChatCompletion.create(
 model="gpt-4",
 messages=[
 {"role": "user", "content": "Hello, how are you?"}
 ]
 )

print(response)
