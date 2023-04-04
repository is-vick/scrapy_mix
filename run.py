from scrapy_mix.core.clawer import Clawer
import time
clawer = Clawer()
t = time.time()
clawer.main()
print(time.time()-t)
