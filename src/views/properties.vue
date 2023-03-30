<template>
  <div>
    <h2 class="text-center my-5">All Properties</h2>

    <!-- search bar-->
    <div class="row mb-4 w-100">
      <div class="col-10 col-sm-8 col-md-6 mx-auto">
        <div class="input-group mb-3" style="height: 45px">
          <input
            type="text"
            class="form-control"
            placeholder="Search by neighbourhood or postal code"
            aria-label="Search by neighbourhood or postal code"
            v-model="search" 
            aria-describedby="button-addon"
          />
          <button
            class="btn btn-outline-secondary"
            type="button"
            id="button-addon"
            @click="findproperties"
          >
            <i class="bi bi-search"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="container-fluid row">
      <!-- need the index to differentiate carousel to make it work-->
      <!-- this is the rough idea using a for loop -->
      <!-- <div v-for="(listing, index) in listings" :key="index">
                <PropertyCard :carouselNum="index+1" ></PropertyCard>
            </div> -->

      <!-- for testing-->
      
        <PropertyCard v-for="properties in property_list"
          :carouselNum="1"
          :property_name= "properties.name"
          :estimated_cost= "properties.estimated_cost"
          :property_add= "properties.address"
          v-bind:key="properties"
          


        ></PropertyCard>
    

      <!-- <PropertyCard :carouselNum="2"></PropertyCard> -->
    </div>
  </div>
</template>

<script>
import PropertyCard from "@/components/propertyCard.vue";

const get_all_URL = "http://localhost:5106/search_list";

export default {
  name: "PropertiesPage",
  components: {
    PropertyCard,
  },
  data() {
    return {
      property_list: [],
      message: "",
      search: ""
    };
  },
  methods: {
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
