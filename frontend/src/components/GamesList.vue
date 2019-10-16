<template>
  <div class="games-list-panel">
    <h3>Games List</h3>
    <button @click="refresh">
      <ion-icon name="refresh"></ion-icon>
    </button>

    <div class="games-list">
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
    border: black 1px solid;
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
