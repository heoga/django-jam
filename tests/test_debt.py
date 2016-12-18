import pytest

from factories import UserFactory

from nimble.models import Debt


@pytest.mark.django_db
def test_name():
    user = UserFactory()
    debt = Debt.objects.create(
        author=user, title='Fix bad code',
    )
    assert debt.name() == 'D{:0>5}'.format(debt.id)
