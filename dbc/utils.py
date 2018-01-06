import os
import json

from dbc.options import get_options

options = get_options()

def get_miner_addr():
    mine_file = "%s/miner_addr" % options.chain_dir
    if os.path.isfile(mine_file):
        file_content = file(mine_file, 'r').read()
        mine_json = json.loads(file_content)
        return mine_json.get('mine_to', '')
    return ''

def get_reward(index):
    reward = '%.8f' % (options.start_stage_reward / float(2 ** (index/options.half_interval)))
    reward = float(reward)
    if reward < 1e-08:
        reward = 0
    return reward
