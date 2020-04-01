import pytest
from main import Pikabu_api
from classes.Post import Post

main = Pikabu_api()
post = main.get_post('https://pikabu.ru/story/podvodim_itogi_2019_goda_7138233')

def test_class():
    global post
    assert isinstance(post, Post)

def test_title():
    global post
    assert post.get_title()

def test_content():
    global post
    assert post.get_content()

def test_content_html():
    global post
    assert post.get_content_html()

def test_content_blocks():
    global post
    assert post.get_content_blocks()

def test_media():
    global post
    assert post.get_media()

def test_links():
    global post
    assert post.get_links()

def test_rating():
    global post
    assert post.get_rating()

def test_pluses():
    global post
    assert post.get_pluses()

def test_minuses():
    global post
    assert post.get_minuses()

def test_post_id():
    global post
    assert post.get_post_id()

def test_username():
    global post
    assert post.get_username()

def test_user_url():
    global post
    assert post.get_user_url()

def test_comments_count():
    global post
    assert post.get_comments_count()

def test_save():
    global post
    assert post.get_saves()

def test_share():
    global post
    assert post.get_shares()

def test_datetime():
    global post
    assert post.get_datetime()

def test_url():
    global post
    assert post.get_url()

def test_tags():
    global post
    assert post.get_tags()

def test_comments():
    global post
    assert post.get_comments()

