#coding=utf8

"""
every opt of used should be define first
this options is based on tornado.options
"""

from tornado.options import define, parse_command_line,\
        parse_config_file, options

common_opts = [
        {
            "name": 'debug',
            "default": True,
            "help": 'if logged debug info',
            "type": bool,
        },
        {
            "name": 'config',
            "default": './etc/dbc.conf',
            "help": 'path of config file',
            "type": str,
            "callback": lambda path: parse_config_file(path, final=False)
        },
        {
            "name": 'api_port',
            "default": 8080,
            "help": 'listen port of api',
            "type": int,
        },
        {
            "name": 'genesis_file',
            "default": "",
            "help": 'a json file to create genesis block',
            "type": str,
        },
        {
            "name": 'peer_nodes',
            "default": "http://localhost:8080,http://localhost:8081",
            "help": 'uris used to sync info',
            "type": str,
        },
        {
            "name": 'mine',
            "default": False,
            "help": 'Enable mining',
            "type": bool,
        },
        {
            "name": 'chain_dir',
            "default": "./data",
            "help": 'all chain data store in this dir',
            "type": str,
        },
        {
            "name": 'max_block_interval',
            "default": 10,
            "help": 'max seconds between block generate',
            "type": int,
        },
        {
            "name": 'start_stage_reward',
            "default": 100,
            "help": 'how many coin reward start stage reward',
            "type": int,
        },
        {
            "name": 'half_interval',
            "default": 10000,
            "help": 'reward halved between this block',
            "type": int,
        },
        {
            "name": "block_path_format",
            "default": "%s/block/%s.json",
            "help": "the path to save block file in python format",
            "type": str,
        },
        {
            "name": "block_trans_size",
            "default": 5,
            "help": "how many trans in one block",
            "type": int,
        },
        {
            "name": "block_diffity",
            "default": 3,
            "help": "how many trans in one block",
            "type": int,
        }
        ]


def register_opt(opt, group=None):
    """Register an option schema
    opt = {
            "name": 'config',
            "default": 'ops.conf',
            "help": 'path of config file',
            "tyle": str,
            "callback": lambda path: parse_config_file(path, final=False)
        }
    """
    if opt.get('name', ''):
        optname = opt.pop('name')
        if optname in options._options.keys():
            options._options.pop(optname)
        define(optname, **opt)


def register_opts(opts, group=None):
    """Register multiple option schemas at once."""
    for opt in opts:
        register_opt(opt, group)
    return options

def get_options(opts=None, group=None):
    if opts:
        register_opts(opts, group)
    options = register_opts(common_opts, 'common')
    parse_command_line()
    return options

if __name__ == "__main__":
    options = get_options().as_dict()
    print options.get('config', None)
