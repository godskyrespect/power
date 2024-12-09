import requests
import json

def RequestApi(link):
  api_url = f"http://13.211.145.139:8000/{link}"
  response = requests.get(api_url)
  json_data = response.json()
  return json_data

def RequestPost(data):
  api_url = "http://13.211.145.139:8000/school/upload"
  response = requests.post(url, json=data)
  return response.status_code
