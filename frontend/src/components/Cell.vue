<template>
  <div class="cell" :class="cellTypeClass">
    <div v-html="cellContent"></div>
  </div>
</template>

<script>
  import cellTypes from './../cell-types'
  import "./../styles.scss"

  export default {
    name: 'Cell',
    props: ['cell'],
    data() {
        return {
            images: {
                apple: require('../assets/apple.png')
            }
        }
    },
    computed: {
      cellTypeClass() {
        if (this.cell === cellTypes.WALL) { return 'bg-dark' }
        if (this.cell === cellTypes.APPLE) { return 'apple' }
        if (this.cell === cellTypes.PLAYER0) { return 'bg-primary'}
        if (this.cell === cellTypes.PLAYER1) { return 'bg-success' }
        return ''
      },
      cellContent() {
          // eslint-disable-next-line no-console,no-undef
          console.log('heh');
        if (this.cell === cellTypes.APPLE) { return '<img class="apple" src=' + this.images.apple + '>' }
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
  }

  .wall {
    background-color: grey;
  }

  .apple {
    width: $cell-size;
    height: $cell-size;
    color: green;
    /*background-color: indianred;*/
  }

  .player0 {
    background-color: $player0-color;
  }

  .player1 {
    background-color: $player1-color;
  }
</style>
