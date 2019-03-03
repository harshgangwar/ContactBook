from warranty.decorators import authorize
from .models import *
from django.utils import timezone
from rest_framework.status import *
from datetime import *
from django.db.models import Q
from django.db import transaction


class ContactHandler:

    @classmethod
    @authorize('fetch_contacts')
    def list(cls, request):
        kwargs = request.query_params.dict()
        result = []
        try:
            search = kwargs.get('search')
            start = kwargs.get('start', 0)
            limit = kwargs.get('limit', 10)
            if start:
                start = start - 1 if start > 0 else 0  # Since in frontend, it always starts with index 1, not 0

            contacts = None
            if search:
                contacts = Contact.objects.filter(Q(email=search) |
                                                   Q(user__first_name=search))[start: start + limit]
            else:
                contacts = Contact.objects.all()[start: start + limit]
            count = contacts.count()
            for contact in contacts:
                result.append({
                    'Name': contact.user.first_name + contact.user.last_name,
                    'Phone': contact.phone,
                    'Email': contact.email
                })
            return 200, 'List of data', {'results': result, 'count': count}
            pass
        except Exception as ex:
            return 400, 'Something went wrong', str(ex)

    @classmethod
    @authorize('create_contacts')
    def create(cls, request):
        try:
            kwargs = request.data
            first_name = kwargs.get('first_name')
            last_name = kwargs.get('last_name')
            email = kwargs.get('email')
            phone = kwargs.get('phone')
            username = kwargs.get('username')
            password = kwargs.get('password')
            if not first_name or not last_name or not email or phone or not password or not username: # Basic check, otherwise
                                                                    # we can check with field wise and check with regex
                return 400, 'Some fields are missing', None

            with transaction.atomic():
                user_ref = User.objects.create(username=username, email=email,
                                 password=password, first_name=first_name, last_name=last_name)
                contact_ref = Contact.objects.create(user=user_ref, phone=phone, email=email, created_at=timezone.now())
                return 200, "Contact data saved", {'user id': user_ref.pk}
        except Exception as ex:
            return 400, 'Something went wrong', str(ex)

    @classmethod
    @authorize('update_contacts')
    def partial_update(cls, request, pk=None):
            try:
                payload = request.data

                contact = payload.get('contact')
                email = payload.get('email')

                if contact and not Contact.objects.filter(phone=contact).exists():
                    return HTTP_400_BAD_REQUEST, "Invalid contact details", None
                if email and Contact.objects.filter(email=email).exists():
                    return HTTP_400_BAD_REQUEST, "Invalid email id", None

                kwargs = {}
                if contact:
                    kwargs['phone'] = contact
                if email:
                    kwargs['email'] = email

                try:
                    Contact.objects.filter(id=pk).update(**kwargs)
                except Exception as ex:
                    return HTTP_400_BAD_REQUEST, "Cannot save data", {'Exception': str(ex)}

                return HTTP_200_OK, "Contact data updated", None

            except Exception as ex:
                return HTTP_400_BAD_REQUEST, "Something went wrong", {'Exception': str(ex)}

