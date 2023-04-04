# staker Type ['SStack', 'LStack', 'LifoQueue']
ENGINE_STACKER_TYPE = 'SStack'

# engine num
ENGINE_NUM = 10

# delay second
DELAY = 1

# pipelines
PIPES = {
    'parts.pipeline.Pipeline': 200
}

# middlewires
MIDWARES = {
    'parts.middlewires.Middleware': 200
}

# tree
TREES = {
    # 'maoyan_tree.MaoYanTree': 200
    'parts.trees.SpiderTree': 200
         }

AIOHTTPDOWNLOADER = True
SELENIUMDOWNLOADER = True