import openai

# from src.schemas import UserModel
from dotenv import dotenv_values


config = dotenv_values(".env")
openai.api_key = config.get("GTPAPIKEY")


"""
username='andrii' email='osandreyman@gmail.com'
age=32 sex='male' 
interests='Python back-end development'

"""
def generate_avatar(body) -> str|None:
    email_prefix = body.email.split("@")[0]
    prompt = f"Generate me an avatar for somebody who named {body.username}," \
    f"with nickname {email_prefix}, his age is {body.age} and gender is {body.sex}, interests are {body.interests}"
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
        )
        print(prompt)
        image_url = response['data'][0]['url']
        print(response, image_url, sep="\n")
        return image_url
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)



if __name__ == '__main__':
    generate_avatar(body=None)