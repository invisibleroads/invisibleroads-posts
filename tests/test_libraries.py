from invisibleroads_posts.libraries.text import render_title


def test_render_title():
    assert 'Abc Xyz' == render_title('/abc-xyz/')
