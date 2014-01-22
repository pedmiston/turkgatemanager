#! /usr/bin/env python
"""
manager.py

Create and manage groups for use with TurkGate.
"""
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from boto.mturk.connection import MTurkConnection

class TurkGateManager(object):
    """
    Create and manage groups for use with TurkGate.
    """
    def __init__(self, user, pwd, host, port, db, aws_key=None, aws_id=None):
        """
        :Parameters:
            user : username for MySQL database
            pwd : password for MySQL user
            port : MySQL port, defaults to 3306
            db : name of MySQL database with the SurveyRequest table
            aws_key : AWS access key id
            aws_id : AWS secret access id
        """
        # MySQL config
        db_url = 'mysql://{user}:{pwd}@{host}:{port}/{db}'.format(
                     user=user, pwd=pwd, host=host, port=port, db=db)
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        # boto config
        if aws_key and aws_id:
            self.mturk = MTurkConnection(aws_key, aws_id)
    
    def get_groups(self):
        """ Retrieve unique group names in SurveyRequest """
        query_groups = self.session.query(SurveyRequest.groupName).distinct()
        group_names = [group.groupName for group in query_groups]
        return group_names
    
    def get_requests(self):
        """ Retrieve unique worker IDs in SurveyRequest """
        query_ids = self.session.query(SurveyRequest.workerID).distinct()
        worker_ids = [worker.workerID for worker in query_ids]
        return worker_ids
    
    def get_requests_by_group(self, group):
        """ Retrieve requests by group name in SurveyRequest """
        query_requests = self.session.query(SurveyRequest).filter(
            SurveyRequest.groupName == group)
        ids_in_group = [request.workerID for request in query_requests]
        return ids_in_group
    
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
    
    def make_requests_from_hit(self, hit_ids):
        """ Retrieve requests from HIT ids """
        dtime = lambda t: datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
        
        if not isinstance(hit_ids, list):
            hit_ids = [hit_ids,]
        
        all_requests = []
        for hit_id in hit_ids:
            num_total = self.mturk.get_assignments(hit_id).TotalNumResults
            num_pages = (int(num_total) / 10) + 1
            
            for page in range(1, num_pages+1):
                assignmts = self.mturk.get_assignments(hit_id, page_number=page)
                requests = [(assign.WorkerId, dtime(assign.SubmitTime)) \
                         for assign in assignmts]
                all_requests.extend(requests)
        
        return all_requests
    
    def make_requests_from_csv(self, results_file, id_col='WorkerId', 
                               time_col='SubmitTime'):
        """ Retrieve requests from HIT results file """
        import pandas as pd
        
        results = pd.read_csv(ids_file)[[id_col, time_col]]
        results[time_col] = pd.to_datetime(results[time_col]).astype(datetime)
        worker_ids = [(worker_id, submit_time) for (worker_id, submit_time) in \
                      results.itertuples(index=False)]
        return worker_ids
    
    def add_requests_to_group(self, assignments, group):
        """ Add requests to SurveyRequest """
        requests = [SurveyRequest(workerID=workerID,groupName=group,time=time) \
                        for workerID, time in assignments]
        self.session.add_all(requests)
        self.session.commit()
        
    def remove_requests_by_group(self, group):
        """ Removes a group from the database """
        self.session.query(SurveyRequest).filter(
            SurveyRequest.groupName == group).delete()
        self.session.commit()
    
    def copy_group(self, existing, new_group):
        """ Copy all requests in existing group to a new group name """
        pass
    
    def rename_group(self, existing, new_group):
        """ Renames a group in the databse """
        pass
        
    def close(self):
        self.session.close()
        self.mturk.close()
    