import boto3


class Schedules:
    """
    Reads schedules from AWS DynamoDB (iot.schedules table)
    """

    def __init__(self):
        self.db = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = self.db.Table('iot.schedules')

    def get(self, category):
        return self.table.scan()
