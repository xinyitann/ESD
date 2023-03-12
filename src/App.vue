<template>
  <NavBar></NavBar>
  <router-view></router-view>
</template>

<script>
import NavBar from "./components/navbar.vue"

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>

</style>
