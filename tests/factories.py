from django.contrib.auth.models import User

import factory
import factory.django


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "testuser"
    email = "test@user.com"
    password = "testpass"
