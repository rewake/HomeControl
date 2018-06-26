import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoTable:
    """

    """
    def __init__(self, table):
        self.db = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = self.db.Table(table)

    def get_all(self):
        return self.table.scan()

    def get_by_group(self, group):
        """
        Search for schedules based on group
        :param group:
        :return:
        """
        return self.table.query(
            KeyConditionExpression=Key('group').eq(group)
        )
