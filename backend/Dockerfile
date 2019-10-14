# Sample usage:
# cp game_players/sample_player.py game_players/player_1.py
# docker build . -t snake
# docker run --rm -v %cd%/.game_log:/tmp/.game_log/ -v %cd%/game_players:/tmp/players/ snake
FROM python:3.7-alpine

ENV SRC_GAME_PLAYERS_DIR="/tmp/players"
ENV GAME_PLAYERS_DIR="game_players"
ENV GAME_PLAYERS_DIR_NAME="game_players"
ENV GAME_LOG_DIR="/tmp/.game_log"

# Install virtualenv
RUN pip install virtualenv

# Add user
RUN adduser -D user
WORKDIR /home/user

# Create virtualenv
RUN python3 -m virtualenv --python=/usr/local/bin/python3 ./venv

# Install dependencies:
COPY requirements.txt .
RUN . ./venv/bin/activate && pip install -r requirements.txt

# Copy project files
COPY game game
COPY sample_run.py sample_run.py
COPY settings.py settings.py
COPY game_players ${GAME_PLAYERS_DIR_NAME}

RUN chown -R user /home/user
USER user

CMD . ./venv/bin/activate && cp ${SRC_GAME_PLAYERS_DIR}/player_*.py ${GAME_PLAYERS_DIR_NAME} && exec python sample_run.py
