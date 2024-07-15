import requests
from dotenv import load_dotenv
import os
load_dotenv()
class Session(requests.Session):
    def __init__(self, base_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://api.clickup.com/api/v2"

    def request(self, method, url, *args, **kwargs):
        if self.base_url:
            url = self.base_url + url
        headers = kwargs.get('headers', {})
        headers['Authorization'] = "pk_74545570_U9HXYVA5CWVZSOHLEDWJCV0IQFKEECEG"
        kwargs['headers'] = headers
        return super().request(method, url, *args, **kwargs)
