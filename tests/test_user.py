import pytest
from main import Pikabu_api
from classes.User import User

main = Pikabu_api()
user = main.get_user('https://pikabu.ru/@admin')

def test_class():
    global user
    assert isinstance(user, User)

def test_nickname():
    global user
    assert user.get_nickname()

def test_url():
    global user
    assert user.get_url()

# def test_about():
#     global user
#     assert user.get_about()

def test_avatar():
    global user
    assert user.get_avatar()

def test_reg_date():
    global user
    assert user.get_reg_date()

def test_pluses():
    global user
    assert user.get_pluses()

def test_minuses():
    global user
    assert user.get_minuses()

def test_edited_posts():
    global user
    assert user.get_edited_posts()

def test_vote_edited_posts():
    global user
    assert user.get_vote_edited_posts()

def test_communities():
    global user
    assert user.get_communities()

def test_rating():
    global user
    assert user.get_rating()

def test_subscribers():
    global user
    assert user.get_subscribers()

def test_comments():
    global user
    assert user.get_comments()

def test_posts_count():
    global user
    assert user.get_posts_count()

def test_posts():
    global user
    assert user.get_posts()

def test_posts_in_hot():
    global user
    assert user.get_posts_in_hot()