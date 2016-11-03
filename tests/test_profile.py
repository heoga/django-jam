from django.contrib.auth.models import User
from jam.models import Profile

import pytest


@pytest.mark.django_db
def test_creating_user_also_creates_profile():
    # Create a new user.
    user = User.objects.create_user(
        username="testuser", email="test@user.com", password="testpass"
    )
    assert user.profile
    profile = user.profile
    assert profile.profile_found() == 'Yes'
    key = profile.id
    assert key == 1
    assert Profile.objects.get(id=1)
    # Now check when the user is deleted, the profile goes as well.
    user.delete()
    with pytest.raises(Profile.DoesNotExist):
        Profile.objects.get(id=1)
