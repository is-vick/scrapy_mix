# staker Type ['SStack', 'LStack', 'LifoQueue']
ENGINE_STACKER_TYPE = 'SStack'

# engine num
ENGINE_NUM = 10

# delay second
DELAY = 1

# pipelines
PIPES = {
    'wparts.pipeline.Pipeline': 200
}

# middlewires
MIDWARES = {
    'wparts.middlewires.Middleware': 200
}

# trees
TREES = {
    'wparts.trees.SpiderTree': 200
         }
# start downloader or not
AIOHTTPDOWNLOADER = True
SELENIUMDOWNLOADER = True