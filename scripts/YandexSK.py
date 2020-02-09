import subprocess
import requests


def refresh_token():
    try:
        out = subprocess.check_output("getToken.bat", stderr=subprocess.STDOUT)
        res = out.decode("utf-8")
        start = res.find("iamToken")
        end = res.find("expiresAt")
        token = res[start + 12:end - 5]
        f = open('SpeechKitToken.txt', 'w')
        f.write(token)
        f.close()
    except Exception as e:
        pass


def get_token():
    f = open('scripts/SpeechKitToken.txt', 'r')
    for line in f:
        f.close()
        return line


def synthesize(folder_id, iam_token, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'voice': 'oksana',
        'emotion': 'good',
        'folderId': folder_id
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def save_file(name, text):
    folder_id = "your folder id"
    with open("audio/" + name + ".ogg", "wb") as f:
        for audio_content in synthesize(folder_id, get_token(), text):
            f.write(audio_content)
