<template>
  <div style="min-height: 100vh">
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

    <div v-if="search!=''">
      <div v-if="search==530321" class="container-fluid row">
      <!-- need the index to differentiate carousel to make it work-->
      <!-- this is the rough idea using a for loop -->
      <!-- <div v-for="(listing, index) in listings" :key="index">
                <PropertyCard :carouselNum="index+1" ></PropertyCard>
            </div> -->

      <!-- for testing-->
      
        <PropertyCard v-for="properties in PO_property_list"
          :carouselNum="1"
          :property_name= "properties.name"
          :estimated_cost= "properties.estimated_cost"
          :property_add= "properties.address"
          :property_id_card="properties.property_id"
          :property_image="properties.image"
          v-bind:key="properties"
          @submit_property_data="get_submit_data($event)"
        ></PropertyCard>

        <!-- <PropertyDetails v-for="properties in property_list"
          :property_id="properties.id"
          v-bind:key="properties"


        ></PropertyDetails> -->
    

      <!-- <PropertyCard :carouselNum="2"></PropertyCard> -->
    </div>
    <div v-else class="container-fluid row">
      <!-- need the index to differentiate carousel to make it work-->
      <!-- this is the rough idea using a for loop -->
      <!-- <div v-for="(listing, index) in listings" :key="index">
                <PropertyCard :carouselNum="index+1" ></PropertyCard>
            </div> -->

      <!-- for testing-->
      
        <PropertyCard v-for="properties in ELSE_property_list"
          :carouselNum="1"
          :property_name= "properties.name"
          :estimated_cost= "properties.estimated_cost"
          :property_add= "properties.address"
          :property_id_card="properties.property_id"
          :property_image="properties.image"
          v-bind:key="properties"
          @submit_property_data="get_submit_data($event)"
        ></PropertyCard>

        <!-- <PropertyDetails v-for="properties in property_list"
          :property_id="properties.id"
          v-bind:key="properties"


        ></PropertyDetails> -->
    

      <!-- <PropertyCard :carouselNum="2"></PropertyCard> -->
    </div>
    </div>

  </div>
</template>

<script>
import PropertyCard from "@/components/propertyCard.vue";
// import PropertyDetails from "./propertyDetails.vue"

// const get_all_URL = "http://localhost:5106/search_list";

export default {
  name: "PropertiesPage",
  components: {
    PropertyCard,
    // PropertyDetails
  },
  
  data() {
    return {
      PO_property_list : [{"address": "Clementi street 1", "agent_id": 6, "auction_id": 6, "build_year": 2008, "customer_id": 6, "estimated_cost": 13500000.0, "facing": "north", "image": "room6.jpg", "name": "Condominium in Clementi", "neighbourhood": "Clementi", "postalcode": 530321, "property_id": 6, "property_type": "Condominium", "room": 3, "square_feet": 1087}, {"address": "Jurong west street 41", "agent_id": 3, "auction_id": 3, "build_year": 2010, "customer_id": 3, "estimated_cost": 14250000.0, "facing": "east", "image": "room3.jpg", "name": "Condominium in Jurong", "neighbourhood": "Jurong", "postalcode": 530323, "property_id": 3, "property_type": "Condominium", "room": 3, "square_feet": 1281}, {"address": "Ridout Road", "agent_id": 9, "auction_id": 9, "build_year": 1990, "customer_id": 9, "estimated_cost": 20000000.0, "facing": "east", "image": "room9.jpg", "name": "Good Class Bungalow", "neighbourhood": "Tanglin", "postalcode": 530325, "property_id": 9, "property_type": "Detached House", "room": 6, "square_feet": 10000}, {"address": "Grange Road", "agent_id": 7, "auction_id": 7, "build_year": 2015, "customer_id": 7, "estimated_cost": 4500000.0, "facing": "west", "image": "room7.jpg", "name": "Luxury Condo", "neighbourhood": "Orchard", "postalcode": 530320, "property_id": 7, "property_type": "Condominium", "room": 4, "square_feet": 2000}, {"address": "waterfront street 17", "agent_id": 1, "auction_id": 1, "build_year": 2011, "customer_id": 1, "estimated_cost": 13150000.0, "facing": "north", "image": "room1.jpg", "name": "Waterfront condominium", "neighbourhood": "Bishan", "postalcode": 530324, "property_id": 1, "property_type": "Condominium", "room": 4, "square_feet": 5929}, {"address": "Punggol field street 2", "agent_id": 2, "auction_id": 2, "build_year": 2005, "customer_id": 2, "estimated_cost": 27000000.0, "facing": "south", "image": "room2.jpg", "name": "HDB flat in Punggol", "neighbourhood": "Punggol", "postalcode": 530322, "property_id": 2, "property_type": "HDB", "room": 3, "square_feet": 1076}, {"address": "Sentosa cove street 1", "agent_id": 4, "auction_id": 4, "build_year": 2015, "customer_id": 4, "estimated_cost": 36500000.0, "facing": "south", "image": "room4.jpg", "name": "Luxury house in Sentosa Cove", "neighbourhood": "Sentosa", "postalcode": 530322, "property_id": 4, "property_type": "Landed", "room": 5, "square_feet": 7500}, {"address": "Punggol field street 2", "agent_id": 2, "auction_id": 2, "build_year": 2005, "customer_id": 2, "estimated_cost": 27000000.0, "facing": "south", "image": "room2.jpg", "name": "HDB flat in Punggol", "neighbourhood": "Punggol", "postalcode": 530322, "property_id": 2, "property_type": "HDB", "room": 3, "square_feet": 1076}, {"address": "Sentosa cove street 1", "agent_id": 4, "auction_id": 4, "build_year": 2015, "customer_id": 4, "estimated_cost": 36500000.0, "facing": "south", "image": "room4.jpg", "name": "Luxury house in Sentosa Cove", "neighbourhood": "Sentosa", "postalcode": 530322, "property_id": 4, "property_type": "Landed", "room": 5, "square_feet": 7500}, {"address": "Tampines Street 45", "agent_id": 8, "auction_id": 8, "build_year": 2000, "customer_id": 8, "estimated_cost": 450000.0, "facing": "north", "image": "room8.jpg", "name": "Spacious HDB", "neighbourhood": "Tampines", "postalcode": 530332, "property_id": 8, "property_type": "HDB", "room": 3, "square_feet": 1000}],
      ELSE_property_list: [
                    {
                        "address": "waterfront street 17",
                        "agent_id": 1,
                        "auction_id": 1,
                        "build_year": 2011,
                        "customer_id": 1,
                        "estimated_cost": 13150000.0,
                        "facing": "north",
                        "image": "room1.jpg",
                        "name": "Waterfront condominium",
                        "neighbourhood": "Bishan",
                        "postalcode": 530324,
                        "property_id": 1,
                        "property_type": "Condominium",
                        "room": 4,
                        "square_feet": 5929
                    },
                ],
      property_list: [],
      message: "",
      search: "",
      selected_property_id: '',
    };
  },
  methods: {
    // findproperties() {
    //     var search_url = get_all_URL + "/" + this.search
    //   const response = fetch(search_url)
    //     .then((response) => response.json())
    //     .then((data) => {
    //       console.log(response);
            
    //       if (data.code === 404) {
    //         // no book in db
    //         this.message = data.message;
    //       } else {
    //         this.property_list = data.data.property_result.data.properties;
    //       }
    //       console.log(this.property_list)
    //     })
    //     .catch((error) => {
    //       // Errors when calling the service; such as network error,
    //       // service offline, etc
    //       console.log(this.message + error);
    //     });
    // },
    get_submit_data(data){
          this.selected_property_id = data
    }

  },
  
  watch: {
    // whenever question changes, this function will run
    selected_property_id(new_id) {
      this.$emit('submit_property_data', new_id)
      console.log('new_id'+new_id)

    }
  },

};
</script>

<style></style>

