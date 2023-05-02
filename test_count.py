#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Fetch places
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/cities/{}/places".format("nop"))
    print(r.status_code)
