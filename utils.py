import requests
import json

def request_api(link):
  api_url = f"http://13.211.145.139:8000/{link}"
  response = requests.get(url_school)
  json_data = response.json()
  return json_data
