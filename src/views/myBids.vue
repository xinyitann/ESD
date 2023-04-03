<template>
    <div style="min-height: 100vh">
      <h2 class="text-center my-5">My Bids</h2>

      <!-- carouselNum to delete, update bids and make carousel work-->
      <div v-if="bidBefore" class="container-fluid row">
        <BidPropertyCard v-for="(property,index) in property_list"
          :index="index"
          :bid="bid_list[index]"
          :property_name= "property.name"
          :estimated_cost= "property.estimated_cost" 
          :property_add= "property.address"
          :property_image="property.image"
          :key="property"
        ></BidPropertyCard>
      </div>
      

      <div v-else class="mx-5">
        <p class="text-center display-6">You have not made a bid yet.</p>
        <div class="d-flex justify-content-center my-5">
          <router-link to="/properties">
            <button type="button" class="btn mx-4" style="background-color: #447098; color: white;">Discover Properties Now</button>
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import BidPropertyCard from "@/components/bidPropertyCard.vue";

  export default {
    name: "MyBidsPage",
    components: {
      BidPropertyCard,
    },
    props: [
        'customer_id_prop',
        'agent_id_prop',
        'user_type',
    ],
    data() {
      return {
        property_list: [],
        carouselNumCounter: 0,
        bid_list: null,
        bidBefore: false,
        id: 0,
      };
    },
    async created(){
      console.log(this.agent_id_prop)
      console.log(this.user_type)

      if (this.user_type == "user"){
        this.id = this.customer_id_prop
      }
      else{
        this.id = this.agent_id_prop
      }

      try {
        var get_property_url = "http://localhost:5029/getbids/" + String(this.id);
        var response = await fetch(get_property_url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        var data = await response.json();
        this.bidBefore = true;
        this.property_list = Reflect.get(data['data'], 'property_result');
        this.bid_list = Reflect.get(data['data'], 'bids_result');

      } catch (error) {
        console.error(error);
      }
    }
  };
  </script>
  
  <style></style>
  