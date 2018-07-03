from dynamodb import DynamoTable
from boto3.dynamodb.conditions import Key, Attr


class Schedules(DynamoTable):
    """
    Reads schedules from AWS DynamoDB (iot.schedules table)
    """

    def __init__(self):
        super(Schedules, self).__init__('iot.schedules')

    def today(self, group):
        return sorted(self.table.scan(
            FilterExpression=Attr('group').eq(group)
        )['Items'], key=lambda k: ['time'])
