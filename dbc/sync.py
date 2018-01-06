#coding=utf8
import datetime
import requests
import time

from dbc.options import get_options
from dbc.block import Block, get_last_block

options = get_options()

def sync(state):
    peer_nodes = state.peer_nodes
    longest_peer, max_id = get_longest_peer(peer_nodes)
    if max_id > get_last_block()['index']:
        print "%s(%s) is larger than %s(local max)" % (max_id, longest_peer, state.block['index'])
        sync_block_range(longest_peer, state.block['index'], max_id, state)

def sync_all(peer_nodes):
    longest_peer, max_id = get_longest_peer(peer_nodes)
    print longest_peer, 0, max_id
    sync_block_range(longest_peer, -1, max_id)

def sync_block_range(peer, start, end, state=''):
    for i in range(start+1, end+1):
        block_json = requests.get("%s/block/%s" % (peer, i)).json()
        if state.trans:
            for tran in block_json['data'].get('trans', []):
                tran_hash = state.trans_hash(str(tran))
                if tran_hash in state.trans_hash:
                    print "trans %s is blocked" % tran
                    trans_index = state.trans_hash.index(tran_hash)
                    state.trans.pop(tran)
                    state.trans_hash.pop(trans_hash)
        print "block %s is %s" % (i, block_json)
        block = Block(block_json['index'],
                block_json['timestamp'],
                block_json['data'],
                block_json['previous_hash'],
                block_json['nonce'],
                block_json['hash'],
                sync=True)
        block.save()


def get_longest_peer(peer_nodes):
    max_id = 0
    peer_node = ''
    for peer in peer_nodes:
        print "%s/block" % peer
        r = requests.get("%s/block" % peer)
        if r.status_code == 200:
            if r.json()['index'] > max_id:
                max_id = r.json()['index']
                peer_node = peer
    return peer, max_id
