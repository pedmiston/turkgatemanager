#! /usr/bin/env/ python
"""
Load credentials for MySQL and AWS
"""
import os
import yaml

def get_credentials(credentials_with_path=None):
    """
    Loads credentials for connecting to MySQL and mTurk
    
    :param credentials_with_path: defaults to 'credentials.yaml' in module directory
    :return: dict containing credentials
    """
    if credentials_with_path is None:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        credentials_with_path = os.path.join(dir_path, 'credentials.yaml')
    return yaml.load(open(credentials_with_path, 'r'))
