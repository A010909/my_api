import os
from dotenv import load_dotenv
import requests

class lastfmAPI:

    def __init__(self):

        load_dotenv()
        lastfm_key = os.getenv("LASTFM_TOKEN")
        lastfm_user = os.getenv("LASTFM_USER")

        # A base parameter that will be used by all functions
        self.base_params = {
            "api_key" : lastfm_key,
            "format" : "json",
            "user" : lastfm_user
        }

    def _fetch_api(self, payload):

        # final parameter 
        final_para = {**self.base_params, **payload}

        try:
            response = requests.get("https://ws.audioscrobbler.com/2.0/", params=final_para, timeout=10)
            response.raise_for_status()
            return response.json()
        
        # handling exceptions
        except requests.exceptions.Timeout:
            return -1

        except requests.exceptions.HTTPError:
            return -2

        except requests.exceptions.RequestException:
            return -3
    
    def get_current_status(self):

        payload = {
            "method" : "user.getrecenttracks",
            "limit" : 1
        }
        
        result = self._fetch_api(payload=payload)

        if isinstance(result, int):
            return result

        attr = result["recenttracks"]["@attr"]
        data = {"count" : attr["total"]}

        tracks_list = result["recenttracks"]["track"]
        if tracks_list:  # If the list is not empty
            track = tracks_list[0]
            if "@attr" in track:
                data["currently_playing"] = track["name"]
                data["artist"] = track["artist"]["#text"]

        return data
    
    def get_top_tracks(self, time_period=None):

        payload = {
            "method" : "user.gettoptracks",
            "limit" : 1
        }

        if time_period!=None:
            payload["period"] = time_period 
        
        result = self._fetch_api(payload=payload)

        if isinstance(result, int):
            return result
        
        data = {}
        top = result["toptracks"]["track"]
        if top:
            top = top[0]
            data = {
                "name" : top["name"],
                "artist" : top["artist"]["name"],
                "playcount" : top["playcount"]
            }
        
        return data
    
    # holyyyy fuckkk, what the hell did i write dayyyymmmmmmm
    # its a fuckin self healing code. 
    def get_vibe(self):

        payload = {
            "method" : "track.gettoptags",
            "autocorrect" : 1
        }

        # if any song is currently playing, then the vibe will show from that...
        track_data = self.get_current_status()
        if "currently_playing" in track_data:
            payload.update({"track" : track_data["currently_playing"], "artist" : track_data["artist"]})

            result = self._fetch_api(payload=payload)

            if isinstance(result, int) or result["toptags"]["tag"] == [] :
                # sometimes the artist name and track gets swapped due to naming read errrors in scrbbler app on phone
                payload.update({"track" : track_data["artist"], "artist" : track_data["currently_playing"]})

                result = self._fetch_api(payload=payload)

                # if still error
                if isinstance(result, int):
                    return result
        else:
            # always get vibe from the minimum parameter (which is 7 day) so that the user connects with his recent vibe
            track_data = self.get_top_tracks("7day")
            payload.update({"track" : track_data["name"], "artist" : track_data["artist"]})

            result = self._fetch_api(payload=payload)

            if isinstance(result, int) or result["toptags"]["tag"] == []:
                # sometimes the artist name and track gets swapped due to naming read errrors in scrbbler app on phone
                payload.update({"track" : track_data["artist"], "artist" : track_data["name"]})

                result = self._fetch_api(payload=payload)

                # if still error
                if isinstance(result, int):
                    return result
        
        try:
            return result["toptags"]["tag"][0]["name"]
        except (IndexError, KeyError):
            return -1

# uncomment this if you want to test
# if __name__ == "__main__":
#     my_music = lastfmAPI()
#     print(my_music.get_current_status())
#     print("\n")
#     print(my_music.get_top_tracks())
#     print("\n")
#     print(my_music.get_vibe())
#     print("\n")
