import requests

if __name__ == "__main__":
    headers = {
    "ser-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    url = "https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial/42.056071,-87.673899?zl=15&o=xml&key=AkgDxxiFx5q-IupXs55G9S8mRKza78MbGjexT2xx_Et_qpBZ0Wjp86jS15EgdY55"
    response = requests.get(url=url, params=params, headers=headers).text
    print(response)