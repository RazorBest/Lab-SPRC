import requests
import json

URL = "https://sprc.dfilip.xyz/lab1"

def task1():
    check_url = URL + "/task1/check"
    payload = {
        "secret": "SPRCisNice",
    }
    params = {
        "nume": "Marius Razvan Pricop", 
        "grupa": "343C1",
    }
    headers = {
        "secret2": "SPRCisBest",
    }

    print("Task1:")
    r = requests.post(check_url, params=params, headers=headers, data=payload)
    print(json.loads(r.text))

def task2():
    task_url = URL + "/task2"
    payload = {
        "username": "sprc",
        "password": "admin",
        "nume": "Marius Razvan Pricop",
    }

    r = requests.post(task_url, data=json.dumps(payload))
    print("Task2: ")
    print(json.loads(r.text))

def task3():
    login_url = URL + "/task3/login"
    check_url = URL + "/task3/check"
    payload = {
        "username": "sprc",
        "password": "admin",
        "nume": "Marius Razvan Pricop",
    }

    s = requests.Session()
    s.post(login_url, data=json.dumps(payload))
    r = s.get(check_url)
    
    print("Task3:")
    print(json.loads(r.text))

def main():
    task1()
    task2()
    task3()

if __name__ == "__main__":
    main()
