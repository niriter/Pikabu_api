# Pikabu Api

Pikabu_api is unofficial API for [pikabu.ru]('https://pikabu.ru').


## Installation

Use the bash console to install Pikabu-api.

```bash
git clone https://github.com/niriter/Pikabu-api
```

## Usage
```python
import pikabu_api.main as pikabu_api

pikabu = pikabu_api.Pikabu_api()

#get user information
pikabu.get_user('https://pikabu.ru/@moderator') #return User object

#get post information
pikabu.get_post('https://pikabu.ru/story/podvodim_itogi_2019_goda_7138233') #return Post object

#get popular posts
pikabu.get_popular_posts() #return Feed object

#get best posts
pikabu.get_best_posts() #return Feed object

#get new posts
pikabu.get_new_posts() #return Feed object

#get most saved posts
pikabu.get_most_saved_posts() #return Feed object

#get most disputed posts
pikabu.get_disputed_posts() #return Feed object

# get communities feed
pikabu.get_communities_feed_posts() #return Feed object
```
---
### Objects
#### Feed

```python
feed = pikabu.get_best_posts() 

feed.get_url() #return feed Url

feed.get_name() #return feed name (or title)

feed.get_has_about() #return bool

feed.get_about() #return feed about if has about

feed.get_date() #return date of feed

feed.get_posts() #return Post objects
```

#### Post
```python
post = pikabu.get_post('https://pikabu.ru/story/podvodim_itogi_2019_goda_7138233')

post.get_title() #return Post title

post.get_content() #return Post solid text without blocks

post.get_content_html() #return Post html

post.get_content_blocks() #return Post content by blocks

post.get_media() #return links of media (Photos)

post.get_links() #return all links of other pages or sites (without links to images)

post.get_rating() #return Post rating (positive or negative)

post.get_post_id() #return Post id

post.get_username() #return Post creator nickname

post.get_user_url() #return Post creator url on pikabu

post.get_comments_count() #return Post number of comments

post.get_datetime() #return Post datetime

post.get_url() #return Post url

post.get_tags() #return dict of tags ("name" - name of tag; "url" - url of tag)

#The following functions are only available with get_post(url)

post.get_saves() #return number of saves; Is available only with get_post

post.get_shares() #return number of shares; Is available only with get_post

post.get_pluses() #return number of pluses; Is available only with get_post

post.get_minuses() #return number of minuses; Is available only with get_post

post.get_comments() #return Comment objects; Is available only with get_post
```

#### Comment
```python
comment = post.get_comments()[0]

comment.get_author_name() #return user nickname

comment.get_author_url() #return user url

comment.get_datetime() #return comment date and time

comment.get_link() #return link of comment

comment.get_rating() #return comment rating (positive or negative)

comment.get_formatted_text() #return comment text

comment.get_pluses() #return number of pluses

comment.get_minuses() #return number of minuses

comment.get_subcomments() #return child Comment objects

comment.get_comment_level() #return Comment level (Top - 0, First child - 1 etc.)
```

#### User
```python
user = pikabu.get_user('https://pikabu.ru/@moderator')

user.get_nickname() #return User name

user.get_url() #return link to User

user.get_about() #return User about or nothing

user.get_avatar() #return link to User avatar

user.get_reg_date() #return registration date and time

user.get_pluses() #return number of liked posts

user.get_minuses() #return number of disliked posts

user.get_edited_posts() #return number of edited posts

user.get_vote_edited_posts() #return number of votes to edit posts

user.get_communities() #return User communities ("title"; "url"; "img")

user.get_rating() #return User rating (can be "14 k" etc.)

user.get_subscribers() #return number of User subscribers

user.get_comments() #return number of User comments

user.get_posts_count() #return number of User posts

user.get_posts() #return Post objects

user.get_posts_in_hot() #return number of User posts in hot
```