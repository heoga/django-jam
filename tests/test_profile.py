import pytest

from django.contrib.auth.models import User
from jam.models import Profile


@pytest.mark.django_db
def test_profile_creation():
    # Create a new user.
    user = User.objects.create_user(
        username="testuser", email="test@user.com", password="testpass"
    )
    assert user.profile
    profile = user.profile
    assert Profile.objects.count() == 1
    assert Profile.objects.get(id=profile.id)
    # Check the default profile is set.
    assert profile.theme == '1'
    assert profile.theme_name() == 'Cerulean'
    # Change the profile to Flatly.
    profile.theme = '5'
    assert profile.theme_name() == 'Flatly'
    # Now change to an invalid profile.
    profile.theme = '56'
    assert profile.theme_name() is None
    # Save something on the user.
    user.first_name = 'Fred'
    user.save()
    # Now check when the user is deleted, the profile goes as well.
    user.delete()
    with pytest.raises(Profile.DoesNotExist):
        Profile.objects.get(id=1)
