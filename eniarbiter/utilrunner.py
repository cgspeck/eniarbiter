import argparse
import json
import logging
import sys

from awsapi import AWSApi


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger

def main():
    parser = argparse.ArgumentParser(
        description="Elastic Network Interface Arbiter"
    )
    parser.add_argument(
        "config", help="The configuration JSON to read", action="store", nargs=1, type=argparse.FileType('r')
    )
    parser.add_argument(
        "-c", "--dry-run", help="Print findings but don't actually detach/attach interfaces", action="store_true"
    )
    args = parser.parse_args()

    config = json.loads(args.config[0].read())

    assert 'region' in config
    assert 'eni_list' in config
    assert 'instance_tag_spec' in config

    logger = setup_logging()

    a = AWSApi()
    logger.info('Connecting to AWS...')
    a.connect(config['region'])
    logger.info('Retrieving ENIs...')
    eni_list = config['eni_list']

    zone_freeenis, count = a.get_zone_free_eni_map(eni_list)

    logger.info('%s available ENIS' % count)

    zone_instances, count = a.get_zone_instance_map(config['instance_tag_spec'])
    logger.info('%s running matching instances' % count)

    failed = False

    for zone, instances in zone_instances.iteritems():
        for instance in instances['running']:
            if bool(set(eni_list) & set(interface.id for interface in instance.interfaces)):
                logger.info('Instance %s already has a specified ENI attached' % instance.id)
            else:

                if len(zone_freeenis[zone]) > 0:
                    allocated_eni = zone_freeenis[zone].pop()
                    device_index = len(instance.interfaces)
                    if args.dry_run:
                        logger.info('Propose attaching interface %s to instance %s as eth%s' % (allocated_eni, instance.id, device_index))
                    else:
                        logger.info('Attaching interface %s to instance %s as eth%s' % (allocated_eni, instance.id, device_index))
                        a.attach_eni(instance.id, allocated_eni, device_index, dry_run=args.dry_run)
                else:
                    logger.critical('No available ENIs in zone %s to attach to instance %s' % (zone, instance))
                    failed = True

    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
