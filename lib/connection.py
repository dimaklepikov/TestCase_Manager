import requests

from creds import TR


class Connection:
    def __init__(self, url, credentials: dict):
        self.url = url
        self.type = "basic_auth"
        self.client = requests
        self.credentials = credentials
        self.auth = None

        # Headers
        self.headers = {
            # TODO: Fix for all cases
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # def __connection_type_dispatcher(self):
        if self.type == "basic_auth":
            self.auth = (
                self.credentials["username"],
                self.credentials["password"]
            )

    def http(self, method, endpoint, **kwargs):
        """Http client"""
        return self.client.request(
            method,
            self.url + endpoint,
            headers=self.headers,
            auth=self.auth, **kwargs
        )


if __name__ == "__main__":
    # Example usage
    connection = Connection(
        "https://testrail.com",
        credentials=TR
    )
    response = connection.http("GET", "https://pluto.testrail.io/index.php?/api/v2/get_sections/3&suite_id=1256")
    print(response.json())