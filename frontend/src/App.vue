<template>
    <div id="app">
        <div class="container-fluid">
            <div class="row">
                <div class="col-3 player_view">
                    <games-list/>
                </div>
                <div class="col player_view">
                    <div class="container">
                        <div class="row">
                            <div class="col-4">
                                <h3>Active Game</h3>
                            </div>
                            <div class="col" >
                                <button @click="play" type="button" class="btn btn-light">
                                    <ion-icon name="play"></ion-icon>
                                </button>
                                <button @click="reset" type="button" class="btn btn-light">
                                    <ion-icon name="refresh"></ion-icon>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-around;" class="col">
                        <player-panel :player="players[0]" :player-idx="0"/>
                        <board :board="currentBoard"/>
                        <player-panel :player="players[1]" :player-idx="1"/>
                    </div>
                </div>
            </div>
        </div>

      <div class="card blocks">
            <button class="btn btn-light" data-toggle="collapse" data-target="#collapseForm" aria-expanded="false"
                    aria-controls="collapseForm" >
                <h3>Manual JSON Upload</h3>
            </button>
      </div>
<div class="collapse" id="collapseForm" >
                <div class="card card-body" style="margin: 0 1%">
                    <textarea v-model="input" class="form-control" id="exampleFormControlTextarea1" rows="7"></textarea>

                <button @click="submitGameLog" type="button" class="btn btn-light btn-lg">
                    Submit
                </button>
            </div>
    </div>
</div>

</template>

<script>
  import { mapGetters, mapState } from 'vuex'

  import Board from './components/Board'
  import GamesList from './components/GamesList'
  import cellTypes from './cell-types'
  import PlayerPanel from './components/PlayerPanel'

  export default {
    name: 'app',
    components: {
      Board,
      GamesList,
      PlayerPanel
    },
    data() { return {
      input: null,
      boardLog: [
        [ //frame 0
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.APPLE, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
        ],
        [ //frame 1
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.APPLE, cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
        ],
        [ //frame 2
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.APPLE, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
        ],
        [ //frame 3
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
        ],
        [ //frame 4
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
        ],
        [ //frame 5
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
          [cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY],
        ],
      ],
      players: [
        {"hash": "f6f4061a1bddc1c04d8109b39f581270", "name": "test0"},
        {"hash": "5a105e8b9d40e1329780d62ea2265d8a", "name": "test1"}
      ],
      currentFrame: 0,
    }},
    computed: {
      ...mapState('game', [
        'selectedGame',
      ]),
      ...mapGetters('game', [
        'selectedPlayers'
      ]),

      currentBoard() {
        return this.boardLog[this.currentFrame]
      },
    },
    created() {
      this.reset()
    },

    watch: {
      selectedGame() {
        this.initFromGameLog(this.selectedGame)
      }
    },

    methods: {
      play() {
        let timeout = 500;
        this.currentFrame = 0;

        let timer = setInterval(() => {
          console.log(`Displaying frame #${this.currentFrame}`);
          this.currentFrame += 1;

          if (this.currentFrame + 1 >= this.boardLog.length) {
            console.log(`Finished. boardIdx: ${this.currentFrame}, boardLog length: ${this.boardLog.length}`);
            clearInterval(timer)
          }
        }, timeout)
      },

      reset() {
        this.currentFrame = 0
      },

      initFromGameLog(gameLog) {
        this.players = Object.values(gameLog.players);

        this.players[0].cellType = cellTypes.PLAYER0;
        this.players[1].cellType = cellTypes.PLAYER1;

        this.boardLog = [];
        gameLog.steps.forEach((board, boardIdx) => {
          this.boardLog[boardIdx] = [];

          board.forEach((row, rowIdx) => {
            this.boardLog[boardIdx][rowIdx] = [];

            row.forEach((cell, cellIdx) => {
              let val = cellTypes.EMPTY;
              switch (cell.state) {
                case 1:
                  val = this.players.filter(pl => pl.hash === cell.player)[0].cellType;
                  break;
                case 2:
                  val = cellTypes.APPLE
              }
              this.boardLog[boardIdx][rowIdx][cellIdx] = val
            })
          })
        });
        this.reset()
      },

      submitGameLog() {
        console.log(JSON.parse(this.input));
        this.initFromGameLog(JSON.parse(this.input))
      },
    }
  }
</script>

<style>
    #app {
        margin: 3%;
        background: #e6ecf0;
    }

    .player_view {
        background: white;
        padding: 5px;
        margin: 0 1%
    }

    .blocks {
        margin: 0 1%;
        margin-top: 0.5%;
    }
    button {
      margin: 10px;
    }
</style>
