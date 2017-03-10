import sys
import os


def test_imports():
    print(sys.path)
    print(os.path.abspath('.'))
    assert os.path.exists(os.path.join(
        'nimble', 'migrations', 'm_0001_initial.py'
    ))
    import nimble.migrations.m_0001_initial
    import nimble.migrations.m_0002_profile_theme
    import nimble.migrations.m_0003_auto_20161127_0953
    import nimble.migrations.m_0004_auto_20161218_1303
    import nimble.migrations.m_0005_story_description
    assert dir(nimble.migrations.m_0001_initial)
    assert dir(nimble.migrations.m_0002_profile_theme)
    assert dir(nimble.migrations.m_0003_auto_20161127_0953)
    assert dir(nimble.migrations.m_0004_auto_20161218_1303)
    assert dir(nimble.migrations.m_0005_story_description)
    assert False
