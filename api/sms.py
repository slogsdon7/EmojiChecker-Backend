import boto3

class SMS():
    def __init__(self,  message):
        self.message = message
        self.client = boto3.client('sns')

    def send(self, phone_number):
        """for now returns only returns True for the sake of writing code that uses this command"""
        #response = self.client.publish(PhoneNumber=phone_number, Message=self.message)
        return True
