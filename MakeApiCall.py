import requests
import json


class MakeApiCall:

    def get_user_data(self, api, parameters):
        response = requests.get(f"{api}", params=parameters)
        if response.status_code == 200:
            print("sucessfully fetched the data with parameters provided")
            text = json.dumps(response.json(), sort_keys=True, indent=4)
            print(text)
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

        return response.status_code

 

    def __init__(self, api):
        # self.get_data(api)

        parameters = {
            "username": "kedark"
        }
        self.get_user_data(api, parameters)


if __name__ == "__main__":
    api_call = MakeApiCall("https://imagesuiteapi.basili.bid/health_check")