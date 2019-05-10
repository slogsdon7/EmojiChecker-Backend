import botocore.exceptions
from boto3.session import Session
from django.conf import settings


class SMS():
    exceptions = ['AuthorizationError', 'EndpointDisabled', 'FilterPolicyLimitExceeded', 'InternalError',
                  'InvalidParameter', 'ParameterValueInvalid', 'NotFound', 'PlatformApplicationDisabled',
                  'SubscriptionLimitExceeded', 'Throttled', 'TopicLimitExceeded']
    def __init__(self,  message):
        self.message = message
        if hasattr(settings, 'SNS_SEND') and settings.SNS_SEND:
            session = Session(aws_access_key_id=settings.SNS_ID,
                              aws_secret_access_key=settings.SNS_KEY,
                              region_name=settings.SNS_REGION)
            self.client = session.client(service_name='sns')


    def send(self, phone_number):
        if hasattr(settings, 'SNS_SEND') and settings.SNS_SEND:
            try:
                response = self.client.publish(PhoneNumber=phone_number, Message=self.message)
            except botocore.exceptions.ClientError as error:
                response = error
        else:
            response = {'MessageID': 'Test'}
        return response
