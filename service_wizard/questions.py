"""This is a home for functions that calculate arguments based on various user
inputs.
"""


import sys

import yaml

from service_wizard.prompt import ask
from service_wizard.autosuggest import suggest_smartstack_proxy_port


def _yamlize(contents):
    return yaml.dump(contents, explicit_start=True, default_flow_style=False)


def get_srvname(srvname, auto):
    if srvname is None:
        if auto:
            sys.exit("I'd Really Rather You Didn't Use --auto Without --service-name")
        while not srvname:
            srvname = ask('Service name?')
    return srvname


def get_smartstack_stanza(yelpsoa_config_root, auto, port, legacy_style=False):
    if port is None:
        suggested_port = suggest_smartstack_proxy_port(yelpsoa_config_root)
        if auto:
            port = suggested_port
        else:
            port = ask("Smartstack proxy_port?", suggested_port)
    smartstack_stanza = {}
    key_name = "main"
    if legacy_style:
        key_name = "smartstack"
    smartstack_stanza[key_name] = {
        "proxy_port": int(port),
        "healthcheck_uri": "/",
    }
    return smartstack_stanza


def get_marathon_stanza():
    stanza = {}
    stanza["main"] = {
        "cpu": 1,
        "mem": 100,
        "instances": 3,
    }
    stanza["canary"] = {
        "cpu": 1,
        "mem": 100,
        "nerve_ns": "main",
    }
    return stanza


def get_monitoring_stanza():
    stanza = {}
    stanza["team"] = "mesos"
    stanza["notification_email"] = "jrm@yelp.com"
    return stanza