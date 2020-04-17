from os import environ

import boto3
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def get_new_boto3_session():
    return boto3.session.Session(
      # Credentials have to be set in environment variables
      region_name = environ.get('AWS_REGION') or config['aws']['region_name'],
      aws_access_key_id = environ.get('AWS_ACCESS_KEY_ID') or config['aws']['aws_access_key_id'],
      aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY') or config['aws']['aws_secret_access_key']
    )
