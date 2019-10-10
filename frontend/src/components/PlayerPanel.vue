<template>
  <div class="player-panel">
    <div :class="['player-name', playerClass]">
      {{player.name}}
    </div>
  </div>
</template>

<script>
  export default {
    name: "PlayerPanel",
    props: ['player', 'playerIdx'],
    computed: {
      playerClass() {
        return this.playerIdx === 0 ? 'player0' : 'player1'
      }
    },
  }
</script>

<style scoped lang="scss">
  @import "./../styles.scss";

  .player-name {
    color: white;
    font-size: 36px;
    padding: 5px;
  }

  .player0 {
    background-color: $player0-color;
  }

  .player1 {
    background-color: $player1-color;
  }
</style>