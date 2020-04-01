import pytest
from main import Pikabu_api
from classes.Feed import Feed

def test_popular_feed():
    main = Pikabu_api()
    feed = main.get_popular_posts()
    global feed
    assert feed

def test_class():
    global feed
    assert isinstance(feed, Feed)

def test_url():
    global feed
    assert feed.get_url()

def test_name():
    global feed
    assert feed.get_name()

def test_posts_count():
    global feed
    assert feed.posts_count()

def test_posts_len_count():
    global feed
    assert feed.posts_count() == len(feed)

def test_about():
    global feed
    if feed.has_about():
        assert feed.get_about()
    else:
        assert True

def test_feed_date():
    global feed
    assert feed.get_date()

