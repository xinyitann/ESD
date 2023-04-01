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

  const get_all_URL = "http://localhost:5029/getbids";

  export default {
    name: "MyBidsPage",
    components: {
      PropertyCard,
    },
    
    data() {
      return {
        property_list: [],
        carouselNumCounter: 1
        
      };
    },
    methods: {
      carouselNum(){
        return this.carouselNumCounter + 1
      },
      findproperties() {
        var search_url = get_all_URL + "/" + this.search
      const response = fetch(search_url)
        .then((response) => response.json())
        .then((data) => {
          console.log(response);
            
          if (data.code === 404) {
            // no book in db
            this.message = data.message;
          } else {
            this.property_list = data.data.property_result.data.properties;
          }
          console.log(this.property_list)
        })
        .catch((error) => {
          // Errors when calling the service; such as network error,
          // service offline, etc
          console.log(this.message + error);
        });
    },
    },
  };
  </script>
  
  <style></style>
  