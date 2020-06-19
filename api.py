#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
import requests

from variables import *
from urllib3.util.retry import Retry
from requests import Request, Session
from requests.adapters import HTTPAdapter

def post (parameter):
  try:
    retries = Retry(
      total = 5,
      backoff_factor = 0.1,
      status_forcelist = [500, 502, 503, 504],
      method_whitelist = frozenset(['GET', 'POST'])
    )

    headers = { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' }

    with Session() as s:
      s.mount('http://', HTTPAdapter(max_retries=retries))

      response = s.post(TM2_URL, data=parameter, headers=headers, timeout=60000)
      response.encoding = 'utf-8'
      response = response.text
      response = json.loads(response)

      return response
  except requests.HTTPError as e:
    raise e
  except Exception as e:
    raise e