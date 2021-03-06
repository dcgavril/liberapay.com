from __future__ import absolute_import, division, print_function, unicode_literals

from liberapay.elsewhere._base import PlatformOAuth2
from liberapay.elsewhere._extractors import key
from liberapay.elsewhere._paginators import keys_paginator


class Facebook(PlatformOAuth2):

    # Platform attributes
    name = 'facebook'
    display_name = 'Facebook'
    account_url = 'https://www.facebook.com/app_scoped_user_id/{user_id}/'
    optional_user_name = True

    # Auth attributes
    auth_url = 'https://www.facebook.com/v2.10/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/v2.10/oauth/access_token'
    refresh_token_url = None
    oauth_default_scope = ['public_profile,email,user_friends']

    # API attributes
    api_format = 'json'
    api_paginator = keys_paginator('data', paging='paging', prev='previous')
    api_url = 'https://graph.facebook.com/v2.10'
    api_user_self_info_path = '/me?fields=id,name,email'
    api_friends_path = '/me/friends'
    api_friends_limited = True

    # User info extractors
    x_user_id = key('id')
    x_display_name = key('name')
    x_email = key('email')

    def x_avatar_url(self, extracted, info, default):
        return 'https://graph.facebook.com/' + extracted.user_id + '/picture?width=256&height=256'
