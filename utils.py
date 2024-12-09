import requests
import json

def capstoneApi(link):
  api_url = f"http://13.211.145.139:8000/{link}"
  response = requests.get(api_url)
  json_data = response.json()
  return json_data
