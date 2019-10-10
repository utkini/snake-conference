<template>
  <div class="games-list-panel">
    <h3>Games List</h3>
    <button @click="refresh">
      <ion-icon name="refresh"></ion-icon>
    </button>

    <div class="games-list">
      <game-item v-for="(game, idx) in gamesList"
                 :game="game" :key="idx"
                 @click.native="setSelectedGameId(idx)"
                 :class="[
                    {'selected': idx === selectedGameId },
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
        'selectedGameId'
      ])
    },
    methods: {
      ...mapActions('game', [
        'refreshGamesList'
      ]),
      ...mapMutations('game', [
        'setSelectedGameId'
      ]),
      refresh() {
        this.refreshGamesList()
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