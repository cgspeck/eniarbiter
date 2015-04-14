import boto.ec2

class AWSApi(object):
    """Object to maintain connection to AWS and manage instances/ENIs"""
    def __init__(self):
        super(AWSApi, self).__init__()
        self.conn = None

    def connect(self, region):
        '''
        Boto connect to AWS Region
        '''
        self.conn = boto.ec2.connect_to_region(region)

    def get_instances(self, filters):
        '''
        Get instances through boto and return them in running / not running buckets
        '''
        all_instances = self.conn.get_only_instances(filters=filters)
        running_list = []
        not_running_list = []

        for instance in all_instances:
            if instance.state == u'running':
                running_list.append(instance)
            else:
                not_running_list.append(instance)

        return {
            'all_instances': all_instances,
            'running': running_list,
            'not_running': not_running_list
        }

    def get_free_enis(self, eni_list):
        '''
        Returns a list of eni ids where that eni is in status avaliable
        '''
        all_enis = self.conn.get_all_network_interfaces(eni_list)
        return [eni.id for eni in all_enis if eni.status == u'available']

    def attach_eni(self, instance_id, eni_id, device_index, dry_run):
        '''
        Calls underlying boto method to attach specified eni to specified instance
        '''
        self.conn.attach_network_interface(eni_id, instance_id, device_index, dry_run)
