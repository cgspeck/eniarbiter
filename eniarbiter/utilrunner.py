import argparse
import os
import json
import sys

from awsapi import AWSApi


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

    #from ipdb import set_trace; set_trace()

    config = json.loads(args.config[0].read())

    assert 'eni_list' in config
    assert 'instance_tag_spec' in config

    sys.exit()


    # instances = find_instances()

    # for instance in instances['unhealthy']:
    #     if instances_has_relevant_eni:
    #         detach_eni(instance)

    # for instance in instances['healthy']:
    #     if not instances_has_relevant_eni:
    #         attach_eni(instance)

    # for f_name in file_list:
    #     print('Loading {0}'.format(f_name))
    #     qr.load(f_name)

    #     if args.overwrite:
    #         print('Saving over original')
    #         qr.save(f_name)
    #     else:
    #         new_file_name = '{pre}_reduced.{extension}'.format(
    #             pre=''.join(f_name.split('.')[:1]), extension=''.join(f_name.split('.')[1:]))
    #         print('Saving to {0}'.format(new_file_name))
    #         qr.save(new_file_name)

if __name__ == "__main__":
    main()
