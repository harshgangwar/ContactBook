from django.contrib.auth.models import User
from django.db import models


"""
This model will have basic contact details of user
"""
class Contact(models.Model):
    user = models.ForeignKey(User, related_name='profiles')
    phone = models.CharField(max_length=15, blank=True)
    created_by = models.ForeignKey(User, null=True)
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('phone', 'email'),)


""" A user will has a role, through which we will define authentication"""
class Role(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get_privileges(self):
        return self.privileges.values('operation')

    def get_homeassure_role(self):
        return self


""" A privilege will define the API level authentication"""
class Privilege(models.Model):
    role = models.ForeignKey(Role, related_name='privileges')
    operation = models.CharField(max_length=200)

    def __unicode__(self):
        return u'{0}'.format(self.operation)


""" User Role mapping"""
class RoleMap(models.Model):
    user = models.ForeignKey(User, related_name='rolemap')
    role = models.ForeignKey(Role, related_name='roles')

    class Meta:
        unique_together = (('user', 'role'),)

