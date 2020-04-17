import timeout_decorator
from os import environ
from logger import Logger
from boto_session import get_new_boto3_session

############ Firebase libraries ############
''' import firebase_admin
from firebase_admin import credentials
from firebase_admin import db '''

############ AWS libraries #################

############ Configuration #################
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

train_id = environ.get('TRAIN_ID') or environ.get('RESIN_DEVICE_UUID') or config['default']['train_id']
timeout_seconds = 15

######### Configure Firebase object #############
''' cred = credentials.Certificate("credentials/traintraintrain-bb07a.json")
firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://traintraintrain-bb07a.firebaseio.com/'
})

ref = db.reference('raw-data/' + train_id)

######### Push to Firebase #############
@timeout_decorator.timeout(timeout_seconds)
def pushToFirebase(input):
  logger.log("Pushing to firebase")
  ref.push({
    'local_time': str(input['time']),
    'server_time': {'.sv': 'timestamp'},
    'data': input['result']
  })'''

######### Configure DynamoDB object #############
session = get_new_boto3_session()

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('traintraintrain_raw_scans')
logger = Logger('database', boto3_session=session)

######### Push to DynamoDB #############

@timeout_decorator.timeout(timeout_seconds)
def pushToDynamoDB(input):
  logger.log("Pushing to DynamoDB")
  table.put_item(
    Item={
      'train_id': train_id,
      'timestamp': str(input['time']),
      'data': input['result']
    }
  )
  logger.log("Finished pushing to DynamoDB")
