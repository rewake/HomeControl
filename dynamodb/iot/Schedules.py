from dynamodb import DynamoTable
import boto3


class Schedules(DynamoTable):
    """
    Reads schedules from AWS DynamoDB (iot.schedules table)
    """

    def __init__(self):
        DynamoTable.__init__(self, 'iot.schedules')
