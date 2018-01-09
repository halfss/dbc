#coding=utf8
import datetime
import requests
import time

from dbc.options import get_options
from dbc.block import Block, get_last_block
from dbc.log import LOG

options = get_options()

def sync(state):
    peer_nodes = state.peer_nodes
    longest_peer, max_id = get_longest_peer(peer_nodes)
    if max_id > get_last_block()['index']:
        LOG.debug("%s(%s) is larger than %s(local max)" % (max_id, longest_peer, state.block['index']))
        sync_block_range(longest_peer, state.block['index'], max_id, state)

def sync_all(peer_nodes):
    longest_peer, max_id = get_longest_peer(peer_nodes)
    sync_block_range(longest_peer, -1, max_id)

def sync_block_range(peer, start, end, state=''):
    for i in range(start+1, end+1):
        block_json = requests.get("%s/block/%s" % (peer, i)).json()
        block = Block(block_json['index'],
                block_json['timestamp'],
                block_json['data'],
                block_json['previous_hash'],
                block_json['nonce'],
                block_json['hash'],
                sync=True)
        block.save()
        time.sleep(0.1)


def get_longest_peer(peer_nodes):
    max_id = 0
    peer_node = ''
    for peer in peer_nodes:
        LOG.debug("Get %s/block info" % peer)
        r = requests.get("%s/block" % peer)
        if r.status_code == 200:
            LOG.debug("Remote block id is %ss" % r.json()['index'])
            if r.json()['index'] > max_id:
                max_id = r.json()['index']
                peer_node = peer
    return peer, max_id
