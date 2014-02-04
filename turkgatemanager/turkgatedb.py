#! /usr/bin/env/ python
"""
turkgatedb.py

Configuration for connecting to a TurkGate MySQL database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()
class SurveyRequest(Base):
    """
    Implement target table in a python class for use with sqlalchemy engine
    
    Assumes TurkGate defaults.
    """
    __tablename__ = 'SurveyRequest'
    
    requestID = Column(Integer, primary_key=True)
    workerID = Column(String)
    URL = Column(String)
    groupName = Column(String)
    time = Column(DateTime)
    
    def __repr__(self):
        return "<SurveyRequest(workerID={0}, URL={1}, \
                groupName={2}, time={3})".format(
                self.workerID, self.URL, self.groupName, self.time)