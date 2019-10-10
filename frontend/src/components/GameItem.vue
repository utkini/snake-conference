<template>
  <div>
    {{players[0].name}} VS {{players[1].name}}
  </div>
</template>

<script>
  export default {
    name: "GameItem",
    props: ['game'],
    computed: {
      players() {
        return Object.values(this.game.players)
      }
    },
  }
</script>

<style scoped>

</style>