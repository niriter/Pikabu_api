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
pikabu.get_user('https://pikabu.ru/@moderator')

#get post information
pikabu.get_post('https://pikabu.ru/story/podvodim_itogi_2019_goda_7138233')

#get popular posts
pikabu.get_popular_posts()

#get best posts
pikabu.get_best_posts()

#get new posts
pikabu.get_new_posts()

#get most saved posts
pikabu.get_most_saved_posts()

#get most disputed posts
pikabu.get_disputed_posts()

# get communities feed
pikabu.get_communities_feed_posts()
```
---

##### TODO:
- Добавить награды пользователя