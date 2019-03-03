from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from contact.models import *


class RolePrivilegeMiddleware(TokenAuthentication):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is logged-in, fetch the role from the table account_profile
        # table where account_profile.user_id = authenticated user's id.
        # Also, fetch the privileges from account_privilege for the role identified
        # above. Finally, add the role and privilege attributes to the request object's
        # auth attribute
        response = self.get_response(request)
        a = response.request
        return response


class MyAuthenticationClass(TokenAuthentication):
    def authenticate(self, request):
        response = super(MyAuthenticationClass, self).authenticate(request)

        request.privileges = []
        request.roles = []

        if response is not None:
            try:
                for rolemap in response[0].rolemap.all():
                    request.privileges.extend([j['operation'] for i in [rolemap.role.get_privileges()] for j in i])
                    request.roles.append(rolemap.role.get_homeassure_role())
            except:
                pass

        return response

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token

