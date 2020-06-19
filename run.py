#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import database

from execute import Batch

logging.basicConfig(
  level=logging.DEBUG,
  filename='tm-batch.log', 
  format='%(asctime)s - %(name)s - %(levelname)s => %(message)s')

if __name__ == '__main__':
  try:
    connection = database.getConnection();

    if connection:
      batch = Batch(connection)
      batch.active()
      batch.close()
    else:
      logging.debug('Database connection is Null!')
  except Exception as e:
    logging.error(e, exc_info=True)
    logging.debug('Close batch module...')