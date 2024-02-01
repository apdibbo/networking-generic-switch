# Copyright 2020 StackHPC
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import re

from networking_generic_switch.devices import netmiko_devices


class CumulusNVUE(netmiko_devices.NetmikoSwitch):
    """Built for Cumulus 5.x

    Note for this switch you want config like this,
    where secret is the password needed for sudo su:

    [genericswitch:<hostname>]
    device_type = netmiko_cumulus
    ip = <ip>
    username = <username>
    password = <password>
    secret = <password for sudo>
    ngs_physical_networks = physnet1
    ngs_max_connections = 1
    ngs_port_default_vlan = 123
    ngs_disable_inactive_ports = False
    """
    NETMIKO_DEVICE_TYPE = "linux"

    ADD_NETWORK = [
        'nv set bridge domain br_default vlan {segmentation_id}',
    ]

    DELETE_NETWORK = [
        'net unset bridge domain br_default vlan {segmentation_id}',
    ]

    PLUG_PORT_TO_NETWORK = [
        'nv set interface {port} bridge domain br_default untagged {segmentation_id}',
    ]

    DELETE_PORT = [
        'nv unset interface {port} bridge domain br_default untagged {segmentation_id}',
    ]

    PLUG_BOND_TO_NETWORK = [
        'nv set interface bond {bond} bridge domain br_default untagged {segmentation_id}',
    ]

    UNPLUG_BOND_FROM_NETWORK = [
        'nv unset interface bond {bond} bridge domain br_default untagged {segmentation_id}',
    ]

    ENABLE_PORT = [
        'nv set interface {port} link state up',
    ]

    DISABLE_PORT = [
        'nv set interface {port} link state down',
    ]

    ENABLE_BOND = [
        'nv set interface bond {bond} link state up',
    ]

    DISABLE_BOND = [
        'nv set interface bond {bond} link state down',
    ]

    SAVE_CONFIGURATION = [
        'nv config apply',
    ]

    ERROR_MSG_PATTERNS = [
        # Its tempting to add this error message, but as only one
        # bridge-access is allowed, we ignore that error for now:
        # re.compile(r'configuration does not have "bridge-access')
        re.compile(r'ERROR: Command not found.'),
        re.compile(r'command not found'),
        re.compile(r'is not a physical interface on this switch'),
    ]
