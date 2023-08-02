#!/usr/bin/python
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
The module file for sonic_vlans
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
module: sonic_vlans
version_added: 1.0.0
notes:
- Tested against Enterprise SONiC Distribution by Dell Technologies.
- Supports C(check_mode).
author: Mohamed Javeed (@javeedf)
short_description: Manage VLAN and its parameters
description:
  - This module provides configuration management of VLANs parameters
    on devices running Enterprise SONiC Distribution by Dell Technologies.
options:
  config:
    description: A dictionary of VLAN options.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
        - ID of the VLAN
        - Range is 1 to 4094
        type: int
        required: true
      description:
        description:
        - Description about the VLAN.
        type: str
  state:
    description:
    - The state that the configuration should be left in.
    type: str
    choices:
    - merged
    - deleted
    default: merged
"""
EXAMPLES = """
# Using merged

# Before state:
# -------------
#
#sonic# show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#30         Inactive
#
#sonic#
#


- name: Merges given VLAN attributes with the device configuration
  dellemc.enterprise_sonic.sonic_vlans:
    config:
      - vlan_id: 10
        description: "Internal"
    state: merged

# After state:
# ------------
#
#sonic# show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#30         Inactive
#
#sonic#
#
#sonic# show interface Vlan 10
#Description: Internal
#Vlan10 is up
#Mode of IPV4 address assignment: not-set
#Mode of IPV6 address assignment: not-set
#IP MTU 6000 bytes
#sonic#
#


# Using deleted

# Before state:
# -------------
#
#sonic# show interface Vlan 70
#Description: Internal
#Vlan70 is up
#Mode of IPV4 address assignment: not-set
#Mode of IPV6 address assignment: not-set
#IP MTU 6000 bytes

- name: Deletes attributes of the given VLANs
  dellemc.enterprise_sonic.sonic_vlans:
    config:
      - vlan_id: 70
        description: "Internal"
    state: deleted

# After state:
# ------------
#
#sonic# show interface Vlan 70
#Vlan70 is up
#Mode of IPV4 address assignment: not-set
#Mode of IPV6 address assignment: not-set
#IP MTU 6000 bytes

# Before state:
# -------------
#
#sonic# show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#20         Inactive
#
#sonic#

- name: Deletes attributes of the given VLANs
  dellemc.enterprise_sonic.sonic_vlans:
    config:
      - vlan_id: 20
    state: deleted

# After state:
# ------------
#
#sonic# show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#
#sonic#


# Using deleted

# Before state:
# -------------
#
#sonic# show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#20         Inactive
#30         Inactive
#
#sonic#

- name: Deletes all the VLANs on the switch
  dellemc.enterprise_sonic.sonic_vlans:
    config:
    state: deleted

# After state:
# ------------
#
#sonic# show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#
#sonic#


"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration that is returned is always in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned is always in the same format
    of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['command 1', 'command 2', 'command 3']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.argspec.vlans.vlans import VlansArgs
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.config.vlans.vlans import Vlans


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=VlansArgs.argument_spec,
                           supports_check_mode=True)

    result = Vlans(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
