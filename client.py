import requests

response = requests.get("http://127.0.0.1:8000/api/valute")
data = response.json()

print("USD:", data["USD"])
print("RUB:", data["RUB"])
print("CNY:", data["CNY"])
