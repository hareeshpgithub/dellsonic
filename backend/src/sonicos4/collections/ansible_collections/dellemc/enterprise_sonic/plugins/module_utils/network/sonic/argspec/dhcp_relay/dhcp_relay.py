#
# -*- coding: utf-8 -*-
# Copyright 2022 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The arg spec for the sonic_dhcp_relay module
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class Dhcp_relayArgs(object):  # pylint: disable=R0903
    """The arg spec for the sonic_dhcp_relay module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        'config': {
            'elements': 'dict',
            'options': {
                'ipv4': {
                    'options': {
                        'circuit_id': {
                            'choices': ['%h:%p', '%i', '%p'],
                            'type': 'str'
                        },
                        'link_select': {'type': 'bool'},
                        'max_hop_count': {'type': 'int'},
                        'policy_action': {
                            'choices': ['append', 'discard', 'replace'],
                            'type': 'str'
                        },
                        'server_addresses': {
                            'elements': 'dict',
                            'options': {
                                'address': {'type': 'str'}
                            },
                            'type': 'list'
                        },
                        'source_interface': {'type': 'str'},
                        'vrf_name': {'type': 'str'},
                        'vrf_select': {'type': 'bool'}
                    },
                    'type': 'dict'
                },
                'ipv6': {
                    'options': {
                        'max_hop_count': {'type': 'int'},
                        'server_addresses': {
                            'elements': 'dict',
                            'options': {
                                'address': {'type': 'str'}
                            },
                            'type': 'list'
                        },
                        'source_interface': {'type': 'str'},
                        'vrf_name': {'type': 'str'},
                        'vrf_select': {'type': 'bool'}
                    },
                    'type': 'dict'
                },
                'name': {'required': True, 'type': 'str'}
            },
            'type': 'list'
        },
        'state': {
            'choices': ['merged', 'deleted', 'replaced', 'overridden'],
            'default': 'merged',
            'type': 'str'
        }
    }  # pylint: disable=C0301