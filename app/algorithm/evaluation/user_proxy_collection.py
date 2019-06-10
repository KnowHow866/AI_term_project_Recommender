
'''
Provide a userProxy collection for client to 
** access all userProxy**
'''
from .simple_user_proxy import SimpleUserproxy

class UserProxyCollection():
    default_proxy = SimpleUserproxy
    proxys = (
        SimpleUserproxy,
    )
    