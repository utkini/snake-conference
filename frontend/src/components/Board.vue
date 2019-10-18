<template>
  <div class="board">
    <div class="board-wrapper">
      <row v-for="(row, index) in board" :row="row" :key="index"/>
    </div>
  </div>
</template>

<script>
  import Row from './Row'

  export default {
    name: 'Board',
    components: {Row},
    props: [
      'board'
    ],
    computed: {
      width() {
        return this.board[0].length
      },
      height() {
        return this.board.length
      },
    }

  }
</script>

<style>
  .board-wrapper {
    border: 2px solid grey;
    display: inline-block;
    line-height: 1.5;
    border-radius: .3rem;
  }
</style>
