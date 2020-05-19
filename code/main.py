import requests
import urllib
import os

if __name__ == "__main__":
    headers = {
    "ser-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }   
    prefix = 'https://dev.virtualearth.net/REST/v1/Imagery/Map/'
    imagerySet = 'AerialWithLabels'
    mapArea = '42.049475,-87.678077,42.060154,-87.668861'
    mapSize = '4000,4000'
    bingKey = 'AkgDxxiFx5q-IupXs55G9S8mRKza78MbGjexT2xx_Et_qpBZ0Wjp86jS15EgdY55'
    imgUrl = '{0}{1}?mapArea={2}&mapSize={3}&key={4}&mapMetadata={5}'.format(prefix, imagerySet, mapArea, mapSize, bingKey, 0)
    print(imgUrl)
    metaUrl = '{0}{1}?mapArea={2}&mapSize={3}&key={4}&mapMetadata={5}'.format(prefix, imagerySet, mapArea, mapSize, bingKey, 1)
    print(metaUrl)
    response = requests.get(url=imgUrl, headers=headers)
    with open('{0}.jpg'.format(imagerySet), 'wb') as f:
        f.write(response.content)
        f.flush()
