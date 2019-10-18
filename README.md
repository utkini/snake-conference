# snake-conference

### How to setup dev environment

> Paths are specified relatively from project root

**Backend**

1. `pip install -r ./backend`
1. Create a directory `./backend/.game_log` (can be changed by `GAME_LOG_DIR_NAME` in ./backend/settings.py)
1. `python ./backend/app.py`

**Froneend**

1. `cd ./frontend`
1. `npm i`
1. Change the `API_URL` setting in `./frontend/src/config.js` to `'http://localhost:5000'` (or another URL that app.py runs on)
1. `npm run serve`

The application is available by address printed by `npm run serve`. Usually, it is http://localhost:8080.


### How to play

1. Put players' `player_*.py` files into `./backend/game_players` or create your own ones. You may use `./backend/game_players/sample_player.py` as a basic example. 
    - **Make sure players' files are named according to the following mask: `player_*.py`**
    - **Make sure to always have exactly 2 player in `./backend/game_players`**
1. `python ./backend/sample_run.py` to play a new game with the players in `./backend/game_players`
1. Open the application in your browser and refresh the games list. The new game should appear in the list.


To play once again, just run `python ./backend/sample_run.py` again. 
To play with other players, put them into `./backend/game_players` instead of the old ones.
