#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import database
import parameter

# Batch 관련 클래스
class Batch:

  batchNo = None

  # Batch 클래스 생성자
  def __init__ (self, connection):
    self.connection = connection

  # batchNo 반환
  def getBatchNo (self):
    return self.batchNo

  # 대기(R) 중 인 배치 조회
  def selectPreparedBatchByStatus (self, status, active):
    try:
      cursor = self.connection.cursor()
      cursor.execute(
        ''' SELECT BATCH_NO
              FROM (
                SELECT BATCH_NO 
                  FROM CO_ANALYZER_BATCH
                 WHERE 1=1
                   AND BATCH_STAT = :status
                   AND (
                     SELECT COUNT(bb.BATCH_NO)
                       FROM CO_ANALYZER_BATCH bb
                      WHERE 1=1
                        AND BATCH_STAT = :active
                   ) = 0
                 ORDER BY REQ_DATE ASC 
              )
             WHERE 1=1
               AND ROWNUM = 1 '''
      , { 'status': status, 'active': active })

      self.batchNo = cursor.fetchone()

      if self.batchNo:
        # (x, ) 의 튜플 에서 결과 값인 x 를 변수 (result) 에 추가
        self.batchNo,  = self.batchNo

      cursor.close()
    except Exception as e:
      raise e

  # 대기(R) 중 인 배치 상태를 진행(A) 상태로 변경
  def updateBatchStateByNo (self, status = 'A'):
    if self.batchNo is not None:
      try:
        cursor = self.connection.cursor()
        cursor.execute(
          ''' UPDATE CO_ANALYZER_BATCH
                SET BATCH_STAT = :status
              WHERE 1=1
                AND BATCH_NO = :batchNo '''
        , { 'status': status, 'batchNo': self.batchNo })
        self.connection.commit()
        cursor.close()

        logging.debug('Batch status update to ACTION!')
      except Exception as e:
        self.connection.rollback()
        raise e

  def selectRequestParameter (self):
    if self.batchNo is not None:
      try:
        cursor = self.connection.cursor()
        cursor.execute(
          ''' SELECT QUERY_JSON
                FROM CO_ANALYZER_BATCH
              WHERE 1=1
                AND BATCH_NO = :batchNo '''
        , { 'batchNo': self.batchNo })

        result = cursor.fetchall()

        if len(result) > 0:
          result, = result
          result, = result  
        else:
          self.updateBatchStateByNo('F')
          raise Exception('There is no request parameter')

        parameter.parse(result)
      except Exception as e:
        raise e

  # 대기(R) 중인 배치 작업을 진행(A) 상태로 변경하는 작업 일괄 처리
  def active (self):
    self.selectPreparedBatchByStatus('R', 'A')
    self.updateBatchStateByNo('A')
    self.selectRequestParameter()

  # Connection 종료 및 batchNo 초기화
  def close (self):
    try:
      self.connection.close()
      self.batchNo = None

      logging.debug('Close database connection!')
    except Exception as e:
      raise e
