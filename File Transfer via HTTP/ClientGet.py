import requests

fil = input('Enter File Name: ')

url = "http://localhost:8080/G:/CODING/Junior training/LAB/Networking Lab/Lab 3/Task 2/example_file.txt"

x = requests.get(url)

if x.status_code == 200:
    with open(fil, "wb") as f:
        f.write(x.content)
    print("File successfully received")
    print("Content: ", x.text)
else:
    print("Error: Could not receive file")
