#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging

import api

def parse (data):
  parameters = [ json.loads(unicode(p, 'utf-8')) for p in data.read().split(',,') if p != '' ]
  
  logging.info(parameters[0]['data'])
  
  try:
    api.post(parameters[0]['data'])
  except Exception as e:
    raise e

  