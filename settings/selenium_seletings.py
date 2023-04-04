# ****************************** SeleniumDwonloader Settings *********************************
from selenium import webdriver

# ************************************** 1.options *******************************************
options = webdriver.ChromeOptions()

# 设置无界面模式
# options.add_argument('--headless')

# 设置浏览器不关闭
# options.add_experimental_option('detach', True)

# 更改UserAgent
# options.add_argument('UserAgent=%s' % ua.random)

# 设置浏览器分辨率（窗口大小）
# options.add_argument("--window-size=1920,1080")

# 隐身模式（无痕模式）
options.add_argument('--incognito')

# 禁用扩展
options.add_argument("--disable-extensions")

# 禁用GPU加速
options.add_argument("--disable-gpu")

# 禁用 3D 软件光栅化器
options.add_argument("--disable-software-rasterizer")

# 禁用javascript
options.add_argument('--disable-javascript')  

# 解决DevToolsActivePort文件不存在的报错
options.add_argument('--no-sandbox')

# 设置Chrome忽略网站证书错误
options.add_argument('--ignore-certificate-errors')

# 默认情况下，https 页面不允许从 http 链接引用 javascript/css/plug-ins。添加这一参数会放行这些内容。
options.add_argument('--allow-running-insecure-content')

# 不加载图片, 提升速度
options.add_argument("blink-settings=imagesEnabled=false")

# 去掉webdriver日志
options.add_argument("disable-blink-features=AutomationControlled")

# 通过Log读取XHR 构造chrome driver：
options.add_argument("--allow-running-insecure-content")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-single-click-autofill")
options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
options.add_argument("--disable-full-form-autofill-ios")
options.add_experimental_option('perfLoggingPrefs', {
    'enableNetwork': True,
    'enablePage': False,
})

# ************************************** 2.desired_capabilities *******************************************

desired_capabilities = webdriver.DesiredCapabilities.CHROME
desired_capabilities['goog:loggingPrefs'] = {
    'browser': 'ALL',
    'performance': 'ALL',
}
desired_capabilities['perfLoggingPrefs'] = {
    'enableNetwork': True,
    'enablePage': False,
    'enableTimeline': False
}