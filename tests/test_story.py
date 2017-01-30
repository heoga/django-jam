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


@pytest.mark.django_db
def test_versioning():
    user = UserFactory()
    a = Story.create(
        author=user, title='first', description='Something or other'
    )
    a.update(user, {'title': 'second'})
    a.update(user, {'title': 'third'})
    versions = a.versions()
    assert len(versions) == 3
    assert versions[0].field_dict['title'] == 'third'
    assert versions[1].field_dict['title'] == 'second'
    assert versions[2].field_dict['title'] == 'first'
    third_id = versions[0].revision.id
    second_id = versions[1].revision.id
    first_id = versions[2].revision.id
    assert a.revision_numbers() == [first_id, second_id, third_id]
    assert a.values_at_revision(second_id)['title'] == 'second'
    assert a.differences_between_revisions(first_id, second_id) == {
        'title': {'new': 'second', 'old': 'first'}
    }
    assert a.difference_tables_between_revisions(first_id, second_id) == {
        'title': (
            '<table class="table">'
            '<tr class="danger" style="font-family:monospace;">'
            '<td><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></td>'  # noqa
            '<td>first</td></tr>'
            '<tr class="success" style="font-family:monospace;">'
            '<td><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></td>'  # noqa
            '<td>second</td></tr></table>'
        )
    }
