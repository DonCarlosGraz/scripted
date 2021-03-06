#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SSH fabric commands.

:copyright: (c) 2014 by Alexander Skiba <skiba@icg.tugraz.at>
:licence: MIT
:bugreports: skiba@icg.tugraz.at

"""

from fabric.api import run, settings, hide, env, task
from fabric.contrib.files import sed
from os.path import basename, splitext
import re
import fabrications.configuration as config

# module configuration ########################################################


MODULE = splitext(basename(__file__))[0]
CONFIGURATION = config.get_configuration(MODULE)


# tasks #######################################################################


@task
def get_fingerprints():
    """(SSH) Retrieve a machine's fingerprints."""

    ssh_key_locations = ["ssh_host_dsa_key",
                         "ssh_host_key",
                         "ssh_host_rsa_key",
                         "ssh_host_ecdsa_key"]

    retrieved_keys = []

    with settings(warn_only=True), hide("stdout", "warnings"):
        for key in ssh_key_locations:
            full_key = "/etc/ssh/" + key + ".pub"
            found_key = run("ssh-keygen -l -f " + full_key)
            if found_key is not None:
                if re.match("[0-9]", found_key[0]) is not None:
                    retrieved_keys.append(found_key)

    print "\nFingerprints for {}".format(env.host)
    for key in retrieved_keys:
        print key
    print "\n"


@task
def set_password_login(boolean):
    """(SSH) Enable/Disable password login. | (bool) boolean."""

    if boolean == "True":
        sed("/etc/ssh/sshd_config", "PasswordAuthentication no",
            "#PasswordAuthentication yes", use_sudo=True)

    elif boolean == "False":
        sed("/etc/ssh/sshd_config", "#PasswordAuthentication yes",
            "PasswordAuthentication no", use_sudo=True)
