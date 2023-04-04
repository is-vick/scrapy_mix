from scrapy_mix.core.clawer import Clawer
import time
clawer = Clawer()
t = time.time()
clawer.core()
print(time.time()-t)
