#!/usr/bin/python
# -*- coding: utf-8 -*-
# © Copyright 2020 Dell Inc. or its subsidiaries. All Rights Reserved
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
The module file for sonic_interfaces
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
module: sonic_interfaces
version_added: 1.0.0
notes:
- Tested against Enterprise SONiC Distribution by Dell Technologies.
- Supports C(check_mode).
short_description: Configure Interface attributes on interfaces such as, Eth, LAG, VLAN, and loopback.
                   (create a loopback interface if it does not exist.)
description: Configure Interface attributes such as, MTU, admin statu, and so on, on interfaces
             such as, Eth, LAG, VLAN, and loopback. (create a loopback interface if it does not exist.)
author: Niraimadaiselvam M(@niraimadaiselvamm)
options:
  config:
    description: A list of interface configurations.
    type: list
    elements: dict
    suboptions:
      name:
        type: str
        description: The name of the interface, for example, 'Eth1/15'.
        required: true
      description:
        type: str
        description:
        - Description about the interface.
      enabled:
        description:
        - Administrative state of the interface.
        type: bool
      mtu:
        description:
        - MTU of the interface.
        type: int
      speed:
        description:
        - Interface speed.
        - Supported speeds are dependent on the type of switch.
        type: str
        choices:
        - SPEED_10MB
        - SPEED_100MB
        - SPEED_1GB
        - SPEED_2500MB
        - SPEED_5GB
        - SPEED_10GB
        - SPEED_20GB
        - SPEED_25GB
        - SPEED_40GB
        - SPEED_50GB
        - SPEED_100GB
        - SPEED_400GB
      auto_negotiate:
        description:
        - auto-negotiate transmission parameters with peer interface.
        type: bool
      advertised_speed:
        description:
        - Advertised speeds of the interface.
        - Supported speeds are dependent on the type of switch.
        - Speeds may be 10, 100, 1000, 2500, 5000, 10000, 20000, 25000, 40000, 50000, 100000 or 400000.
        type: list
        elements: str
      fec:
        description:
        - Interface FEC (Forward Error Correction).
        type: str
        choices:
        - FEC_RS
        - FEC_FC
        - FEC_DISABLED
        - FEC_DEFAULT
        - FEC_AUTO
  state:
    description:
    - The state the configuration should be left in.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    default: merged
"""
EXAMPLES = """
# Using deleted
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           Ethernet-8          down                            100000       9100
#Ethernet12          Ethernet-12         down                on          -            5000
#Ethernet16          -                   down                            40000        9100
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# fec AUTO
# shutdown
#
- name: Configure interfaces
  sonic_interfaces:
    config:
      - name: Ethernet8
      - name: Ethernet12
      - name: Ethernet16
    state: deleted
#
# After state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   up                              100000       9100
#Ethernet12          -                   up                              100000       9100
#Ethernet16          -                   up                              100000       9100
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# shutdown
#
# Using deleted
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   down                            100000       9100
#Ethernet12          -                   down                            1000         9100
#Ethernet16          -                   down                            100000       9100
#
- name: Configure interfaces
  sonic_interfaces:
    config:

    state: deleted
#
# After state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   up                              100000       9100
#Ethernet12          -                   up                              100000       9100
#Ethernet16          -                   up                              100000       9100
#
#
#
# Using merged
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   down                            100000       9100
#Ethernet12          -                   down                            100000       9100
#Ethernet16          -                   down                            100000       9100
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# shutdown
#
- name: Configure interfaces
  sonic_interfaces:
    config:
      - name: Ethernet8
        fec: FEC_AUTO
      - name: Ethernet12
        description: 'Ethernet Twelve'
        auto_negotiate: True
      - name: Ethernet16
        description: 'Ethernet Sixteen'
        enabled: True
        mtu: 3500
        speed: SPEED_40GB
    state: merged
#
# After state:
# ------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   down                            100000       9100
#Ethernet12          Ethernet Twelve     down                on          100000       9100
#Ethernet16          Ethernet Sixteen    up                              40000        3500
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# fec AUTO
# shutdown
#
# Using overridden
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           E0                  up                              100000       9100
#Ethernet4           E4                  up                              100000       9100
#Ethernet8           E8                  down                            100000       9100
#Ethernet12          -                   down                            1000         9100
#Ethernet16          -                   down                            100000       9100
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# shutdown
#
- name: Configure interfaces
  sonic_interfaces:
    config:
      - name: Ethernet8
        fec: FEC_AUTO
      - name: Ethernet12
        description: 'Ethernet Twelve'
        mtu: 3500
        enable: True
        auto_negotiate: True
      - name: Ethernet16
        description: 'Ethernet Sixteen'
        mtu: 3000
        enable: False
        speed: SPEED_40GB
    state: overridden
#
# After state:
# ------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   up                              100000       9100
#Ethernet12          Ethernet Twelve     up                  on          100000       3500
#Ethernet16          Ethernet Sixteen    down                            40000        3000
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# fec AUTO
# no shutdown
#
# Using replaced
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   down                            100000       9100
#Ethernet12          -                   down                            1000         9100
#Ethernet16          -                   down                            100000       9100
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# shutdown
#
- name: Configure interfaces
  sonic_interfaces:
    config:
      - name: Ethernet8
        fec: FEC_AUTO
      - name: Ethernet12
        description: 'Ethernet Twelve'
        mtu: 3500
        enable: True
        auto_negotiate: True
      - name: Ethernet16
        description: 'Ethernet Sixteen'
        mtu: 3000
        enable: False
        speed: SPEED_40GB
    state: replaced
#
# After state:
# ------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin     Oper      AutoNeg     Speed        MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                              100000       9100
#Ethernet4           -                   up                              100000       9100
#Ethernet8           -                   up                              100000       9100
#Ethernet12          Ethernet Twelve     up                  on          100000       3500
#Ethernet16          Ethernet Sixteen    down                            40000        3000
#
# show running-configuration interface Ethernet 8
#!
#interface Ethernet8
# mtu 9100
# speed 100000
# fec AUTO
# no shutdown
#
"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration returned is always in the same format
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
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.argspec.interfaces.interfaces import InterfacesArgs
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.config.interfaces.interfaces import Interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=InterfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()