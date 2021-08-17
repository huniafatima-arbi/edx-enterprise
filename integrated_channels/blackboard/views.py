"""
Views containing APIs for Blackboard integrated channel
"""

import base64

import requests
from rest_framework import generics
from rest_framework.exceptions import APIException, NotFound, ParseError
from rest_framework.response import Response
from six.moves.urllib.parse import urljoin

from django.apps import apps
from django.conf import settings

from enterprise.utils import get_enterprise_customer
from integrated_channels.blackboard.models import BlackboardEnterpriseCustomerConfiguration

# TODO: Refactor candidate (duplication with canvas views.py)


class BlackboardCompleteOAuthView(generics.ListAPIView):
    """
        **Use Cases**

            Retrieve and save a Blackboard OAuth refresh token after an enterprise customer
            authorizes to integrated courses. Typically for use to plug into the redirect_uri field
            in visiting the 'authorizationcode' endpoint:
            Ref: https://developer.blackboard.com/portal/displayApi/Learn
            e.g. https://blackboard.edx.us.org/learn/api/public/v1/oauth2/
                 authorizationcode?redirect_uri={{this_endpoint}}&response_type=code
                 &client_id={{app id}}&state={{enterprise_uuid}}

        **Example Requests**

            GET /blackboard/oauth-complete?code=123abc&state=abc123

        **Query Parameters for GET**

            * code: The one time use string generated by the Blackboard API used to fetch the
            access and refresh tokens for integrating with Blackboard.

            * state: The user's enterprise customer uuid used to associate the incoming
            code with an enterprise configuration model.

        **Response Values**

            HTTP 200 "OK" if successful

            HTTP 400 if code/state is not provided

            HTTP 404 if state is not valid or contained in the set of registered enterprises

    """
    def get(self, request, *args, **kwargs):
        app_config = apps.get_app_config('blackboard')
        oauth_token_path = app_config.oauth_token_auth_path

        # Check if encountered an error when generating the oauth code.
        request_error = request.GET.get('error')
        if request_error:
            raise APIException(
                "Blackboard OAuth API encountered an error when generating client code - "
                "error: {} description: {}".format(
                    request_error,
                    request.GET.get('error_description')
                )
            )

        # Retrieve the newly generated code and state (Enterprise user's ID)
        client_code = request.GET.get('code')
        enterprise_customer_uuid = request.GET.get('state')
        if not enterprise_customer_uuid:
            raise ParseError("Enterprise ID (as 'state' url param) needed to obtain refresh token")

        if not client_code:
            raise ParseError("'code' url param was not provided, needed to obtain refresh token")

        enterprise_customer = get_enterprise_customer(enterprise_customer_uuid)
        if not enterprise_customer:
            raise NotFound("No enterprise data found for given uuid: {}."
                           .format(enterprise_customer_uuid))

        try:
            enterprise_config = BlackboardEnterpriseCustomerConfiguration.objects.get(
                enterprise_customer=enterprise_customer
            )
        except BlackboardEnterpriseCustomerConfiguration.DoesNotExist as error:
            raise NotFound(
                "No Blackboard configuration found for enterprise: {}".format(enterprise_customer_uuid)
            ) from error

        auth_header = self._create_auth_header(enterprise_config)

        access_token_request_params = {
            'grant_type': 'authorization_code',
            'redirect_uri': settings.LMS_INTERNAL_ROOT_URL + "/blackboard/oauth-complete",
            'code': client_code,
        }

        auth_token_url = urljoin(enterprise_config.blackboard_base_url, oauth_token_path)
        auth_response = requests.post(
            auth_token_url,
            access_token_request_params,
            headers={
                'Authorization': auth_header,
                'Content-Type': 'application/x-www-form-urlencoded'
            })

        try:
            data = auth_response.json()
            refresh_token = data['refresh_token']
        except KeyError as exception:
            raise ParseError(
                "BLACKBOARD: failed to find refresh_token in auth response. "
                "Auth response text: {}, Response code: {}, JSON response: {}".format(
                    auth_response.text,
                    auth_response.status_code,
                    data,
                )
            ) from exception
        except ValueError as exception:
            raise ParseError(
                "BLACKBOARD: auth response is invalid json. auth_response: {}".format(auth_response)
            ) from exception

        enterprise_config.refresh_token = refresh_token
        enterprise_config.save()

        return Response()

    def _create_auth_header(self, enterprise_config):
        """
        Auth header in oauth2 token format as per Blackboard doc
        """
        return 'Basic {}'.format(
            base64.b64encode(u'{key}:{secret}'.format(
                key=enterprise_config.client_id, secret=enterprise_config.client_secret
            ).encode('utf-8')).decode()
        )
