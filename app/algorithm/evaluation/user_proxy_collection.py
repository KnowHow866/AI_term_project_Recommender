
'''
Provide a userProxy collection for client to 
** access all userProxy**
'''
from .simple_user_proxy import SimpleUserproxy
from .keyword_user_proxy import KeywordUserProxy
from .keyword_enhance_user_proxy import KeywordEnhanceUserProxy

class UserProxyCollection():
    default_proxy = KeywordEnhanceUserProxy
    proxys = (
        SimpleUserproxy,
        KeywordUserProxy,
        KeywordEnhanceUserProxy
    )
    