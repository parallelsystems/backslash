import logbook
import os 

from flask import current_app, request
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
import requests
import msal

from .. import config


_logger = logbook.Logger(__name__)


def get_oauth2_identity(auth_code):

    config_dict = config.get_runtime_config_private_dict()
    client_id = config_dict['google_oauth2_client_id']
    client_secret = config_dict['google_oauth2_client_secret']
    if not client_id:
        _logger.error('No OAuth2 client id configured')
        return

    if not client_secret:
        _logger.error('No OAuth2 client secret configured')
        return

    redirect_uri = request.host_url[:-1]

    _logger.debug('get_oauth2_identity: Using redirect URI {!r}', redirect_uri)

    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,

        scope='https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri=redirect_uri)

    credentials = flow.step2_exchange(auth_code)

    info = _get_user_info(credentials)
    _logger.debug('Found user info: {}', info)
    return info

def get_oauth2_identity_azure(auth_code):
    """Gets identity from azure auth_code""" 

    config_dict = config.get_runtime_config_private_dict()
    client_id = config_dict['azure_oauth2_client_id']
    client_secret = config_dict['azure_oauth2_client_secret']
    authority = f"https://login.microsoftonline.com/{config_dict['azure_oauth2_tenant_id']}"

    if not client_id:
        _logger.error('No OAuth2 client id configured')
        return

    if not client_secret:
        _logger.error('No OAuth2 client secret configured')
        return

    redirect_uri = request.host_url[:-1]

    _logger.info('get_oauth2_identity: Using redirect URI {!r}', redirect_uri)

    _logger.info("Redirect URI from the environment: {}", os.environ.get("REDIRECT_URI"))

    redirect_uri = os.environ.get("REDIRECT_URI")

    client = msal.ConfidentialClientApplication(
        client_id, authority=authority,
        client_credential=client_secret, token_cache=None)

    token = client.acquire_token_by_authorization_code(code=auth_code, scopes=["User.read"], redirect_uri=)

    if "error" in token:
        _logger.error(token["error_description"])
        assert False
    
    user_info = token["id_token_claims"]

    return {
        "email" : user_info["email"], 
        "first_name" : user_info["name"].split()[0],
        "last_name" : user_info["name"].split()[-1],
    }


def _get_user_info(credentials):
    http_client = Http()
    if credentials.access_token_expired:
        credentials.refresh(http_client)
    credentials.authorize(http_client)
    service = build('oauth2', 'v2', http=http_client)
    return service.userinfo().get().execute()
