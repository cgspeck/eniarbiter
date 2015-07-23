from collections import defaultdict

import boto.ec2

class AWSApi(object):
    """Object to maintain connection to AWS and manage instances/ENIs"""
    def __init__(self):
        super(AWSApi, self).__init__()
        self.conn = None

    def connect(self, region):
        """
        Boto connect to AWS Region
        """
        self.conn = boto.ec2.connect_to_region(region)

    def get_instances(self, filters):
        """
        Get instances through boto and return them in running / not running buckets
        """
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

    def get_zone_instance_map(self, filters):
        """
        Returns a default dictionary of instances grouped by zone, and then split into all_instances, running, not_running
        and a count of running instances

        { 'ap-southeast-2a': {
            'all_instances': [<instance123>, ...],
            'running': [<instance123>, ...],
            'not_running': [<instance456>, ...],
            },
          'ap-southeast-2b': {
            'all_instances': ...
            }
        }
        """
        count = 0
        all_instances = self.conn.get_only_instances(filters=filters)
        instance_zone_map = defaultdict(lambda: {'all_instances': [], 'running': [], 'not_running': []})

        for instance in all_instances:
            instance_zone_map[instance.placement]['all_instances'].append(instance)
            if instance.state == u'running':
                instance_zone_map[instance.placement]['running'].append(instance)
                count += 1
            else:
                instance_zone_map[instance.placement]['not_running'].append(instance)

        return instance_zone_map, count

    def get_free_enis(self, eni_list):
        """
        Returns a list of eni ids where that eni is in status available
        """
        all_enis = self.conn.get_all_network_interfaces(eni_list)
        return [eni.id for eni in all_enis if eni.status == u'available']

    def get_zone_free_eni_map(self, eni_list):
        """
        Returns a defaultdict in form of { 'zonea': ['eni1', 'eni2', 'eni3'], 'zoneb': ['eni] and count of found enis
        { 'ap-southeast-2a': ['eni123'...], 'ap-southeast-2b', ['eni456'...] }
        """
        count = 0
        eni_zone_map = defaultdict(list)
        for eni in [available_eni for available_eni in self.conn.get_all_network_interfaces(eni_list) if available_eni.status == u'available']:
            eni_zone_map[eni.availability_zone].append(eni.id)
            count += 1

        return eni_zone_map, count

    def attach_eni(self, instance_id, eni_id, device_index, dry_run):
        """
        Calls underlying boto method to attach specified eni to specified instance
        """
        self.conn.attach_network_interface(eni_id, instance_id, device_index, dry_run)

    def get_available_publicips(self, ip_list):
        """
        Returns a list containing available Public IP Address objects which may be a subset of ip_list

        :param ip_list: list of public ip address to query
        "type ip_list: list of strings with literal ip addresses, e.g. ['1.2.3.4', '1.2.3.5'...]

        :returns: list of public ip address objects
        :rtype: list of boto.ec2.address.Address
        """
        return [
            address for address in self.conn.get_all_addresses()
            if address.instance_id is None
            and address.public_ip in ip_list
        ]
