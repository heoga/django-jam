import pytest

from factories import UserFactory

from nimble.models import Feature


@pytest.mark.django_db
def test_name():
    user = UserFactory()
    feature = Feature.objects.create(
        author=user, title='Cool feature',
    )
    assert feature.name() == 'F{:0>5}'.format(feature.id)
