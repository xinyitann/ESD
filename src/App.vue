<template>
  <NavBar></NavBar>
  <router-view @passdata="GetData($event)" @agent_id="GetAgent($event)" :customer_id_prop='customer_id' :agent_id_prop='agent_id' :user_type="user_type"></router-view>
  <FooterComponent></FooterComponent>
  <button @click="check_id()"></button> 
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
      customer_id: 24,   //random initial variable for testing will get changed after logging in
      agent_id: 67,   //random initial variable for testing will get changed after logging in
      user_type: 'agent',   //random initial variable for testing will get changed after logging in
    }
  },
  methods: {
    GetData(data){
      this.customer_id = data
    },
    GetAgent(data){
      this.agent_id = data
    },
    check_id(){
      console.log(this.agent_id)
    }
  },
  created(){
    
  }
}
</script>

<style>

</style>
