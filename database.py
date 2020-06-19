#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import cx_Oracle

from variables import * 

def getConnection():
  logging.debug('Connecting database...')

  try:
    # 한글 떄문에 UTF-8 설정
    connection = cx_Oracle.connect(USER, PASSWORD, cx_Oracle.makedsn(HOST, PORT, SID), encoding = 'utf-8', nencoding="utf-8")
    connection.autocommit = False
    
    logging.debug('Complete database connect!')

    return connection
  except Exception as e:    
    raise e