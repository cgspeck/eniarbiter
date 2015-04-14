import boto.ec2

class AWSApi(object):
    """Object to maintain connection to AWS and manage instances/ENIs"""
    def __init__(self, arg):
        super(AWSApi, self).__init__()
        self.arg = arg

    def connect(self):
        pass

    def get_instances(self, filter):
        pass

    def attach_eni(self, instance, eni):
        pass

    def detach_eni(self, instance, eni):
        pass

        