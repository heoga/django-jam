import os
import time

from django.contrib.auth.models import User

from nimble.models.debt import Debt
from nimble.models.feature import Feature


def wait_for_firefox(selenium):
    pause = int(os.environ.get('FIREFOX_PAUSE', 1))
    if hasattr(selenium, 'firefox_profile'):
        time.sleep(pause)


def test_change_theme(selenium, live_server):
    User.objects.create_user(
        username="fflint", email="fred@bedrock.com", password="wilma",
        first_name="Fred", last_name="Flintstone"
    )
    # Fred opens his Nimble link.
    selenium.get(live_server.url + '/nimble/')
    # His browser opens full screen.
    selenium.set_window_size(1920, 1080)
    # He enters his username.
    user_field = selenium.find_element_by_name('username')
    user_field.send_keys('fflint')
    # And password (should pick something more secure).
    password_field = selenium.find_element_by_name('password')
    password_field.send_keys('wilma')
    # And logs in.
    button = selenium.find_element_by_name('login')
    button.click()
    wait_for_firefox(selenium)
    # He notices the scheme is cerulean, a bit too bright for his tastes.
    css_links = selenium.find_elements_by_tag_name('link')
    assert any([
        'cerulean' in d for d in [c.get_attribute('href') for c in css_links]
    ])
    # He double checks, it is him that's logged in.
    menu = selenium.find_element_by_id('user_menu')
    assert "Fred Flintstone" in menu.text
    # He goes to the control panel
    menu.click()
    selenium.find_element_by_id('control_panel').click()
    wait_for_firefox(selenium)
    # He changes the theme to superhero.
    theme = selenium.find_element_by_id('id_theme')
    for option in theme.find_elements_by_tag_name('option'):
        if option.text == 'Superhero':
            option.click()
            break
    button = selenium.find_element_by_name('submit')
    button.click()
    wait_for_firefox(selenium)
    # And is happy to see the theme change.
    css_links = selenium.find_elements_by_tag_name('link')
    assert any([
        'superhero' in d for d in [c.get_attribute('href') for c in css_links]
    ])


def create_fred():
    return User.objects.create_user(
        username="fflint", email="fred@bedrock.com", password="wilma",
        first_name="Fred", last_name="Flintstone"
    )


def login(selenium, user, password):
    # He enters his username.
    user_field = selenium.find_element_by_name('username')
    user_field.send_keys(user)
    # And password (should pick something more secure).
    password_field = selenium.find_element_by_name('password')
    password_field.send_keys(password)
    # And logs in.
    button = selenium.find_element_by_name('login')
    button.click()
    wait_for_firefox(selenium)


def test_view_stories(selenium, live_server):
    fred = create_fred()
    debt = Debt.objects.create(author=fred, title='Fix bad code style')
    feature = Feature.objects.create(author=fred, title='User can pick theme')
    # Fred opens his Nimble link.
    selenium.get(live_server.url + '/nimble/stories/')
    # His browser opens full screen.
    selenium.set_window_size(1920, 1080)
    login(selenium, 'fflint', 'wilma')
    table = selenium.find_element_by_id('stories_table')
    rows = table.find_elements_by_tag_name('tr')
    assert debt.name() in rows[0].text
    assert debt.title in rows[0].text
    assert debt.author.get_full_name() in rows[0].text
    assert feature.name() in rows[1].text
    assert feature.title in rows[1].text
    assert feature.author.get_full_name() in rows[1].text
