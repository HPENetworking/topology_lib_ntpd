# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_lib_ntpd communication library implementation.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division


CONFIG_FILE = '/etc/ntp.conf'
KEYS_FILE = '/etc/ntp.keys'


def ntpd_stop(enode):
    """
    Stop the NTP daemon program.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str shell: Shell name to execute commands. If ``None``, use the
     Engine Node default shell.

    """

    cmd = '/etc/init.d/ntp stop'
    ntpd_stop_re = enode(cmd, shell='bash')

    assert 'done' in ntpd_stop_re


def add_ntp_server(enode, server):
    """
    Add an ntp server to '/etc/ntp.conf' file.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str server: Server's FQDN or IP address

    """

    assert server

    cmd = 'echo "server {server}" >> {config_file}'.format(
            server=server, config_file=CONFIG_FILE
    )

    enode(cmd, shell='bash')


def remove_ntp_server(enode, server):
    """
    Remove an ntp server in '/etc/ntp.conf' file that matches
    with received server.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str server: Server's FQDN or IP address

    """

    assert server

    cmd = "sed -i '/{server}/d' {config_file}".format(
            server=server, config_file=CONFIG_FILE
    )

    enode(cmd, shell='bash')


def add_trustedkey(enode, trustedkey_id):
    """
    Add a trustedkey to '/etc/ntp.conf' file.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param int trustedkey_id: NTP Key number

    """

    assert trustedkey_id > 0 and trustedkey_id < 65535

    cmd = 'echo "trustedkey {trustedkey_id}" >> {config_file}'.format(
            trustedkey_id=trustedkey_id, config_file=CONFIG_FILE
    )

    enode(cmd, shell='bash')


def remove_trustedkey(enode, trustedkey_id):
    """
    Remove a trustedkey in '/etc/ntp.conf' file that matches with trustedkey_id

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param int trustedkey_id: NTP Key number

    """

    assert trustedkey_id > 0 and trustedkey_id < 65535

    cmd = "sed -i '/trustedkey {trustedkey_id}/d' {config_file}".format(
            trustedkey_id=trustedkey_id, config_file=CONFIG_FILE
    )

    enode(cmd, shell='bash')


def add_trustedkey_password(enode, trustedkey_id, key, type='M'):
    """
    Add keys to '/etc/ntp.keys' file.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param int trustedkey_id: NTP Key number
    :param str key: NTP Key password
    :param str type: Hash type. Default is MD5

    """

    assert trustedkey_id > 0 and trustedkey_id < 65535
    assert key

    cmd = 'echo "{trustedkey_id} {type} {key}" >> {keys_file}'.format(
        trustedkey_id=trustedkey_id, type=type, key=key, keys_file=KEYS_FILE
    )

    enode(cmd, shell='bash')


def remove_trustedkey_password(enode, trustedkey_id):
    """
    Remove key from '/etc/ntp.keys' file that matches with trustedkey_id.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param int trustedkey_id: NTP Key number

    """

    assert trustedkey_id > 0 and trustedkey_id < 65535

    cmd = "sed -i '/{trustedkey_id}[[:space:]]/d' {keys_file}".format(
            trustedkey_id=trustedkey_id, keys_file=KEYS_FILE
    )

    enode(cmd, shell='bash')


def ntpd_config_files(enode, keyfile=False, trustedkey_id=None):
    """
    Configure the NTP daemon program in order to use '/etc/ntp.conf' as the
    configuration file, and define the keyfile path as '/etc/ntp.keys'
    if applicable

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param bool keyfile: Flag that defines if the NTP daemon should read the
     key file or not
    :param int trustedkey_id: NTP Key number

    """

    cmd = 'ntpd -c {config_file}'.format(config_file=CONFIG_FILE)

    if keyfile:
        assert trustedkey_id is not None
        cmd = cmd + ' -k {keys_file} -t {trustedkey_id}'.format(
            keys_file=KEYS_FILE, trustedkey_id=trustedkey_id
        )

    enode(cmd, shell='bash')


def ntpd_start(enode):
    """
    Start the NTP daemon program.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode

    """

    cmd = '/etc/init.d/ntp start'
    ntpd_start_re = enode(cmd, shell='bash')

    assert 'done' in ntpd_start_re


__all__ = [
    'ntpd_stop', 'add_ntp_server', 'remove_ntp_server', 'add_trustedkey',
    'remove_trustedkey', 'add_trustedkey_password',
    'remove_trustedkey_password', 'ntpd_config_files', 'ntpd_start'
]
