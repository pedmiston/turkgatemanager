#! /usr/bin/env python
"""
manager.py

Create and manage groups for use with TurkGate.
"""
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from boto.mturk.connection import MTurkConnection

import pandas as pd

class TurkGateManager(object):
    """
    Create and manage groups for use with TurkGate.
    """
    def __init__(self, credentials):
        """
        :param dict credentials: MySQL and AWS credentials obtained via get_credentials.
        """
        mysql_creds = credentials['mysql']
        aws_creds = credentials['aws']
        
        db_url = 'mysql://{user}:{pwd}@{host}:{port}/{db}'.format(**mysql_creds)
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        self.mturk = MTurkConnection(**aws_creds)
    
    def get_groups(self):
        """ 
        .. function:: get_groups(self)
        
        Retrieve unique group names in SurveyRequest.
        
        :return: unique group names
        :rtype: list 
        """
        query_groups = self.session.query(SurveyRequest.groupName).distinct()
        return [group.groupName for group in query_groups]
    
    def get_workers(self):
        """ Retrieve unique worker IDs in SurveyRequest """
        query_ids = self.session.query(SurveyRequest.workerID).distinct()
        return [worker.workerID for worker in query_ids]
    
    def get_requests_by_group(self, group):
        """ Retrieve requests by group name in SurveyRequest """
        query_requests = self.session.query(SurveyRequest)
        return query_requests.filter(SurveyRequest.groupName == group)
    
    def get_workers_by_group(self, group):
        """ Retrieve worker ids for a given group name """
        all_requests = self.get_requests_by_group(group)
        return [request.workerID for request in all_requests]
        
    def add_requests(self, requests):
        """ Add requests to SurveyRequest """
        self.session.add_all(requests)
        self.session.commit()
    
    def remove_requests_by_group(self, group):
        """ Removes a group from the database """
        self.get_requests_by_group(group).delete()
        self.session.commit()
    
    def copy_group(self, existing, new_group):
        """ Copy all requests in existing group to a new group name """
        # TODO: Should be possible to just change the group name
        for request in self.get_requests_by_group(existing):
            new_requests.append(SurveyRequest(workerID=request.workerID,
                                              URL=request.URL,
                                              groupName=new_group,
                                              time=request.time))
        self.add_requests(new_requests)
    
    def rename_group(self, existing, new_group):
        """ Renames a group in the databse """
        self.copy_group(existing, new_group)
        self.remove_requests_by_group(existing)
    
    ############################################################################
    
    def get_recent_hit_titles(self, num_recent=10, num_pages=1):
        """ Retrieve titles of recent HITs """
        all_titles = []
        
        for page in range(1, num_pages+1):
            page_hits = self.mturk.search_hits(sort_by='CreationTime',
                            sort_direction='Descending', page_size=num_recent,
                            page_number=page)
            page_matches = [hit.Title for hit in page_hits]
            all_titles.extend(page_matches)
        
        return all_titles
    
    def get_hit_ids_by_title(self, title, num_recent=10, num_pages=4):
        """ Retrieve HIT ids from HIT title """
        all_matches = []
        
        for page in range(1,num_pages+1):
            page_hits = self.mturk.search_hits(sort_by='CreationTime',
                            sort_direction='Descending', page_size=num_recent,
                            page_number=page)
            page_matches = [hit.HITId for hit in page_hits if hit.Title==title]
            all_matches.extend(page_matches)
        
        return all_matches
    
    def get_assignments_from_hit_id(self, hit_id):
        """ Retrieve assignments based on a hit id """
        num_total = self.mturk.get_assignments(hit_id).TotalNumResults
        num_pages = (int(num_total) / 10) + 1
        
        assignments = []
        for pg in range(1, num_pages+1):
            assignments.extend(self.mturk.get_assignments(hit_id,page_number=pg))
        
        return assignments
    
    def get_assignments_by_title(self, title):
        all_hit_ids = self.get_hit_ids_by_title(title)
        
        all_assignments = []
        for hit_id in all_hit_ids:
            all_assignments.extend(self.get_assignments_from_hit_id(hit_id))
        
        return all_assignments
    
    def make_requests_from_assignments(self, assignments, group, url=None, 
                                       keep_time=True):
        
        dtime = lambda t: datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
        
        if not keep_time:
            dtime = lambda t: None
        
        requests = []
        for assignment in assignments:
            requests.append(SurveyRequest(workerID=assignment.WorkerId,
                                          URL=url, groupName=group,
                                          time=dtime(assignment.SubmitTime)))
        return requests
    
    def make_requests_from_csv(self, results_file, id_col='WorkerId', 
                               time_col='SubmitTime'):
        """ Retrieve requests from HIT results file """
        pass
    
    def make_requests_from_hit_title(self, title, group, url=None,
                                     keep_time=True):
        assignments = self.get_assignments_by_title(title)
        return self.make_requests_from_assignments(assignments, group, url,
                                                   keep_time)
    
    def close(self):
        self.session.close()
        self.mturk.close()
    