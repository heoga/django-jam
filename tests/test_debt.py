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


@pytest.mark.django_db
def test_debt_creation():
    user = UserFactory()
    a = Debt.create(
        author=user, title='My Title', description='Something or other'
    )
    assert a.id is not None
    assert isinstance(a, Debt)
