import os
import time

from django.contrib.auth.models import User

from selenium.webdriver.common.keys import Keys

from nimble.forms.feature import FeatureForm
from nimble.forms.profile import ProfileForm
from nimble.models.debt import Debt
from nimble.models.feature import Feature


def wait_for_firefox(selenium):
    pause = int(os.environ.get('FIREFOX_PAUSE', 5))
    if hasattr(selenium, 'firefox_profile'):
        time.sleep(pause)


def test_change_theme(selenium, live_server, mocker):
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
    # He attempts to change it to Sandstone, but somehow manages to sender
    # corrupt data.
    mocker.patch.object(ProfileForm, 'is_valid', return_value=False)
    theme = selenium.find_element_by_id('id_theme')
    for option in theme.find_elements_by_tag_name('option'):
        if option.text == 'Sandstone':
            option.click()
            break
    button = selenium.find_element_by_name('submit')
    button.click()
    wait_for_firefox(selenium)
    # The server ignores the corrupt data and leaves the theme as superhero.
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
    # Fred opens his Nimble shortcut for stories.
    selenium.get(live_server.url + '/nimble/stories/')
    # His browser opens full screen.
    selenium.set_window_size(1920, 1080)
    login(selenium, 'fflint', 'wilma')
    # He scans the list of stories presented.
    table = selenium.find_element_by_id('stories_table')
    body = table.find_element_by_tag_name('tbody')
    rows = body.find_elements_by_tag_name('tr')
    assert debt.name() in rows[0].text
    assert debt.title in rows[0].text
    assert debt.author.get_full_name() in rows[0].text
    assert feature.name() in rows[1].text
    assert feature.title in rows[1].text
    assert feature.author.get_full_name() in rows[1].text
    # Fred finds the feature story and clicks the link.
    link = rows[1].find_element_by_tag_name('a')
    link.click()
    wait_for_firefox(selenium)
    # He corrects the form.
    title = selenium.find_element_by_name('title')
    for i in range(0, 19):
        title.send_keys(Keys.BACKSPACE)
    title.send_keys('User can pick from a list of themes')
    wait_for_firefox(selenium)
    button = selenium.find_element_by_name('submit')
    button.click()
    wait_for_firefox(selenium)
    # Return back to the story list.
    selenium.get(live_server.url + '/nimble/stories/')
    wait_for_firefox(selenium)
    # Fred sees the title has changed.
    table = selenium.find_element_by_id('stories_table')
    body = table.find_element_by_tag_name('tbody')
    rows = body.find_elements_by_tag_name('tr')
    assert 'User can pick from a list of themes' in rows[1].text
    # Fred goes back into the feature.
    link = rows[1].find_element_by_tag_name('a')
    link.click()
    wait_for_firefox(selenium)
    # And clicks the API link.
    api_link = selenium.find_element_by_name('API')
    api_link.click()
    wait_for_firefox(selenium)
    # He confirms that the link has forwarded him to the API.
    assert 'Feature Instance' in selenium.title
    assert 'Django REST framework' in selenium.title


def test_bad_idents(selenium, live_server, mocker):
    fred = create_fred()
    feature = Feature.objects.create(author=fred, title='User can pick theme')
    # Fred opens his Nimble shortcut for stories.
    selenium.get(live_server.url + '/nimble/')
    # His browser opens full screen.
    selenium.set_window_size(1920, 1080)
    login(selenium, 'fflint', 'wilma')
    # Attempt to access feature via Debt ID.
    selenium.get(live_server.url + '/nimble/D{}'.format(feature.pk))
    assert 'Not Found' in selenium.page_source
    selenium.get(live_server.url + '/nimble/F{}'.format(feature.pk))
    wait_for_firefox(selenium)
    mocker.patch.object(FeatureForm, 'is_valid', return_value=False)
    title = selenium.find_element_by_name('title')
    for i in range(0, 19):
        title.send_keys(Keys.BACKSPACE)
    title.send_keys('User can pick from a list of themes')
    wait_for_firefox(selenium)
    button = selenium.find_element_by_name('submit')
    button.click()
    wait_for_firefox(selenium)
    # The form was repopulated with the invalid content.
    time.sleep(20)
    title2 = selenium.find_element_by_name('title')
    assert 'User can pick from a list of themes' in title2.get_attribute(
        'value'
    )
