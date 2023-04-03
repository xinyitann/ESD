<template>
  <NavBar :user_type="user_type"></NavBar>
  <router-view @set_user_type="GetUserType($event)" @submit_property_data="GetPropertyData($event)" @passdata="GetData($event)" @agent_id="GetAgent($event)" :customer_id_prop='customer_id' :agent_id_prop='agent_id' :user_type="user_type" :property_id_prop="property_id"></router-view>
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
      customer_id: '',   //random initial variable for testing will get changed after logging in
      agent_id: '',   //random initial variable for testing will get changed after logging in
      user_type: '',   //random initial variable for testing will get changed after logging in
      property_id: ''
    }
  },
  methods: {
    GetData(data){
      this.agent_id = data
      this.customer_id = data
    },
    GetAgent(data){
      this.agent_id = data
    },
    handlePropertyClicked(propertyId) {
      this.property_id = propertyId;
    },
    GetPropertyData(data){
      this.property_id = data
    },
    GetUserType(data){
      this.user_type = data
    },
  },
  created(){
    
  }
}
</script>

<style>

</style>


