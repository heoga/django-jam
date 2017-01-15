import pytest

from nimble.models.story import Story


@pytest.mark.django_db
def test_title_max_length():
    assert Story._meta.get_field('title').max_length == 100
