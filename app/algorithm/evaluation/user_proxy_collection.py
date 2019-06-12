
'''
Provide a userProxy collection for client to 
** access all userProxy**
'''
from .simple_user_proxy import SimpleUserproxy
from .keyword_user_proxy import KeywordUserProxy
from .keyword_enhance_user_proxy import KeywordEnhanceUserProxy
from .proxy_for_remember_preference import ProxyForRememberPreference

class UserProxyCollection():
    default_proxy = KeywordEnhanceUserProxy
    proxys = (
        SimpleUserproxy,
        KeywordUserProxy,
        KeywordEnhanceUserProxy,
        ProxyForRememberPreference
    )
    