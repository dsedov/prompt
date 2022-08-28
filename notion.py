import yaml, os, requests, json
from time import sleep

class Notion:
    def __init__(self, config_file):
        self.config = yaml.safe_load(open(config_file))
    def headers(self):
        access_key = self.config["notion"]["access_key"]
        return    {"Authorization" : access_key,
                  "Content-Type" : "application/json",
                  "Notion-Version": "2022-02-22"}
    def filtered_prompts(self, query):
        prompts = []
        
        database_id = self.config["notion"]["prompt_db"]

        headers = self.headers()
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, headers = headers, data = json.dumps(query))
        if response.status_code == 200:
            data = json.loads(response.content)
            results = data["results"]
            if data["has_more"]:
                while data["has_more"]:
                    sleep(0.3)
                    query["start_cursor"] = data["next_cursor"]
                    response = requests.post(url, headers = headers, data = json.dumps(query))
                    if response.status_code == 200:
                        data = json.loads(response.content)
                        results = results + data["results"]
                    else: break

            for result in results:
                prompt = {}
                prompt["prompt"] = result["properties"]["prompt"]["title"][0]["plain_text"]
                prompt["id"] = result["id"]
                prompts.append(prompt)
        return prompts
    def filtered_artists(self, query):
        artists = []
        
        database_id = self.config["notion"]["artist_db"]

        headers = self.headers()
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, headers = headers, data = json.dumps(query))
        if response.status_code == 200:
            data = json.loads(response.content)
            results = data["results"]
            if data["has_more"]:
                while data["has_more"]:
                    sleep(0.3)
                    query["start_cursor"] = data["next_cursor"]
                    response = requests.post(url, headers = headers, data = json.dumps(query))
                    if response.status_code == 200:
                        data = json.loads(response.content)
                        results = results + data["results"]
                    else: break

            for result in results:
                artist = {}
                artist["name"] = result["properties"]["name"]["title"][0]["plain_text"]
                artist["id"] = result["id"]
                artists.append(artist)
        return artists
    def artist_study_prompts(self):
        return self.filtered_prompts({
                    "filter": {
                        "property": "tags",
                        "multi_select": {
                            "contains": "artist_study"
                        }
                    },
                    "sorts": [{
                        "property": "prompt",
                        "direction": "ascending"
                    }]
                 })
    def fav_artists(self):
        return self.filtered_artists({
                    "filter": {
                        "property": "Fav",
                        "checkbox": {
                            "equals": True
                        }
                    },
                    "sorts": [{
                        "property": "name",
                        "direction": "ascending"
                    }]
                 })
    def empty_coherance_artists(self):
        return self.filtered_artists({
                    "filter": {
                        "property": "Coherence",
                        "number": {
                            "is_empty": True
                        }
                    },
                    "sorts": [{
                        "property": "name",
                        "direction": "ascending"
                    }]
                 })
#n = Notion("config.yaml")
#prompts = n.artist_study_prompts()
#print(prompts)

