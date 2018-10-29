from __future__ import print_function
from __future__ import absolute_import
import json
import requests

from resources.hackerearth.settings import COMPILE_API_ENDPOINT
from resources.hackerearth.settings import RUN_API_ENDPOINT

from resources.hackerearth.result import CompileResult
from resources.hackerearth.result import RunResult


class HackerEarthAPI(object):
    def __init__(self, params):
        self.params_dict = params.get_params()

    def compile(self):
        response = self.__request(COMPILE_API_ENDPOINT, self.params_dict)
        result = CompileResult(response.text)
        if response.status_code != 200:
            result.valid = False
        else:
            result.valid = True
        return result

    def run(self):
        response = self.__request(RUN_API_ENDPOINT, self.params_dict)
        result = RunResult(response.text)
        if response.status_code != 200:
            result.valid = False
        else:
            result.valid = True
        return result

    def __request(self, url, params):
        response = None
        try:
            response = requests.post(url, data=params)
        except Exception:
            print(Exception)
        return response

    def __result(self, res):
        result = json.load(res)
        return result
