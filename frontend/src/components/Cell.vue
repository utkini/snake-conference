<template>
  <div class="cell" :class="cellTypeClass">
    <div v-html="cellContent"></div>
  </div>
</template>

<script>
  import cellTypes from './../cell-types'

  export default {
    name: 'Cell',
    props: ['cell'],
    computed: {
      cellTypeClass() {
        if (this.cell === cellTypes.WALL) { return 'wall' }
        if (this.cell === cellTypes.APPLE) { return 'apple' }
        if (this.cell === cellTypes.PLAYER0) { return 'player0' }
        if (this.cell === cellTypes.PLAYER1) { return 'player1' }
        return ''
      },

      cellContent() {
        if (this.cell === cellTypes.APPLE) { return '<ion-icon name="logo-apple"></ion-icon>' }
        return ''
      }
    }
  }
</script>

<style lang="scss">
  @import "./../styles.scss";

  .cell {
    width: $cell-size;
    height: $cell-size;
    margin: 1px;
    background-color: white;
  }

  .wall {
    background-color: grey;
  }

  .apple {
    color: green;
    font-size: $cell-size;
    /*background-color: indianred;*/
  }

  .player0 {
    background-color: $player0-color;
  }

  .player1 {
    background-color: $player1-color;
  }
</style>