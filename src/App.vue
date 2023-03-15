<template>
  <NavBar></NavBar>
  <router-view></router-view>
  <FooterComponent></FooterComponent>
</template>

<script>
import NavBar from "./components/navbar.vue"
import FooterComponent from "./components/footer.vue"

export default {
  name: 'App',
  components: {
    NavBar,
    FooterComponent,
  }
}
</script>

<style>

</style>
