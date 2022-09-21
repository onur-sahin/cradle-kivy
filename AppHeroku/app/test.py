import requests

# resp = requests.post("http://127.0.0.1:8080/predict", files={"file":open("test.wav", "rb")})


resp = requests.post("http://cradle-server.herokuapp.com/predict",
                      files={"file":open("yeni2.wav", "rb")})


# resp = requests.post("http://localhost:5000/predict",
#                       files={"file":open("test.wav", "rb")})

print(resp.text)


