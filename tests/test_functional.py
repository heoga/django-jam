from django.contrib.auth.models import User


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
    button.submit()
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
    # He changes the theme to superhero.
    theme = selenium.find_element_by_id('id_theme')
    for option in theme.find_elements_by_tag_name('option'):
        if option.text == 'Superhero':
            option.click()
            break
    button = selenium.find_element_by_name('submit')
    button.submit()
    # And is happy to see the theme change.
    css_links = selenium.find_elements_by_tag_name('link')
    assert any([
        'superhero' in d for d in [c.get_attribute('href') for c in css_links]
    ])
