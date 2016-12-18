from django.contrib.auth.models import User

import pytest

from nimble.models import Debt, Feature, Story


@pytest.mark.django_db
def test_polymorphic_story_relations():
    # Create a new user.
    user = User.objects.create_user(
        username="testuser", email="test@user.com", password="testpass"
    )
    feature = Feature.objects.create(
        author=user, title='Cool feature',
    )
    debt = Debt.objects.create(
        author=user, title='Bad design',
    )
    # Get the stories created by this user.
    stories = Story.objects.filter(author__username='testuser')
    assert list(stories) == [feature, debt]
    assert [a.name() for a in stories] == [feature.name(), debt.name()]
