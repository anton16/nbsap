from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.contrib.auth import models as auth_models
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')

def create_admin(app, created_models, verbosity, **kwargs):
    if settings.DEBUG:
        try:
            auth_models.User.objects.get(username='admin')
        except auth_models.User.DoesNotExist:
            print '*' * 50
            print 'Creating admin user "admin" with password "q"'
            print '*' * 50
            assert auth_models.User.objects.create_superuser('admin',
                                                             'admin@example.com',
                                                             'q')
        else:
            print '*' * 50
            print 'Admin user is "admin" with password "q".'
            print '*' * 50

signals.post_syncdb.connect(
    create_admin,
    sender=auth_models,
    dispatch_uid='apps.auth.models.create_admin')

def logged_in_message(sender, user, request, **kwargs):
    """
    Welcome message when the user loggs in
    """
    messages.info(request, "Successfully signed in.")


def logged_out_message(sender, user, request, **kwargs):
    """
    Goodbye message when the user loggs out
    """
    messages.info(request, "Successfully signed out.")

user_logged_in.connect(logged_in_message)
user_logged_out.connect(logged_out_message)

