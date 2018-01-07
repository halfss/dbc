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

def get_reward_trans(index, miner_address):
    reward = get_reward(index)
    if reward < 1e-08:
        reward = 0
    coin_trans = {
        u"from": 0,
        u"to": u'%s' % miner_address,
        u"assets":{u"coin": reward}
    }
    return coin_trans
