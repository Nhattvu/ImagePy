import requests
import json
from requests.models import Response


class MakeApiCall:

    def get_user_data(self, api, parameters):
        try:
            response = requests.get(f"{api}", params=parameters, timeout=2)
        
        except requests.exceptions.RequestException as e:
            # Handles website unreachable
            response = Response()
            response.status_code = 408
            response._content = "Timeout"

        if response.status_code == 200:
            print("sucessfully fetched the data with parameters provided")
            text = json.dumps(response.json(), sort_keys=True, indent=4)
            print(text)
        else:
            print(
                f"Failed to connect to basili.bid API, {response.status_code} error")

        return response.status_code

 

    def __init__(self, api):
        # self.get_data(api)

        parameters = {
            "username": "myusername"
        }
        self.get_user_data(api, parameters)


if __name__ == "__main__":
    api_call = MakeApiCall("https://imagesuiteapi.basili.bid/health_check")