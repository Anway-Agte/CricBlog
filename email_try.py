import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox5e07cf77fcba42008bac1035c713fd6f.mailgun.org",
        auth=("api", "16af08ff3ff3ecb081fdf991463f2b43-28d78af2-31a0a10b"),
        data={
            "from": "Excited User <mailgun@sandbox5e07cf77fcba42008bac1035c713fd6f.mailgun.org>",
            "to": [
                "anway.agte@gmail.com",
                "YOU@sandbox5e07cf77fcba42008bac1035c713fd6f.mailgun.org",
            ],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomness!",
        },
    )


result = send_simple_message()
print(result.text)