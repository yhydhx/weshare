#-*- coding:utf-8 -*-  
  
class settings:  
  # 安全检验码，以数字和字母组成的32位字符  
  ALIPAY_KEY = 'ogdhuv0vu7mwyfnvpyox6qctjgo4n2oq'  
  
  ALIPAY_INPUT_CHARSET = 'utf-8'  
  
  # 合作身份者ID，以2088开头的16位纯数字  
  ALIPAY_PARTNER = '2088421797331962'  
  
  # app端支付的APP ID
  ALIPAY_APP_ID = '2016090101833175'
  
  
  # 签约支付宝账号或卖家支付宝帐户  
  ALIPAY_SELLER_EMAIL = 'wesharehere@163.com'  
  
  ALIPAY_SIGN_TYPE = 'MD5'  

  ALIPAY_APP_SIGN_TYPE = "RSA"
  
  # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数  
  ALIPAY_RETURN_URL='http://www.wshere.com/alipay/return'  
  
  # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数  
  ALIPAY_NOTIFY_URL='http://www.wshere.com/alipay/notify'  

  # 不知道什么东西，集成中需要
  ALIPAY_SHOW_URL='http://www.wshere.com/alipay/show'  