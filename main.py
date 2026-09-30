import os
from dotenv import load_dotenv
import requests


class GithubAPI:
    # constructor
    def __init__(self):
        load_dotenv()
        github_key = os.getenv("GITHUB_TOKEN")

        # specific header to look for a format of the returned data [copied it from google]
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_key}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _fetch_api(self, url, paras=None):
        try:
            response = requests.get(url, headers=self.headers, timeout=10, params=paras)
            # check for any failure in getting data : immediately proceed to exceptoin block (-2)
            response.raise_for_status()
            return response.json()

        # handling exceptions
        except requests.exceptions.Timeout:
            return -1

        except requests.exceptions.HTTPError:
            return -2

        except requests.exceptions.RequestException:
            return -3

    # normal information from github
    def git_info(self):
        data = self._fetch_api(url="https://api.github.com/user")

        if isinstance(data, int):
            return data

        # dictonary format conversion and returning
        info = {
            "name": f"{data['name']}",
            "login_id": f"{data['login']}",
            "public_repos": data["public_repos"],
            "private_repos": data["total_private_repos"],
        }
        return info

    # get github commit data
    def git_commits(self):
        data = self._fetch_api(url="https://api.github.com/user")

        if isinstance(data, int):
            return data

        # Fetch username dynamically so i don't have to hardcode it
        username = data["login"]

        # Search API to find all commits authored by me
        search_url = "https://api.github.com/search/commits"

        # The 'q' parameter lets me search specifically for commits i authored
        params = {
            "q": f"author:{username}",
            "per_page": 1,  # We only need the total_count, so we tell the API to only return 1 item to save data
        }

        stats = self._fetch_api(url=search_url, paras=params)

        if isinstance(stats, int):
            return stats

        return stats["total_count"]

    # github repo lists and links
    def git_repo(self):
        params = {
            "visibility": "all",  # Includes both public and private repos
            "sort": "updated",  # Sorts by most recently updated
            "per_page": 10,  # Limits results to 10 per page (max is 100)
        }

        repos = self._fetch_api(url="https://api.github.com/user/repos", paras=params)

        if isinstance(repos, int):
            return repos

        repo_data = []

        # Loop through the list of dictionaries returned by the API
        for repo in repos:
            name = repo.get("name")
            url = repo.get("html_url")
            is_private = "Private" if repo.get("private") else "Public"

            # store it in a temporaray dictionary
            temp_dict = {"name": name, "url": url, "status": is_private}

            # append it to the repo data (a list of dictionary)
            repo_data.append(temp_dict)

        # fuckin return it
        return repo_data


# just for testing purpose - might delete it later
if __name__ == "__main__":
    my_api = GithubAPI()
    print(my_api.git_info())
    print(my_api.git_repo())
