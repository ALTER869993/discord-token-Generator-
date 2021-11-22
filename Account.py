import requests
import random
import string
import time
import colorama
import sys
import json

from colorama import Fore, Style
from time import sleep

with open('config.json') as r:
	config = json.load(r)

captcha_api_key = config.get('CaptchaKey')

discord_register_url = "https://discord.com/api/v9/auth/register"

captcha_submit_url = "http://2captcha.com/in.php"

captcha_get_url = "http://2captcha.com/res.php"

discord_hcaptcha_id = "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34"

discord_captcha_register = "https://discord.com/register"

p_list = []


def typewritter(text):
    for x in text:
        print(x, end="")
        sys.stdout.flush()
        sleep(0.1)


def write_token_to_file(token, password, email):
    with open("accounts.txt", "a") as fhandle:
        fhandle.write(f"{token} | {password} | {email}\n")


def generate_random_data():
    password = "".join(
        random.choice(string.ascii_letters) for i in range(0, 20)
    ) + "".join(random.choice(string.digits) for i in range(0, 10))
    email = (
        "".join(random.choice(string.ascii_letters) for i in range(0, 20))
        + "".join(random.choice(string.digits) for i in range(0, 10))
        + "@gmail.com"
    )
    username = "".join(
        random.choice(string.ascii_letters) for i in range(0, 7)
    ) + "".join(random.choice(string.digits) for i in range(0, 10))
    fingerprint = "".join(
        random.choice(string.ascii_letters) for i in range(0, 40)
    ) + "".join(random.choice(string.digits) for i in range(0, 10))
    return [password, email, username, fingerprint]


def submit_captcha_key():
    url = "http://2captcha.com/in.php"
    querystring = {
        "key": captcha_api_key,
        "method": "hcaptcha",
        "sitekey": discord_hcaptcha_id,
        "pageurl": discord_captcha_register,
    }
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    return response.text.split("|", 1)[1]


def get_discord_captcha(captcha_key_response):
    params = {"key": captcha_api_key, "action": "get", "id": captcha_key_response}
    captcha_final_request = requests.get(url=captcha_get_url, params=params)
    return captcha_final_request.text.split("|", 1)


def create_discord_account(captcha_key):
    big_random_data = generate_random_data()
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    params = {
        "fingerprint": big_random_data[3],
        "email": big_random_data[1],
        "username": big_random_data[2],
        "password": big_random_data[0],
        "consent": True,
        "date_of_birth": "2000-04-05",
        "captcha_key": captcha_key,
    }
    make_token_request = requests.post(
        url=discord_register_url, json=params, headers=headers
    )
    try:
        write_token_to_file(
        	make_token_request.json()["token"], big_random_data[0], big_random_data[1]
        )
        print("Token Saved To File")
        print(f"Token Password: {big_random_data[0]}")
        print(f"Token Email: {big_random_data[1]}")
    except:
        print("Being Rate Limited Or Token Failure")
    print("-" * len(big_random_data[1]))


def main():
    captcha_step_one = submit_captcha_key()
    print(f"\n{captcha_step_one}")
    while True:
        time.sleep(10)
        captcha_step_two = get_discord_captcha(captcha_step_one)
        try:
            if len(captcha_step_two[1]) > 60:
                print("Token Created")
                create_discord_account(captcha_key=captcha_step_two[1])
                looping = False
        except IndexError:
            print("Token Captcha Not Ready")


if __name__ == "__main__":
    typewritter("https://github.com/3v1")
    main()
