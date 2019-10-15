<template>
  <div id="app">
    <games-list/>

    <h3>Active Game</h3>
    <button @click="play">
      <ion-icon name="play"></ion-icon>
    </button>
    <button @click="reset">
      <ion-icon name="refresh"></ion-icon>
    </button>

    <div style="display: flex; justify-content: space-around;">
      <player-panel :player="players[0]" :player-idx="0"/>

      <board :board="currentBoard"/>

      <player-panel :player="players[1]" :player-idx="1"/>
    </div>

    <h3>Manual JSON Upload</h3>
    <textarea v-model="input" cols="45" rows="10" style="margin-top: 10px;"></textarea>
    <button @click="submitGameLog">
      Submit
    </button>
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
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.APPLE, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
        ],
        [ //frame 1
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.APPLE, cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
        ],
        [ //frame 2
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.APPLE, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
        ],
        [ //frame 3
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
        ],
        [ //frame 4
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
        ],
        [ //frame 5
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.PLAYER1, cellTypes.PLAYER0, cellTypes.PLAYER0, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.PLAYER1, cellTypes.PLAYER1, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.EMPTY, cellTypes.WALL],
          [cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL, cellTypes.WALL],
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
        let timeout = 500
        this.currentFrame = 0

        let timer = setInterval(() => {
          console.log(`Displaying frame #${this.currentFrame}`)
          this.currentFrame += 1

          if (this.currentFrame + 1 >= this.boardLog.length) {
            console.log(`Finished. boardIdx: ${this.currentFrame}, boardLog length: ${this.boardLog.length}`)
            clearInterval(timer)
          }
        }, timeout)
      },

      reset() {
        this.currentFrame = 0
      },

      initFromGameLog(gameLog) {
        this.players = Object.values(gameLog.players)

        this.players[0].cellType = cellTypes.PLAYER0
        this.players[1].cellType = cellTypes.PLAYER1

        this.boardLog = []
        gameLog.steps.forEach((board, boardIdx) => {
          this.boardLog[boardIdx] = []

          board.forEach((row, rowIdx) => {
            this.boardLog[boardIdx][rowIdx] = []

            row.forEach((cell, cellIdx) => {
              let val = cellTypes.EMPTY
              switch (cell.state) {
                case 1:
                  val = this.players.filter(pl => pl.hash === cell.player)[0].cellType
                  break
                case 2:
                  val = cellTypes.APPLE
              }
              this.boardLog[boardIdx][rowIdx][cellIdx] = val
            })
          })
        })
        this.reset()
      },

      submitGameLog() {
        console.log(JSON.parse(this.input))
        this.initFromGameLog(JSON.parse(this.input))
      },
    }
  }
</script>

<style>
  #app {
    margin: 60px;
  }

  button {
    margin: 5px;
  }
</style>
