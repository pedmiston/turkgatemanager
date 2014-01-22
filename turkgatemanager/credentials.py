#! /usr/bin/env/ python
"""
Load credentials for MySQL and AWS
"""
import os
import yaml

def get_credentials(credentials_with_path=None):
    if credentials_with_path is None:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        credentials_with_path = os.path.join(dir_path, 'credentials.yaml')
    return yaml.load(open(credentials_with_path, 'r'))
