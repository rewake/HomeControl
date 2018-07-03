import boto3
from boto3.dynamodb.conditions import Key, Attr


class DynamoTable(object):
    """

    """
    def __init__(self, table):
        self.db = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = self.db.Table(table)

    def get_all(self):
        return self.table.scan()

    def get_by_attribute(self, attr, group):
        """
        Search for schedules based on group
        :param attr:
        :param group:
        :return:
        """
        print "Scanning by attribute: " + attr + " = " + group

        return self.table.scan(
            FilterExpression=Attr(attr).eq(group) and Attr('mode').eq(0)
        )['Items']
