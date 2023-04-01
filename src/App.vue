<template>
  <NavBar :user_type="user_type"></NavBar>
  <router-view @passdata="GetData($event)" @agent_id="GetAgent($event)" :customer_id_prop='customer_id' :agent_id_prop='agent_id' :user_type="user_type" :property_id_prop="property_id"></router-view>
    <PropertyCard></PropertyCard>
  <FooterComponent></FooterComponent>
  
</template>

<script>
import NavBar from "./components/navbar.vue"
import FooterComponent from "./components/footer.vue"
import PropertyCard from "./components/propertyCard.vue"

export default {
  name: 'App',
  components: {
    NavBar,
    FooterComponent,
    PropertyCard,
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
    handlePropertyClicked(propertyId) {
      this.property_id = propertyId;
    }
  },
  created(){
    
  }
}
</script>

<style>

</style>

