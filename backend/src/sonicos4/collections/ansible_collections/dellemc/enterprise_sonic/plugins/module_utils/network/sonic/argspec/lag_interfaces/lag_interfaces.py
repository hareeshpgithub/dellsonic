#
# -*- coding: utf-8 -*-
# Copyright 2020 Dell Inc. or its subsidiaries. All Rights Reserved
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
The arg spec for the sonic_lag_interfaces module
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class Lag_interfacesArgs(object):  # pylint: disable=R0903

    """The arg spec for the sonic_lag_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "members": {
                    "options": {
                        "interfaces": {
                            "elements": "dict",
                            "options": {
                                "member": {"type": "str"}
                            },
                            "type": "list"
                        }
                    },
                    "type": "dict"
                },
                "name": {"required": True, "type": "str"},
                "mode": {"type": "str", "choices": ["static", "lacp"]}
            },
            "type": "list"
        },
        "state": {
            "choices": ["merged", "deleted"],
            "default": "merged",
            "type": "str"
        }
    }  # pylint: disable=C0301
