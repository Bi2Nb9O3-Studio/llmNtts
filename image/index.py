import os
import pick
import requests
import easygui
from sympy import im

AZURE_API_KEY = "GB5XtDKii3M2qBOPsSAQtR3CEyzbbbF1ZgCQU0uc0MvvuCloLQIpJQQJ99BEACfhMk5XJ3w3AAAAACOG9438"
AZURE_ENDPOINT = "https://10227-maawb1pl-swedencentral.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AZURE_API_KEY}"
}


def generate(prompt, size="1024x1024", style="vivid", quality="standard", n=1):
    """
    Generate an image using the DALL-E model.

    Args:
        prompt (str): The text prompt to generate the image.
        size (str): The size of the generated image. Default is "1024x1024".
        style (str): The style of the generated image. Default is "vivid".
        quality (str): The quality of the generated image. Default is "standard".
        n (int): The number of images to generate. Default is 1.

    Returns:
        dict: The response from the API containing the generated image(s).
    """
    print("")
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": size,
        "style": style,
        "quality": quality,
        "n": n
    }
    print("Posting request.")
    response = requests.post(AZURE_ENDPOINT, headers=header, json=data)
    if response.status_code == 200:
        print("Request successful, processing response...")
        resp = response.json()
    else:
        if response.status_code == 429:
            print("Rate limit exceeded. Please try again later.")
            return
        if response.status_code == 400:
            print(f"{response.json()['error']['message']}")
            return
        raise Exception(f"Error: {response.status_code}, {response.text}")
    print("Downloading image...")
    image_url = resp['data'][0]['url']
    with open(f"{resp['created']}.jpg", "wb") as f:
        f.write(requests.get(image_url).content)
    print(f"Image saved as {resp['created']}.jpg")
    print(f"Final prompt: {resp['data'][0]['revised_prompt']}")
    os.startfile(f"{resp['created']}.jpg")
    print("")


while True:
    try:
        try:
            prompt = input("Enter your prompt:")
            if not prompt:
                print("Prompt cannot be empty.")
                continue
            size = pick.pick(title="Select image size:", options=[
                             '1024x1024', '1792x1024', '1024x1792'])[0]
            style = pick.pick(title="Select image style:",
                              options=['vivid', 'natural'])[0]
            quality = pick.pick(title="Select image quality:",
                                options=["standard", "hd"])[0]
            # n = int(input("Enter number of images to generate:"))
            n=1
        except Exception as e:
            print("Input invalid:", e)

        generate(prompt, size, style, quality, n)
    except KeyboardInterrupt:
        print("Exiting...")
        break
