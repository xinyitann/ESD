<template>
  <NavBar></NavBar>
  <router-view @passdata="GetData($event)" @agent_id="GetAgent($event)" :customer_id_prop='customer_id' :agent_id_prop='agent_id' :user_type="user_type" :property_id_prop="property_id"></router-view>
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
  },
  data(){
    return {
      customer_id: 2,   //random initial variable for testing will get changed after logging in
      agent_id: 1,   //random initial variable for testing will get changed after logging in
      user_type: 'agent',   //random initial variable for testing will get changed after logging in
      property_id: 6
    }
  },
  methods: {
    GetData(data){
      this.agent_id = data
    },
    GetAgent(data){
      this.agent_id = data
    },
  },
  created(){
    
  }
}
</script>

<style>

</style>

