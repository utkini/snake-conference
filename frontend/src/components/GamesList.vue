<template>
    <div class="games-list-panel">
        <div class="container-fluid" style="padding-left: 3px">
            <div class="row">
                <div class="col">
                    <h3>Games List</h3>
                </div>
                <div class="col-6">
                    <button @click="refresh" type="button" class="btn btn-light">
                        <ion-icon name="refresh"></ion-icon>
                    </button>
                </div>
            </div>
        </div>
        <div class="games-list" data-spy="scroll" data-offset="0">
            <game-item v-for="(game, idx) in gamesList"
                     :game="game" :key="idx"
                     @click.native="selectGame(game)"
                     :class="[
                        {'selected': game.game_log_id === selectedGameId },
                        'game-item'
                     ]"
            />
        </div>

    </div>
</template>

<script>
  import {mapState, mapActions, mapMutations} from 'vuex'

  import GameItem from './GameItem'

  export default {
    name: "GamesList",
    components: {
      GameItem
    },
    computed: {
      ...mapState('game', [
        'gamesList',
        'selectedGameId',
        'selectedGame'
      ])
    },
    methods: {
      ...mapActions('game', [
        'refreshGamesList',
        'getGame'
      ]),
      refresh() {
        this.refreshGamesList()
      },
      selectGame(game) {
        this.getGame(game.game_log_id)
      }
    },
    created() {
      this.refresh()
    }
  }
</script>

<style scoped lang="scss">
  .games-list {
    padding: 5px;

  }

  .game-item {
    cursor: pointer;

    &:hover{
      background: lightgray;
    }
  }

  .game-item.selected {
    font-weight: bold;
  }
</style>
