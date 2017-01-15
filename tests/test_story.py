import pytest

from factories import UserFactory
from nimble.models.story import Story


@pytest.mark.django_db
def test_title_max_length():
    assert Story._meta.get_field('title').max_length == 100


@pytest.mark.django_db
def test_story_creation():
    user = UserFactory()
    a = Story.create(
        author=user, title='My Title', description='Something or other'
    )
    assert a.id is not None


@pytest.mark.django_db
def test_story_update():
    user = UserFactory()
    a = Story.create(
        author=user, title='My Title', description='Something or other'
    )
    assert a.id is not None
    assert a.title == 'My Title'
    assert a.description == 'Something or other'
    data = {
        'title': 'Different title', 'description': 'Something else',
    }
    a.update(user, data)
    refreshed = Story.objects.get(id=a.id)
    assert refreshed.title == 'Different title'
    assert refreshed.description == 'Something else'
