import re
import yaml
import sys

import datetime

newline = "\n"
config_const = "    configs:\n"
no_shutdown_const = "no shutdown"
bgp_asn_const = "  - bgp_as: '{{ bgp_asn }}'\n"
ipv4_const = "    ipv4:\n"
ip_address_const = "ip address"
router_bgp_const = "router bgp"
interface_vlan_const = "interface Vlan"


def all_parser(input_file, output_file):
    # region Management Ip
    management_ip_start = False
    yaml_output_management_ip = "# Management IP\n"
    yaml_output_management_ip += "management_ip: "

    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("interface Management 0"):
                management_ip_start = True
            if management_ip_start == True:
                if line.strip().startswith("ip address"):
                    yaml_output_management_ip += line.strip().split()[2].split("/")[0]
                if line.startswith("!"):
                    break
    with open(output_file, "w") as f:
        f.write(yaml_output_management_ip)
        f.write(newline)
        f.write(newline)
    print("Created Management IP")
    # endregion

    # region Host Name
    data = {"host_name": input_file.rsplit("/", 1)[-1].split(".")[0]}
    with open(output_file, "a") as f:
        f.write("# Host Name\n")
        yaml.dump(data, f)
        f.write(newline)
    print("Created Hostname")
    # endregion

    # region Any Cast Mac Address
    anycast_mac_address = None
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("ip anycast-mac-address"):
                anycast_mac_address = line.strip().split()[-1]
                break

    if anycast_mac_address is not None:
        data = {"anycast_mac_address": anycast_mac_address}

        with open(output_file, "a") as f:
            f.write("# Any Cast Mac Address\n")
            yaml.dump(data, f)
            f.write(newline)
        print("Created Anycast MAC address")
    # endregion

    # region Loopback
    with open(input_file, "r") as f:
        block_started = False
        config_started = False
        yaml_output_info = ""
        loopback_lb_id = ""
        yaml_output_sonic_loopback_interface_ids = "sonic_loopback_interface_ids:\n"
        yaml_output_sonic_loopback_interfaces = "sonic_loopback_interfaces:\n"
        yaml_output_sonic_l3_loopback_interfaces = "sonic_l3_loopback_interfaces:\n"
        for line in f:
            if line.startswith("interface Loopback"):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False

            if block_started:
                if line.startswith("interface Loopback"):
                    loopback_lb_id = line.strip().split()[-1]
                    yaml_output_info += (
                        f"loopback_inf{loopback_lb_id}: Loopback{loopback_lb_id}\n"
                    )
                    yaml_output_sonic_loopback_interfaces += (
                        f"  - name: '{{{{ loopback_inf{loopback_lb_id} }}}}'\n"
                    )
                    config_started = False
                elif line.strip().startswith(ip_address_const):
                    yaml_output_info += (
                        f"loopback{loopback_lb_id}_ip: {line.strip().split()[-1]}\n"
                    )

                    yaml_output_sonic_l3_loopback_interfaces += (
                        f"  - name: '{{{{ loopback_inf{loopback_lb_id} }}}}'\n"
                    )
                    yaml_output_sonic_l3_loopback_interfaces += ipv4_const
                    yaml_output_sonic_l3_loopback_interfaces += f"      addresses:\n        - address: '{{{{ loopback{loopback_lb_id}_ip }}}}'\n"

                    yaml_output_sonic_loopback_interface_ids += (
                        f"  - lb_id: {loopback_lb_id}\n"
                    )
                    yaml_output_sonic_loopback_interface_ids += (
                        f"    ipv4_address: '{{{{ loopback{loopback_lb_id}_ip }}}}'\n"
                    )
                elif line.strip().startswith("ip ospf"):
                    if config_started == False:
                        config_started = True
                        yaml_output_sonic_loopback_interface_ids += config_const

                    yaml_output_sonic_loopback_interface_ids += (
                        f"      - {line.strip()}\n"
                    )

        with open(output_file, "a") as f:
            f.write("# Loopback\n")
            f.write(yaml_output_info)
            f.write(yaml_output_sonic_l3_loopback_interfaces)
            f.write(yaml_output_sonic_loopback_interface_ids)
            f.write(yaml_output_sonic_loopback_interfaces)

            f.write(newline)
        print("Created Loopback")
    # endregion

    # region vrf management
    ip_vrf_mgmt = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("ip vrf mgmt"):
                ip_vrf_mgmt = True
                break

    if ip_vrf_mgmt:
        with open(output_file, "a") as f:
            f.write("# VRF Management\n")
            f.write("sonic_vrf_name: mgmt\n")
            f.write(newline)
        print("Created VRF Management")
    # endregion

    # region Vlan
    with open(input_file, "r") as f:
        block_started = False
        vlan_id_full = None
        vlan_id = None
        vlan_desc = None

        yaml_output_sonic_vlans = "sonic_vlans:\n"
        yaml_output_sonic_vlan_ids = "sonic_vlan_ids:\n"
        yaml_output_sonic_vlan_ids_config_start = False
        yaml_output_sonic_l3_vlan = "sonic_l3_vlan:\n"
        yaml_output_interface_vlan_started = False
        ip4_address_start = False
        for line in f:
            if line.startswith(interface_vlan_const):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False
                vlan_id_full = None
                vlan_id = None
                vlan_desc = None

            if block_started:
                if line.startswith(interface_vlan_const):
                    yaml_output_interface_vlan_started = True
                    vlan_id_full = line.split()[-1]
                    vlan_id = line.split()[-1].replace("Vlan", "")
                    yaml_output_sonic_vlans += f"  - vlan_id: {vlan_id}\n"
                    ip4_address_start = False
                    yaml_output_sonic_vlan_ids_config_start = False
                elif line.strip().startswith("description"):
                    vlan_desc = line.split()[-1]
                    yaml_output_sonic_vlans += f"    description: {vlan_desc}\n"
                elif line.strip().startswith("neigh-suppress"):
                    yaml_output_sonic_vlan_ids += f"  - name: {vlan_id_full}\n"
                    if yaml_output_sonic_vlan_ids_config_start == False:
                        yaml_output_sonic_vlan_ids_config_start = True
                        yaml_output_sonic_vlan_ids += config_const
                    yaml_output_sonic_vlan_ids += "      - neigh-suppress\n"
                elif line.strip().startswith("mtu"):
                    yaml_output_sonic_vlan_ids += f"  - name: {vlan_id_full}\n"
                    if yaml_output_sonic_vlan_ids_config_start == False:
                        yaml_output_sonic_vlan_ids_config_start = True
                        yaml_output_sonic_vlan_ids += config_const
                    yaml_output_sonic_vlan_ids += f"      - {line.strip()}\n"

                elif line.strip().startswith("ip anycast-address"):
                    ipv4_address = line.split()[-1]
                    yaml_output_sonic_l3_vlan += f"  - name: {vlan_id_full}\n"
                    yaml_output_sonic_l3_vlan += ipv4_const
                    yaml_output_sonic_l3_vlan += "      anycast_addresses:\n"
                    yaml_output_sonic_l3_vlan += f"        - {ipv4_address}\n"
                elif line.strip().startswith(ip_address_const):
                    ipv4_address = line.split()[+2]
                    if ip4_address_start == False:
                        ip4_address_start = True

                        yaml_output_sonic_l3_vlan += f"  - name: {vlan_id_full}\n"
                        yaml_output_sonic_l3_vlan += ipv4_const
                        yaml_output_sonic_l3_vlan += "      addresses:\n"

                    yaml_output_sonic_l3_vlan += f"        - address: {ipv4_address}\n"

                    if "secondary" in line:
                        yaml_output_sonic_l3_vlan += "          secondary: True"
        if yaml_output_interface_vlan_started == True:
            with open(output_file, "a") as f:
                f.write("# Vlan\n")
                f.write(yaml_output_sonic_vlans)
                f.write(yaml_output_sonic_vlan_ids)
                f.write(yaml_output_sonic_l3_vlan)
                f.write(newline)
            print("Created Vlan")
    # For Super Spine
    with open(input_file, "r") as f:
        block_started = False
        config_started = False
        yaml_output_sonic_vlan_ids_mclag = "sonic_vlan_ids_mclag:\n"
        yaml_output_sonic_vlan_ids_mclag_found = False
        for line in f:
            if line.startswith(interface_vlan_const):
                block_started = True

            if block_started == True and line.startswith("!"):
                break

            if block_started:
                if line.startswith(interface_vlan_const):
                    yaml_output_sonic_vlan_ids_mclag_found = True
                    vlan_id_full = line.split()[-1]
                    yaml_output_sonic_vlan_ids_mclag += f"  - name: {vlan_id_full}\n"
                if line.strip().startswith(
                    "mclag-separate-ip"
                ) or line.strip().startswith("ip"):
                    if config_started == False:
                        yaml_output_sonic_vlan_ids_mclag += "    configs:\n"
                        config_started = True
                    yaml_output_sonic_vlan_ids_mclag += f"      - {line.strip()}\n"
        if yaml_output_sonic_vlan_ids_mclag_found == True:
            with open(output_file, "a") as f:
                f.write(yaml_output_sonic_vlan_ids_mclag)
                f.write(newline)
            print("Created Vlan")
    # endregion

    # region Vxlan
    with open(input_file, "r") as f:
        block_started = False
        vtep = None
        yaml_output_sonic_vxlans = "sonic_vxlans:\n"
        yaml_output_vxlan_map = "vxlan_map:\n"

        yaml_output_sonic_vxlans_started = False
        for line in f:
            if line.startswith("interface vxlan"):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False
                break

            if block_started:
                if line.startswith("interface vxlan"):
                    yaml_output_sonic_vxlans_started = True
                    vtep = line.split()[-1]
                elif line.strip().startswith("source-ip"):
                    source_ip = line.split()[-1]
                    yaml_output_sonic_vxlans += f"  - name: {vtep}\n"
                    yaml_output_sonic_vxlans += f"    source_ip: {source_ip}\n"
                    yaml_output_sonic_vxlans += "    evpn_nvo: nvo1\n"
                    yaml_output_sonic_vxlans += "    vlan_map: '{{ vxlan_map }}'\n"
                elif line.strip().startswith("map vni"):
                    vlan_id = line.split()[-1]
                    vlan_vxlan_id = line.split()[-3]
                    yaml_output_vxlan_map += f"  - vlan: {vlan_id}\n"
                    yaml_output_vxlan_map += f"    vni: {vlan_vxlan_id}\n"
        if yaml_output_sonic_vxlans_started == True:
            with open(output_file, "a") as f:
                f.write("# Vxlan\n")
                f.write(yaml_output_sonic_vxlans)
                f.write(yaml_output_vxlan_map)
                f.write(newline)
            print("Created Vxlan")
    # endregion

    # region Portchannel
    with open(input_file, "r") as f:
        block_started = False
        vtep = None
        port_channel_id = None
        yaml_output_sonic_portchannels = "sonic_portchannels:\n"
        yaml_output_sonic_portchannels_allowed_vlans = (
            "sonic_portchannels_allowed_vlans:\n"
        )
        interface_portchannel = "interface PortChannel"
        interface_portchannel_started = False
        portchannels_allowed_vlans_stated = False
        for line in f:
            if line.startswith(interface_portchannel):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False
                port_channel_id = None

            if block_started:
                if line.startswith(interface_portchannel):
                    interface_portchannel_started = True
                    port_channel_id = line.split()[+2]
                    yaml_output_sonic_portchannels += (
                        f"  - name: PortChannel{port_channel_id}\n"
                    )
                    yaml_output_sonic_portchannels += "    mode: lacp\n"
                    portchannels_allowed_vlans_stated = False

                if line.strip().startswith("switchport access Vlan"):
                    vlan_id = line.split()[-1]
                    if portchannels_allowed_vlans_stated == False:
                        yaml_output_sonic_portchannels_allowed_vlans += (
                            f"  - name: PortChannel{port_channel_id}\n"
                        )
                        portchannels_allowed_vlans_stated = True
                    yaml_output_sonic_portchannels_allowed_vlans += "    access:\n"
                    yaml_output_sonic_portchannels_allowed_vlans += (
                        f"      vlan: {vlan_id}\n"
                    )
                if line.strip().startswith("switchport trunk allowed Vlan"):
                    if portchannels_allowed_vlans_stated == False:
                        yaml_output_sonic_portchannels_allowed_vlans += (
                            f"  - name: PortChannel{port_channel_id}\n"
                        )
                        portchannels_allowed_vlans_stated = True
                    yaml_output_sonic_portchannels_allowed_vlans += "    trunk:\n"
                    yaml_output_sonic_portchannels_allowed_vlans += (
                        "      allowed_vlans:\n"
                    )
                    vlan_id = line.split()[-1]

                    if "-" in vlan_id:
                        # multiple ranges
                        for vlan_range in vlan_id.split(","):
                            if "-" in vlan_range:
                                start_vlan, end_vlan = map(int, vlan_range.split("-"))
                                for vlan_id in range(start_vlan, end_vlan + 1):
                                    yaml_output_sonic_portchannels_allowed_vlans += (
                                        f"        - vlan: {vlan_id}\n"
                                    )
                            else:
                                yaml_output_sonic_portchannels_allowed_vlans += (
                                    f"        - vlan: {vlan_range}\n"
                                )
                    else:
                        for vlan_range in vlan_id.split(","):
                            yaml_output_sonic_portchannels_allowed_vlans += (
                                f"        - vlan: {vlan_range}\n"
                            )
        if interface_portchannel_started == True:
            with open(output_file, "a") as f:
                f.write("# Portchannel\n")
                f.write(yaml_output_sonic_portchannels)
                f.write(yaml_output_sonic_portchannels_allowed_vlans)
            print("Created Portchannels 1/2")
    with open(input_file, "r") as f:
        block_started = False
        port_channel_id = None
        mode = False
        mclag = False
        description = None
        shutdown = "shutdown"
        switch_port_access = None
        switch_port_trunk = None
        yaml_output_sonic_portchannels_ids = "sonic_portchannels_ids:\n"
        yaml_output_sonic_portchannels_ids_started = False
        for line in f:
            if line.startswith(interface_portchannel):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False
                if port_channel_id != None:
                    yaml_output_sonic_portchannels_ids += (
                        f"  - po_id: {port_channel_id}\n"
                    )
                    yaml_output_sonic_portchannels_ids += f"    mode_active: {mode}\n"
                    yaml_output_sonic_portchannels_ids += f"    mclag: {mclag}\n"
                    yaml_output_sonic_portchannels_ids += config_const
                    if description == None:
                        yaml_output_sonic_portchannels_ids += "      - no description\n"
                    else:
                        yaml_output_sonic_portchannels_ids += (
                            f"      - description {description}\n"
                        )
                    if switch_port_access != None:
                        yaml_output_sonic_portchannels_ids += (
                            f"      - {switch_port_access}\n"
                        )

                    if switch_port_trunk != None:
                        yaml_output_sonic_portchannels_ids += (
                            f"      - {switch_port_trunk}\n"
                        )

                    yaml_output_sonic_portchannels_ids += f"      - {shutdown}\n"

                    port_channel_id = None
                    mode = False
                    mclag = False
                    description = None
                    shutdown = "shutdown"
                    switch_port_access = None
                    switch_port_trunk = None

            if block_started:
                if line.startswith(interface_portchannel):
                    yaml_output_sonic_portchannels_ids_started = True
                    port_channel_id = line.split()[+2]

                if "mode active" in line:
                    mode = True

                if "mclag" in line:
                    mclag = True

                if no_shutdown_const in line:
                    shutdown = no_shutdown_const

                if "switchport access" in line:
                    switch_port_access = line.strip()

                if "switchport trunk" in line:
                    switch_port_trunk = line.strip()

                if "description" in line:
                    description = line.split()[-1]
        if yaml_output_sonic_portchannels_ids_started == True:
            with open(output_file, "a") as f:
                f.write(yaml_output_sonic_portchannels_ids)
                f.write(newline)
            print("Created Portchannels 2/2")
    # endregion

    # region mclag
    with open(input_file, "r") as f:
        block_started = False
        yaml_output_sonic_mclag = "sonic_mclag:\n"
        yaml_output_sonic_mclag_ids = "sonic_mclag_ids:\n"
        yaml_output_sonic_mclag_found = False
        domain_id = None
        for line in f:
            if line.startswith("mclag"):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False
                break

            if block_started:
                if line.startswith("mclag"):
                    yaml_output_sonic_mclag_found = True
                    domain_id = line.split()[-1]
                    yaml_output_sonic_mclag += f"  domain_id: {domain_id}\n"
                    yaml_output_sonic_mclag_ids += f"  - domain_id: {domain_id}\n"
                if line.strip().startswith("source-ip"):
                    source_ip = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag += f"  source_address: {source_ip}\n"
                if line.strip().startswith("peer-ip"):
                    peer_address = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag += f"  peer_address: {peer_address}\n"
                if line.strip().startswith("peer-link"):
                    peer_link = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag += f"  peer_link: {peer_link}\n"
                if line.strip().startswith("mclag-system-mac"):
                    system_mac = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag += f"  system_mac: {system_mac}\n"
                if line.strip().startswith("keepalive-interval"):
                    keepalive = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag += f"  keepalive: {keepalive}\n"
                if line.strip().startswith("session-timeout"):
                    session_timeout = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag += f"  session_timeout: {session_timeout}\n"
                if line.strip().startswith("delay-restore"):
                    session_timeout = line.strip().split(" ")[1]
                    yaml_output_sonic_mclag_ids += (
                        f"    delay_restore: {session_timeout}\n"
                    )
    if yaml_output_sonic_mclag_found == True:
        with open(output_file, "a") as f:
            f.write("# Mclag\n")
            f.write(yaml_output_sonic_mclag)
            f.write(yaml_output_sonic_mclag_ids)
            f.write(newline)
        print("Created Mclag")
    # endregion

    # region Ethernet
    with open(input_file, "r") as f:
        block_started = False
        yaml_output_sonic_interfaces_eth = "sonic_interfaces_eth:\n"
        yaml_output_sonic_l3_ethernet_interfaces = "sonic_l3_ethernet_interfaces:\n"
        yaml_output_sonic_interfaces_eth_ids = "sonic_interfaces_eth_ids:\n"
        interface = None
        description = None
        mtu = 9100
        speed = None
        channel_group = None
        shutdown = None
        no_shutdown = None
        ipv6_enable = False
        switch_port = None
        ipv4_address = None
        fec_rs = None
        ip_ospf_area = None
        ip_ospf_network = None
        prefixes = [
            "description",
            "mtu",
            "speed",
            no_shutdown_const,
            "shutdown",
            "ipv6 enable",
            "switchport",
            "channel-group",
            ip_address_const,
            "fec RS",
            "ip ospf area",
            "ip ospf network",
        ]
        for line in f:
            if line.startswith("interface Eth"):
                block_started = True

            if block_started == True and line.startswith("!"):
                block_started = False
                if interface != None:
                    yaml_output_sonic_interfaces_eth += f"  - name: {interface}\n"
                    if description != None:
                        yaml_output_sonic_interfaces_eth += (
                            f"    description: {description}\n"
                        )
                    # else:
                    #     yaml_output_sonic_interfaces_eth += "    no description\n"

                    yaml_output_sonic_interfaces_eth += f"    mtu: {mtu}\n"

                    if ipv6_enable == True:
                        yaml_output_sonic_l3_ethernet_interfaces += (
                            f"  - name: {interface}\n"
                        )
                        yaml_output_sonic_l3_ethernet_interfaces += "    ipv6:\n"
                        yaml_output_sonic_l3_ethernet_interfaces += (
                            "      enabled: true\n"
                        )
                    if ipv4_address != None:
                        yaml_output_sonic_l3_ethernet_interfaces += (
                            f"  - name: {interface}\n"
                        )
                        yaml_output_sonic_l3_ethernet_interfaces += ipv4_const
                        yaml_output_sonic_l3_ethernet_interfaces += "      addresses:\n"
                        yaml_output_sonic_l3_ethernet_interfaces += (
                            f"        - address: {ipv4_address}\n"
                        )
                # Separately Written sonic_interfaces_eth_ids to avoid confusion
                if interface != None:
                    yaml_output_sonic_interfaces_eth_ids += f"  - name: {interface}\n"
                    yaml_output_sonic_interfaces_eth_ids += config_const
                    if speed != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - speed {speed}\n"
                        )
                    if channel_group != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - channel-group {channel_group}\n"
                        )
                    if shutdown != None:
                        yaml_output_sonic_interfaces_eth_ids += f"      - {shutdown}\n"

                    if no_shutdown != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - {no_shutdown}\n"
                        )
                    if ipv4_address != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - ip address {ipv4_address}\n"
                        )

                    if switch_port != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - {switch_port}\n"
                        )

                    if fec_rs != None:
                        yaml_output_sonic_interfaces_eth_ids += f"      - {fec_rs}\n"

                    if ip_ospf_area != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - {ip_ospf_area}\n"
                        )

                    if ip_ospf_network != None:
                        yaml_output_sonic_interfaces_eth_ids += (
                            f"      - {ip_ospf_network}\n"
                        )
                interface = None
                description = None
                mtu = 9100
                speed = None
                channel_group = None
                shutdown = None
                no_shutdown = None
                ipv6_enable = False
                switch_port = None
                ipv4_address = None
                fec_rs = None
                ip_ospf_area = None
                ip_ospf_network = None

            if block_started:
                if line.startswith("interface Eth"):
                    interface = line.split()[1]

                if any(line.strip().startswith(x) for x in prefixes):
                    if line.strip().split()[0] == "description":
                        description = line.replace("description", "").strip()
                    if line.strip().split()[0] == "mtu":
                        mtu = line.replace("mtu", "").strip()
                    if line.strip().split()[0] == "speed":
                        speed = line.replace("speed", "").strip()
                    if line.strip() == "shutdown":
                        shutdown = line.strip()
                    if line.strip() == no_shutdown_const:
                        no_shutdown = line.strip()
                    if line.strip().split()[0] == "switchport":
                        switch_port = line.strip()
                    if line.strip().split()[0] == "channel-group":
                        channel_group = line.replace("channel-group", "").strip()
                    if line.strip() == "ipv6 enable":
                        ipv6_enable = True
                    if line.strip().startswith(ip_address_const):
                        ipv4_address = line.strip().split()[-1]
                    if line.strip().startswith("fec RS"):
                        fec_rs = line.strip()
                    if line.strip().startswith("ip ospf area"):
                        ip_ospf_area = line.strip()
                    if line.strip().startswith("ip ospf network"):
                        ip_ospf_network = line.strip()
        with open(output_file, "a") as f:
            f.write("# Interface Ethernet\n")
            f.write(yaml_output_sonic_interfaces_eth)
            f.write(yaml_output_sonic_l3_ethernet_interfaces)
            f.write(yaml_output_sonic_interfaces_eth_ids)
            f.write(newline)
        print("Created Interface Ethernet")
    # endregion

    # region port Break
    yaml_output_sonic_port_breakout = "sonic_port_breakout:\n"
    yaml_output_sonic_port_breakout_found = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("interface breakout"):
                yaml_output_sonic_port_breakout_found = True
                yaml_output_sonic_port_breakout += (
                    f"  - name: {line.strip().split()[+3]}\n"
                )
                yaml_output_sonic_port_breakout += (
                    f"    mode: {line.strip().split()[+5]}\n"
                )
    if yaml_output_sonic_port_breakout_found == True:
        with open(output_file, "a") as f:
            f.write("# Port Break\n")
            f.write(yaml_output_sonic_port_breakout)
            f.write(newline)
        print("Created Port Brake")
    # endregion

    # region ip prefix-list
    yaml_output_sonic_prefix_list_cli = "sonic_prefix_list_cli:\n"
    yaml_output_sonic_prefix_list_cli_found = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("ip prefix-list"):
                yaml_output_sonic_prefix_list_cli_found = True
                yaml_output_sonic_prefix_list_cli += (
                    f"  - name: {line.strip().split()[+2]}\n"
                )

                if "permit" in line:
                    yaml_output_sonic_prefix_list_cli += "    permit: true\n"
                    if "seq" in line:
                        yaml_output_sonic_prefix_list_cli += "    entries:\n"
                        yaml_output_sonic_prefix_list_cli += (
                            f"      - ip: {line.strip().split()[+6]}\n"
                        )
                        yaml_output_sonic_prefix_list_cli += (
                            f"        seq: {line.strip().split()[+4]}\n"
                        )
    if yaml_output_sonic_prefix_list_cli_found == True:
        with open(output_file, "a") as f:
            f.write("# IP prefix-list\n")
            f.write(yaml_output_sonic_prefix_list_cli)
            f.write(newline)
        print("Created ip prefix-list")
    # endregion

    # region route_maps_cli
    yaml_output_sonic_route_maps_cli = "sonic_route_maps_cli:\n"
    yaml_output_sonic_route_maps_cli_found = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("route-map"):
                yaml_output_sonic_route_maps_cli_found = True
                yaml_output_sonic_route_maps_cli += (
                    f"  - name: {line.strip().split()[+1]}\n"
                )

                if "permit" in line:
                    yaml_output_sonic_route_maps_cli += "    permit: true\n"
                    yaml_output_sonic_route_maps_cli += (
                        f"    seq: {line.strip().split()[+3]}\n"
                    )
            if line.strip().startswith("set ip"):
                yaml_output_sonic_route_maps_cli += (
                    f"    match_ip_prefix_list: {line.strip().split()[-1]}\n"
                )

            # if yaml_output_sonic_route_maps_cli_found == True and line.startswith("!"):
            #     break
    if yaml_output_sonic_route_maps_cli_found == True:
        with open(output_file, "a") as f:
            f.write("# Route Maps\n")
            f.write(yaml_output_sonic_route_maps_cli)
            f.write(newline)
        print("Created Route Maps")
    # endregion

    # region BGP Stage 1
    yaml_output_bgp_asn = "bgp_asn: "
    yaml_output_bgp_router_id = "bgp_router_id: "
    yaml_output_sonic_bgp = "sonic_bgp:\n"
    yaml_output_sonic_bgp += bgp_asn_const
    yaml_output_sonic_bgp += "    router_id: '{{ bgp_router_id }}'\n"
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith(router_bgp_const):
                yaml_output_bgp_asn += (
                    line.replace(router_bgp_const, "").strip() + newline
                )
            if line.strip().startswith("router-id"):
                yaml_output_bgp_router_id += (
                    line.replace("router-id", "").strip() + newline
                )
            if line.strip().startswith("bestpath as-path"):
                yaml_output_sonic_bgp += "    bestpath:\n"
                yaml_output_sonic_bgp += "      as_path:\n"
                if "multipath-relax" in line:
                    yaml_output_sonic_bgp += "        multipath_relax: True\n"
                if "as-set" in line:
                    yaml_output_sonic_bgp += "        multipath_relax_as_set: True\n"

    with open(output_file, "a") as f:
        f.write("# BGP Server\n")
        f.write(yaml_output_bgp_asn)
        f.write(yaml_output_bgp_router_id)
        f.write(yaml_output_sonic_bgp)
    print("Created BGP Server 1/2")
    # Stage 2
    # endregion

    # region BGP Stage 2
    yaml_output_sonic_bgp_af = "sonic_bgp_af:\n"
    yaml_output_sonic_bgp_af += bgp_asn_const
    yaml_output_sonic_bgp_af += "    address_family:\n"
    yaml_output_sonic_bgp_af += "      afis:\n"
    yaml_output_sonic_bgp_neighbors = "sonic_bgp_neighbors:\n"
    yaml_output_sonic_bgp_neighbors += bgp_asn_const

    yaml_output_sonic_bgp_af_extra = "sonic_bgp_af_extra:\n"
    yaml_output_sonic_bgp_neighbors_af_extra = "sonic_bgp_neighbors_af_extra:\n"
    yaml_output_sonic_bgp_neighbors_af_extra_header = ""
    yaml_output_sonic_bgp_neighbors_af_extra_configs = False
    yaml_output_sonic_bgp_af_extra_temp = ""
    yaml_output_sonic_bgp_af_extra_started = False

    yaml_output_sonic_bgp_neighbors_af = "sonic_bgp_neighbors_af:\n"
    yaml_output_sonic_bgp_neighbors_af_address_family_started = False
    yaml_output_sonic_bgp_neighbors_af_address_header = False
    yaml_output_sonic_bgp_neighbors_af_temp = None

    router_bgp_started = False
    neighbor_started = False
    peer_group_started = False
    router_bgp_address_family_started = False
    peer_group_advertise_started = False
    neighbor_entry_started = False
    capability_started = False
    route_map_started = False
    prefix_list_started = False
    capability_value = ""

    with open(input_file, "r") as f:
        for line in f:
            if line.startswith(router_bgp_const):
                router_bgp_started = True

            if router_bgp_started == True:
                if line.startswith(" peer-group"):
                    router_bgp_address_family_started = False
                    peer_group_started = True
                    neighbor_started = False
                if line.strip().startswith("neighbor"):
                    router_bgp_address_family_started = False
                    neighbor_started = True
                    peer_group_started = False

                if peer_group_started == False and neighbor_started == False:
                    if line.strip().startswith("address-family"):
                        router_bgp_address_family_started = True
                    if router_bgp_address_family_started == True:
                        if line.strip().startswith("address-family"):
                            yaml_output_sonic_bgp_af += (
                                f"        - afi: {line.strip().split()[-2]}\n"
                            )
                            yaml_output_sonic_bgp_af += (
                                f"          safi: {line.strip().split()[-1]}\n"
                            )

                            yaml_output_sonic_bgp_af_extra_temp = (
                                f"      - afi: {line.strip().split()[-2]}\n"
                            )
                            yaml_output_sonic_bgp_af_extra_temp += (
                                f"        safi: {line.strip().split()[-1]}\n"
                            )

                        if line.strip().startswith("dampening"):
                            yaml_output_sonic_bgp_af += "          dampening: True\n"

                        if line.strip().startswith("redistribute connected"):
                            yaml_output_sonic_bgp_af += "          redistribute:\n"
                            yaml_output_sonic_bgp_af += (
                                "            - protocol: connected\n"
                            )

                        if line.strip().startswith("advertise-all-vni"):
                            yaml_output_sonic_bgp_af += (
                                "          advertise_all_vni: true\n"
                            )

                        if line.strip().startswith("advertise-default-gw"):
                            yaml_output_sonic_bgp_af += (
                                "          advertise_default_gw: true\n"
                            )

                        if "maximum-paths" in line and "ibgp" not in line:
                            yaml_output_sonic_bgp_af += "          max_path:\n"
                            yaml_output_sonic_bgp_af += (
                                f"            ebgp: {line.strip().split()[-1]}\n"
                            )

                        if "maximum-paths" in line and "ibgp" in line:
                            yaml_output_sonic_bgp_af += (
                                f"            ibgp: {line.strip().split()[-1]}\n"
                            )

                        if line.strip().startswith("advertise "):
                            yaml_output_sonic_bgp_af += (
                                "          route_advertise_list:\n"
                            )
                            yaml_output_sonic_bgp_af += f"            - advertise_afi: {line.strip().split()[+1]}\n"

                        if line.strip().startswith("default-originate"):
                            if yaml_output_sonic_bgp_af_extra_started == False:
                                yaml_output_sonic_bgp_af_extra += "  address_family:\n"
                                yaml_output_sonic_bgp_af_extra += "    afis:\n"
                                yaml_output_sonic_bgp_af_extra_started = True

                            yaml_output_sonic_bgp_af_extra += (
                                yaml_output_sonic_bgp_af_extra_temp
                            )
                            yaml_output_sonic_bgp_af_extra += "        configs:\n"
                            yaml_output_sonic_bgp_af_extra += f"          - default-originate {line.strip().split()[+1]}\n"
                if peer_group_started == True:
                    if line.strip().startswith("peer-group"):
                        yaml_output_sonic_bgp_neighbors += "    peer_group:\n"
                        yaml_output_sonic_bgp_neighbors += (
                            f"      - name: {line.strip().split()[-1]}\n"
                        )

                    if line.strip().startswith("remote-as"):
                        yaml_output_sonic_bgp_neighbors += "        remote_as:\n"
                        yaml_output_sonic_bgp_neighbors += (
                            f"          peer_type: {line.strip().split()[-1]}\n"
                        )

                    if line.strip().startswith("capability"):
                        yaml_output_sonic_bgp_neighbors += "        capability:\n"
                        if line.strip().split()[-1] == "extended-nexthop":
                            capability_value = "extended_nexthop"
                        yaml_output_sonic_bgp_neighbors += (
                            f"          {capability_value}: true\n"
                        )

                    if line.strip().startswith("address-family"):
                        if peer_group_advertise_started == False:
                            peer_group_advertise_started = True
                            yaml_output_sonic_bgp_neighbors += (
                                "        address_family:\n"
                            )
                            yaml_output_sonic_bgp_neighbors += "          afis:\n"

                        if line.strip().startswith("address-family"):
                            yaml_output_sonic_bgp_neighbors += (
                                f"            - afi: {line.strip().split()[-2]}\n"
                            )
                            yaml_output_sonic_bgp_neighbors += (
                                f"              safi: {line.strip().split()[-1]}\n"
                            )

                    if line.strip().startswith("redistribute connected"):
                        yaml_output_sonic_bgp_neighbors += "            redistribute:\n"
                        yaml_output_sonic_bgp_neighbors += (
                            "              - protocol: connected\n"
                        )

                    if line.strip().startswith("advertise-all-vni"):
                        yaml_output_sonic_bgp_neighbors += (
                            "            advertise_all_vni: true\n"
                        )

                    if line.strip().startswith("advertise-default-gw"):
                        yaml_output_sonic_bgp_af += (
                            "            advertise_default_gw: true\n"
                        )

                    if "maximum-paths" in line and "ibgp" not in line:
                        yaml_output_sonic_bgp_neighbors += "            max_path:\n"
                        yaml_output_sonic_bgp_neighbors += (
                            f"              ebgp: {line.strip().split()[-1]}\n"
                        )

                    if "maximum-paths" in line and "ibgp" in line:
                        yaml_output_sonic_bgp_neighbors += (
                            f"              ibgp: {line.strip().split()[-1]}\n"
                        )

                    if line.strip().startswith("advertise "):
                        yaml_output_sonic_bgp_neighbors += (
                            "            route_advertise_list:\n"
                        )
                        yaml_output_sonic_bgp_neighbors += f"              - advertise_afi: {line.strip().split()[+1]}\n"

                    if line.strip() == "activate":
                        yaml_output_sonic_bgp_neighbors += (
                            "              activate: true\n"
                        )
                    if line.strip().startswith("allowas-in"):
                        yaml_output_sonic_bgp_neighbors += "              allowas_in:\n"
                        yaml_output_sonic_bgp_neighbors += (
                            f"                value: {line.strip().split()[-1]}\n"
                        )

                if neighbor_started == True:
                    if neighbor_entry_started == False:
                        yaml_output_sonic_bgp_neighbors += "    neighbors:\n"
                        neighbor_entry_started = True
                    if line.strip().startswith("neighbor"):
                        yaml_output_sonic_bgp_neighbors += (
                            f"      - neighbor: {line.strip().split()[-1]}\n"
                        )
                        yaml_output_sonic_bgp_neighbors_af_temp = line.strip().split()[
                            -1
                        ]
                        route_map_started = False
                        prefix_list_started = False
                        capability_started = False
                    if line.strip().startswith("description"):
                        yaml_output_sonic_bgp_neighbors += (
                            f"        nbr_description: {line.strip().split()[-1]}\n"
                        )

                    if line.strip().startswith("update-source"):
                        yaml_output_sonic_bgp_neighbors += (
                            f"        local_address: {line.strip().split()[-1]}\n"
                        )

                    if line.strip().startswith("capability"):
                        if capability_started == False:
                            capability_started = True
                            yaml_output_sonic_bgp_neighbors += "        capability:\n"
                        if line.strip().split()[-1] == "extended-nexthop":
                            capability_value = "extended_nexthop"
                        if line.strip().split()[-1] == "dynamic":
                            capability_value = "dynamic"
                        yaml_output_sonic_bgp_neighbors += (
                            f"          {capability_value}: true\n"
                        )
                    if line.strip().startswith("peer-group"):
                        yaml_output_sonic_bgp_neighbors += (
                            f"        peer_group: {line.strip().split()[-1]}\n"
                        )
                    if line.strip().startswith("remote-as"):
                        yaml_output_sonic_bgp_neighbors += "        remote_as:\n"
                        yaml_output_sonic_bgp_neighbors += (
                            f"          peer_as: {line.strip().split()[-1]}\n"
                        )

                    if line.strip().startswith("bfd"):
                        yaml_output_sonic_bgp_neighbors += "        bfd:\n"
                        yaml_output_sonic_bgp_neighbors += "          enabled: true\n"

                    if line.strip().startswith("address-family"):
                        yaml_output_sonic_bgp_neighbors_af_address_family_started = True
                        yaml_output_sonic_bgp_neighbors_af_extra_configs = False
                        yaml_output_sonic_bgp_neighbors_af_extra_header = ""

                    if (
                        yaml_output_sonic_bgp_neighbors_af_address_family_started
                        == True
                    ):
                        if line.strip() == "!":
                            yaml_output_sonic_bgp_neighbors_af_address_family_started = (
                                False
                            )

                        sonic_bgp_neighbors_af_extra_prefixes = [
                            "send-community",
                            "soft-reconfiguration",
                            "default-originate",
                        ]
                        if any(
                            line.strip().startswith(x)
                            for x in sonic_bgp_neighbors_af_extra_prefixes
                        ):
                            if (
                                yaml_output_sonic_bgp_neighbors_af_extra_configs
                                == False
                            ):
                                yaml_output_sonic_bgp_neighbors_af_extra += (
                                    yaml_output_sonic_bgp_neighbors_af_extra_header
                                )
                                yaml_output_sonic_bgp_neighbors_af_extra += (
                                    "      configs:\n"
                                )
                                yaml_output_sonic_bgp_neighbors_af_extra_configs = True

                            yaml_output_sonic_bgp_neighbors_af_extra += (
                                f"        - {line.strip()}\n"
                            )

                        if line.strip().startswith("address-family"):
                            if (
                                yaml_output_sonic_bgp_neighbors_af_address_header
                                == False
                            ):
                                yaml_output_sonic_bgp_neighbors_af += bgp_asn_const
                                yaml_output_sonic_bgp_neighbors_af += "    neighbors:\n"
                                yaml_output_sonic_bgp_neighbors_af_address_header = True

                            yaml_output_sonic_bgp_neighbors_af += f"      - neighbor: { yaml_output_sonic_bgp_neighbors_af_temp }\n"
                            yaml_output_sonic_bgp_neighbors_af += (
                                "        address_family:\n"
                            )
                            yaml_output_sonic_bgp_neighbors_af += (
                                f"          - afi: {line.strip().split()[-2]}\n"
                            )
                            yaml_output_sonic_bgp_neighbors_af += (
                                f"            safi: {line.strip().split()[-1]}\n"
                            )

                            yaml_output_sonic_bgp_neighbors_af_extra_header += f"  - neighbor: { yaml_output_sonic_bgp_neighbors_af_temp }\n"
                            yaml_output_sonic_bgp_neighbors_af_extra_header += (
                                "    address_family:\n"
                            )
                            yaml_output_sonic_bgp_neighbors_af_extra_header += (
                                f"      afi: {line.strip().split()[-2]}\n"
                            )
                            yaml_output_sonic_bgp_neighbors_af_extra_header += (
                                f"      safi: {line.strip().split()[-1]}\n"
                            )

                        if line.strip() == ("activate"):
                            yaml_output_sonic_bgp_neighbors_af += (
                                "            activate: true\n"
                            )

                        if line.strip().startswith("prefix-list"):
                            if prefix_list_started == False:
                                prefix_list_started = True

                            if "out" in line:
                                yaml_output_sonic_bgp_neighbors_af += (
                                    "            prefix_list_out: NSX_BBPS\n"
                                )

                        if line.strip().startswith("route-map"):
                            if route_map_started == False:
                                route_map_started = True
                                yaml_output_sonic_bgp_neighbors_af += (
                                    "            route_map:\n"
                                )

                            yaml_output_sonic_bgp_neighbors_af += (
                                f"              - name: {line.strip().split()[+1]}\n"
                            )
                            yaml_output_sonic_bgp_neighbors_af += f"                direction: {line.strip().split()[-1]}\n"

                        if line.strip() == ("default-originate"):
                            yaml_output_sonic_bgp_neighbors_af += (
                                "            ip_afi:\n"
                            )
                            yaml_output_sonic_bgp_neighbors_af += (
                                "              send_default_route: true\n"
                            )

            if line.startswith("!") and router_bgp_started == True:
                break
        with open(output_file, "a") as f:
            f.write(yaml_output_sonic_bgp_af)
            f.write(yaml_output_sonic_bgp_neighbors)
            f.write(yaml_output_sonic_bgp_af_extra)
            f.write(yaml_output_sonic_bgp_neighbors_af)
            f.write(yaml_output_sonic_bgp_neighbors_af_extra)
            f.write(newline)
        print("Created BGP 2/2")
    # endregion

    # region NTP Server

    yaml_output_sonic_ntp_servers = "sonic_ntp_servers:\n"
    yaml_output_servers = "  servers:\n"
    yaml_output_servers_found = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("ntp source-interface"):
                ntp_source_interface = line.replace("ntp source-interface", "").strip()
                yaml_output_sonic_ntp_servers += (
                    f"  source_interface: {ntp_source_interface}\n"
                )
                yaml_output_servers_found = True
                break

    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("ntp server"):
                pattern = r"ntp server (\S+) minpoll (\d+) maxpoll (\d+)"
                match = re.search(pattern, line)
                if match:
                    ntp_server = match.group(1)
                    minpoll = match.group(2)
                    maxpoll = match.group(3)

                    yaml_output_servers += f"    - server: {ntp_server}\n"
                    yaml_output_servers += f"      minpoll: {minpoll}\n"
                    yaml_output_servers += f"      maxpoll: {maxpoll}\n"
    if yaml_output_servers_found == True:
        with open(output_file, "a") as f:
            f.write("# NTP Server\n")
            f.write(yaml_output_sonic_ntp_servers)
            f.write(yaml_output_servers)
            f.write(newline)
        print("Created NTP Server")

    # endregion

    # region SNMP
    yaml_output_sonic_snmp_servers = "sonic_snmp_servers:\n"
    yaml_output_snmp_views = "  views:\n"
    yaml_output_snmp_server_host = "  snmp_server_host:\n"
    yaml_output_sonic_ip_access_list = "sonic_ip_access_list:\n"
    yaml_output_permit_entries = "    permit_entries:\n"
    yaml_output_deny_entries = "    deny_entries:\n"
    yaml_output_snmp_agentaddress = "  snmp_agentaddress:\n"
    yaml_output_snmp_agentaddress_found = False
    yaml_output_v3_privileges_set = False
    user = ""
    group = ""
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("snmp-server user"):
                pattern = r"snmp-server user\s+(?P<user>\S+)\s+group\s+(?P<group>\S+)"
                match = re.match(pattern, line)
                user = match.group("user")
                group = match.group("group")
                yaml_output_sonic_snmp_servers += f"  user_name: {user}\n"
                yaml_output_sonic_snmp_servers += f"  group_name: {group}\n"
                yaml_output_sonic_snmp_servers += "  auth_password: 'admin'\n"
                yaml_output_sonic_snmp_servers += "  priv_password: 'admin'\n"
    if user != None:
        with open(input_file, "r") as f:
            for line in f:
                if (
                    line.startswith("snmp-server group " + user)
                    or line.startswith("snmp-server group " + group)
                    and yaml_output_v3_privileges_set == False
                ):
                    yaml_output_v3_privileges_set = True
                    match = re.search(r"v3\s+\w+\s+(.*)", line)
                    if match:
                        permissions_str = match.group(1)
                        yaml_output_sonic_snmp_servers += (
                            f"  v3_privileges: {permissions_str}\n"
                        )

        with open(input_file, "r") as f:
            for line in f:
                if line.startswith("snmp-server view"):
                    pattern = r"snmp-server view (?P<permission>\w+) (?P<oid>[.\d]+) (?P<type>\w+)"
                    match = re.search(pattern, line)

                    if match:
                        permission = match.group("permission")
                        oid = match.group("oid")
                        type_snmp = match.group("type")
                        yaml_output_snmp_views += f"    - permission: {permission}\n"
                        yaml_output_snmp_views += f"      oid: '{oid}'\n"
                        yaml_output_snmp_views += f"      type: {type_snmp}\n"

        with open(input_file, "r") as f:
            source_interface = None
            for line in f:
                if line.startswith("snmp-server host"):
                    match = re.search(
                        r"snmp-server host (\S+) .* source-interface (\S+)", line
                    )
                    if source_interface == None:
                        source_interface = match.group(2)
                        yaml_output_snmp_server_host += (
                            f"    source_interface: {source_interface}\n"
                        )
                        yaml_output_snmp_server_host += "    hosts:\n"

                    hosts = match.group(1)
                    yaml_output_snmp_server_host += f"      - {hosts}\n"

                if line.startswith("snmp-server agentaddress"):
                    yaml_output_snmp_agentaddress_found = True
                    if "interface mgmt" in line:
                        yaml_output_snmp_agentaddress += (
                            "    source_interface: interface mgmt\n"
                        )
                    yaml_output_snmp_agentaddress += (
                        f"    host: {line.strip().split()[+2]}\n"
                    )

        with open(input_file, "r") as f:
            block_started = False
            ip_access_list_name = None
            for line in f:
                if line.startswith("ip access-list"):
                    block_started = True

                if block_started == True and line.startswith("!"):
                    block_started = False
                    yaml_output_sonic_ip_access_list += yaml_output_permit_entries
                    yaml_output_sonic_ip_access_list += yaml_output_deny_entries
                    yaml_output_permit_entries = "    permit_entries:\n"
                    yaml_output_deny_entries = "    deny_entries:\n"
                if block_started:
                    if line.startswith("ip access-list"):
                        ip_access_list_name = line.strip().split()[-1]
                        yaml_output_sonic_ip_access_list += (
                            f"  - name: {ip_access_list_name}\n"
                        )

                    if line.strip().startswith("seq"):
                        if "permit" in line:
                            yaml_output_permit_entries += (
                                f"      - seq: {line.strip().split()[+1]}\n"
                            )
                            if "host" in line:
                                yaml_output_permit_entries += "        host: true\n"
                                yaml_output_permit_entries += (
                                    f"        ip: {line.strip().split()[+5]}\n"
                                )

                            if "host" not in line:
                                yaml_output_permit_entries += "        host: false\n"
                                yaml_output_permit_entries += (
                                    f"        ip: {line.strip().split()[+4]}\n"
                                )

                            yaml_output_permit_entries += (
                                f"        protocol: {line.strip().split()[+3]}\n"
                            )

                            if " eq " in line:
                                yaml_output_permit_entries += (
                                    f"        allow: {line.strip().split()[-1]}\n"
                                )

                        if "deny" in line:
                            if "host" in line:
                                yaml_output_deny_entries += (
                                    f"      - ip: {line.strip().split()[+5]}\n"
                                )
                                yaml_output_deny_entries += (
                                    f"        seq: {line.strip().split()[+1]}\n"
                                )
                                yaml_output_deny_entries += "        host: true\n"

                            if "host" not in line:
                                yaml_output_deny_entries += (
                                    f"      - ip: {line.strip().split()[+5]}\n"
                                )
                                yaml_output_deny_entries += (
                                    f"        seq: {line.strip().split()[+1]}\n"
                                )
                                yaml_output_deny_entries += "        host: false\n"

                            yaml_output_deny_entries += (
                                f"        protocol: {line.strip().split()[+3]}\n"
                            )

                            if " eq " in line:
                                yaml_output_permit_entries += (
                                    f"        allow: {line.strip().split()[-1]}\n"
                                )

        yaml_output_sonic_snmp_servers += yaml_output_snmp_views
        yaml_output_sonic_snmp_servers += yaml_output_snmp_server_host
        if yaml_output_snmp_agentaddress_found == True:
            yaml_output_sonic_snmp_servers += yaml_output_snmp_agentaddress

        with open(output_file, "a") as f:
            f.write("# SNMP\n")
            f.write(yaml_output_sonic_snmp_servers)
            f.write(yaml_output_sonic_ip_access_list)
            f.write(newline)
        print("Created SNMP")
    # endregion

    # region Timezone
    clock_timezone = None
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("clock timezone"):
                clock_timezone = line.strip().split()[-1]
                break

    if clock_timezone is not None:
        data = {"sonic_timezone": clock_timezone}

        with open(output_file, "a") as f:
            f.write("# Clock Timezone\n")
            yaml.dump(data, f)
            f.write(newline)
        print("Created Clock Timezone")
    # endregion

    # region Logging Server
    yaml_output_sonic_logging_server = "sonic_logging_server:\n"
    logging_server = None
    logging_server_config_found = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("logging server"):
                logging_server = line.strip()
                logging_server_config_found = True
            else:
                logging_server = None
            if logging_server != None:
                pattern = r"logging server (\S+) remote-port (\S+) source-interface (\S+) (\S+)"
                match = re.search(pattern, logging_server)
                if match:
                    ip_address = match.group(1)
                    remote_port = match.group(2)
                    source_interface = match.group(3) + " " + match.group(4)
                    yaml_output_sonic_logging_server += (
                        f"  - logging_server: {ip_address}\n"
                    )
                    yaml_output_sonic_logging_server += (
                        f"    remote_port: {remote_port}\n"
                    )
                    yaml_output_sonic_logging_server += (
                        f"    source_interface: {source_interface}\n"
                    )
    if logging_server_config_found == True:
        with open(output_file, "a") as f:
            f.write("# Logging Server\n")
            f.write(yaml_output_sonic_logging_server)
            f.write(newline)
        print("Created Logging Server")
    # endregion

    # region router ospf
    yaml_output_router_ospf = "router_ospf:\n"
    yaml_output_router_ospf_started = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("router ospf"):
                yaml_output_router_ospf_started = True
                yaml_output_router_ospf += "  configs:\n"
                yaml_output_router_ospf += "    - router ospf\n"

            if line.strip().startswith("ospf"):
                yaml_output_router_ospf += f"    - {line.strip()}\n"

            if line.strip().startswith("area"):
                yaml_output_router_ospf += f"    - {line.strip()}\n"

            if line.startswith("!") and yaml_output_router_ospf_started == True:
                break
    if yaml_output_router_ospf_started == True:
        with open(output_file, "a") as f:
            f.write("# Router OSPF\n")
            f.write(yaml_output_router_ospf)
            f.write(newline)
        print("Created Router OSPF")
    # endregion

    # region BFD
    yaml_output_bfd_peer = "bfd_peer:\n"
    yaml_output_bfd_peer_started = False
    configs_started = False
    prefixes = ["detect-multiplier", "receive-interval", "transmit-interval"]
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("bfd"):
                yaml_output_bfd_peer_started = True

            if yaml_output_bfd_peer_started == True:
                if line.strip().startswith("peer"):
                    yaml_output_bfd_peer += f"  - peer_ip: {line.strip().split()[+1]}\n"
                    configs_started = False
                if "interface" in line:
                    yaml_output_bfd_peer += (
                        f"    interface: {line.strip().split()[+3]}\n"
                    )

                if any(line.strip().startswith(x) for x in prefixes):
                    if configs_started == False:
                        configs_started = True
                        yaml_output_bfd_peer += config_const
                    yaml_output_bfd_peer += f"      - {line.strip()}\n"
                if line.startswith("!") and yaml_output_bfd_peer_started == True:
                    break
    if yaml_output_bfd_peer_started == True:
        with open(output_file, "a") as f:
            f.write("# BFD\n")
            f.write(yaml_output_bfd_peer)
            f.write(newline)
        print("Created BFD")
    # endregion

    # region AAA
    yaml_output_sonic_aaa_authentication = "sonic_aaa:\n"
    yaml_output_sonic_aaa_authentication_started = False
    data_started = False
    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("aaa authentication"):
                yaml_output_sonic_aaa_authentication_started = True

            if yaml_output_sonic_aaa_authentication_started == True:
                if line.startswith("aaa authentication"):
                    if data_started == False:
                        data_started = True
                        yaml_output_sonic_aaa_authentication += "  authentication:\n"
                        yaml_output_sonic_aaa_authentication += "    data:\n"
                    if "failthrough enable" in line:
                        yaml_output_sonic_aaa_authentication += (
                            "      fail_through: true\n"
                        )
                    if "local" in line:
                        yaml_output_sonic_aaa_authentication += "      local: true\n"
                    if "group" in line:
                        yaml_output_sonic_aaa_authentication += (
                            f"      group: {line.strip().split()[-1]}\n"
                        )
    if data_started == True:
        with open(output_file, "a") as f:
            f.write("# AAA\n")
            f.write(yaml_output_sonic_aaa_authentication)
            f.write(newline)
        print("Created AAA")
    # endregion

    # region sonic_tacacs_server
    yaml_output_sonic_tacacs_server = "sonic_tacacs_server:\n"
    yaml_output_sonic_tacacs_server_found = False
    source_interface = None
    timeout = None
    auth_type = None
    # key = None
    server_name = None
    server_port = None
    server_priority = None
    server_vrf = None
    server_timeout = None
    server_auth_type = None
    server_key = "123"

    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("tacacs-server"):
                yaml_output_sonic_tacacs_server_found = True

                if yaml_output_sonic_tacacs_server_found == True:
                    if "source-interface" in line:
                        source_interface = line.strip().replace(
                            "tacacs-server source-interface ", ""
                        )
                    if "timeout" in line:
                        timeout = line.strip().split()[-1]
                    if "auth-type" in line:
                        auth_type = line.strip().replace("tacacs-server auth-type ", "")
                        # key = line.strip().replace("tacacs-server auth-type ", "")
                    if "host" in line:
                        server_name = line.strip().split()[+2]
                        server_port = line.strip().split()[+4]
                        server_timeout = line.strip().split()[+6]
                        server_auth_type = line.strip().split()[-5]
                        server_priority = line.strip().split()[-3]
                        server_vrf = line.strip().split()[-1]
                        server_key = "123"

    if yaml_output_sonic_tacacs_server_found == True:
        yaml_output_sonic_tacacs_server += f"  auth_type: {auth_type}\n"
        # yaml_output_sonic_tacacs_server += f"  key: {key}\n"
        yaml_output_sonic_tacacs_server += f"  source_interface: {source_interface}\n"
        yaml_output_sonic_tacacs_server += f"  timeout: {timeout}\n"
        yaml_output_sonic_tacacs_server += "  servers:\n"
        yaml_output_sonic_tacacs_server += "    host:\n"

        yaml_output_sonic_tacacs_server += f"      - name: {server_name}\n"
        yaml_output_sonic_tacacs_server += f"        port: {server_port}\n"
        yaml_output_sonic_tacacs_server += f"        auth_type: {server_auth_type}\n"
        yaml_output_sonic_tacacs_server += f"        priority: {server_priority}\n"
        yaml_output_sonic_tacacs_server += f"        timeout: {server_timeout}\n"
        yaml_output_sonic_tacacs_server += f"        vrf: {server_vrf}\n"
        yaml_output_sonic_tacacs_server += f"        key: {server_key}\n"

        with open(output_file, "a") as f:
            f.write("# TACACS\n")
            f.write(yaml_output_sonic_tacacs_server)
            f.write(newline)
        print("Created TACACS")
    # endregion


if __name__ == "__main__":
    host_name = sys.argv[1]
    all_parser(sys.argv[2], sys.argv[3])
    # dir_path = r"../Configurations/NPCI/Hyderabad/Backup"
    # out_path = r"../Configurations/NPCI/Hyderabad/Yml"
    # isExist = os.path.exists(out_path)
    # if not isExist:
    #     os.mkdir(out_path)
    # default_run_all = True
    # res = os.listdir(dir_path)
    # for all_files in res:
    #     print(all_files)
    # #     if ".txt" in all_files and all_files.startswith("HYD"):
    # #         print(all_files.replace(".txt", " ansible_host=192.168.29.88"))

    # if default_run_all:
    #     for all_files in res:
    #         if ".txt" in all_files:
    #             input_file = dir_path + "/" + all_files
    #             output_file = out_path + "/" + all_files.replace(".txt", ".yml")
    #             print(input_file, output_file)
    #             all_parser(input_file, output_file)

    #             # Open the file in read mode
    #             with open(output_file, "r") as file:
    #                 # Read the contents of the file into a variable
    #                 contents = file.read()

    #             # Replace all single quotes with double quotes
    #             modified_contents = contents.replace("'", '"')
    #             modified_contents = modified_contents.rstrip("\n")
    #             # Open the file in write mode
    #             with open(output_file, "w") as file:
    #                 # Write the modified contents back to the file
    #                 file.write(modified_contents)
    # else:
    #     input_file_name = "CHN-SIR-F1E-R147-SSPINE-BBPS-Z9432F-SW01.txt"
    #     output_file_name = input_file_name.replace(".txt", ".yml")
    #     input_file = "/Users/hareesh/Desktop/NPCI/Config_Backup/" + input_file_name
    #     output_file = "/Users/hareesh/Desktop/NPCI/Created_Yaml/" + output_file_name
    #     all_parser(input_file, output_file)
    #     # Open the file in read mode
    #     with open(output_file, "r") as file:
    #         # Read the contents of the file into a variable
    #         contents = file.read()

    #     # Replace all single quotes with double quotes
    #     modified_contents = contents.replace("'", '"')
    #     modified_contents = modified_contents.rstrip("\n")

    #     # Open the file in write mode
    #     with open(output_file, "w") as file:
    #         # Write the modified contents back to the file
    #         file.write(modified_contents)

    #     # Open the file in write mode
    #     with open(output_file, "w") as file:
    #         # Write the modified contents back to the file
    #         file.write(modified_contents)
