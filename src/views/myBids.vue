<template>
    <div>
      <h2 class="text-center my-5">My Bids</h2>

  
      <div class="container-fluid row">
        <!-- need the index to differentiate carousel to make it work-->
        <!-- this is the rough idea using a for loop -->
        <!-- <div v-for="(listing, index) in listings" :key="index">
                  <PropertyCard :carouselNum="index+1" ></PropertyCard>
              </div> -->
  
        <!-- for testing-->
        
          <PropertyCard v-for="properties in property_list"
            :carouselNum="carouselNum"
            :property_name= "properties.name"
            :estimated_cost= "properties.estimated_cost" 
            :property_add= "properties.address"
            :key="properties"
          ></PropertyCard>
  
        <!-- <PropertyCard :carouselNum="2"></PropertyCard> -->
      </div>
    </div>
  </template>
  
  <script>
  import PropertyCard from "@/components/propertyCard.vue";

  export default {
    name: "MyBidsPage",
    components: {
      PropertyCard,
    },
    
    data() {
      return {
        property_list: [],
        message: "",
        search: "",
        carouselNumCounter: 1
        
      };
    },
    methods: {
      carouselNum(){
        return this.carouselNumCounter + 1
      }
    },
  };
  </script>
  
  <style></style>
  