import yaml
import boto3
from botocore.exceptions import ClientError

def load_config():
    with open('config.yml', 'r') as config_file:
      config = yaml.load(config_file)
      return config

def initiate_session(config, client):
    session = boto3.Session(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        region_name='eu-west-1'
    ) 
    print(session)
    client = session.resource(client)
    return client

def upload_file(client, fileobj, bucket, key):
    with open(fileobj, 'rb') as data:
        try:
            client.Bucket(bucket).put_object(
                Body = data,
                Bucket = bucket,
                Key = key,
                ContentType = 'image/jpeg'
            ) 
            print('success')
            return 'success'

        except ClientError as e:
          print('error: %s') % e
          return 'error'

def main():
    config = load_config()
    client = initiate_session(config, 's3')

    fileobj = './static/great_success.jpg'
    bucket = config['upload_bucket']
    key = 'testimg.jpg'

    status = upload_file(client, fileobj, bucket, key)
    return status 

if __name__ == '__main__':
    main()


