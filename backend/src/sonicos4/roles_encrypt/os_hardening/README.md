# todo - Change / Incremental Changes

# no ip anycast-mac-address 02:01:e9:a1:a1:a1

# then add new anycast-mac-address

# without removing old mac it wont allow updating new

# above commands are tested on sonic-cli and working fine

# todo - Change / Incremental Changes

# ipv6 anycast-address disable

# ipv4 anycast-address disable

# no ip anycast-mac-address 02:01:e9:a1:a1:a1

# above commands are tested on sonic-cli and working fine

# - name: Read file contents

# set_fact:

# file_contents: "{{ lookup('file', 'configs_backup/' + inventory_hostname + '.txt') }}"

# - name: Find anycast MAC address

# set_fact:

# anycast_mac_address_configured: "{{ item.split()[2] }}"

# loop: "{{ file_contents.split('\n') }}"

# when:

# - anycast_mac_address_configured is not defined

# - item.split("\n") | regex_search("ip anycast-mac-address")

# vars:

# connection: httpapi

# - name: Debug anycast MAC address

# debug:

# var: anycast_mac_address_configured
