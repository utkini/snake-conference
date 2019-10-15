<template>
  <div class="row">
    <cell v-for="(cell, index) in row" :cell=cell :key="index"></cell>
  </div>
</template>

<script>
  import Cell from './Cell'

  export default {
    name: "Row",
    components: {Cell},
    props: ['row'],
  }
</script>

<style scoped>
  .row {
    display: flex;
    margin-left: 0;
    margin-right: 0;
  }
</style>
