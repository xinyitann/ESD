<template>
    <div>
        <h2 class="text-center my-5">My Properties</h2>

        <div class="d-flex justify-content-end">
            <router-link to="/addlisting">
                <button class="btn mx-5" style="background-color: #447098; color: white;">Add Listing</button>
            </router-link>
        </div>
        
        <div class="container-fluid row">

            <MyPropertyCard v-for="properties in property_list"
                :carouselNum="1"
                :key="properties"
                :property_name= "properties.name"
                :property_add= "properties.address"
                :property_postal_code = "properties.postalcode"
                :property_type = "properties.property_type"
                :property_square_feet="properties.square_feet"
                :property_room = "properties.room"
                :property_facing = "properties.facing"
                :property_build_year = "properties.build_year"
                :property_estimated_cost = "properties.estimated_cost"
                :property_neighbourhood = "properties.neighbourhood"
                :property_image = "properties.image"
                :property_id = "properties.property_id"
                :auction_id = "properties.auction_id"
                :property_agent_id = "properties.agent_id"
                :property_customer_id = "properties.customer_id"
            ></MyPropertyCard>

        </div>
    </div>  
</template>

<script>
import MyPropertyCard from '../components/MyPropertyCard.vue';

const get_all_URL = "http://localhost:5001/property/agent";


export default {
name: 'MyPropertyPage',
    components: {
        MyPropertyCard
    },
    data() {
    return {
        property_list: [],
        message: "",
        search: "",
        agent_id:this.agent_id_prop
    };
},

  methods: {
    findproperties() {
        console.log("here")
        // this.property_id={{}}
        // console.log(this.property_id)
        var search_url = get_all_URL + '/'+ this.agent_id
        console.log(search_url)
        const response = fetch(search_url)
        .then((response) => response.json())
        .then((data) => {
            console.log(response);
            console.log(data)
            
            if (data.code === 404) {
            // no book in db
            this.message = data.message;
            } else {
            this.property_list = data.data;
            console.log("property_list", this.property_list)
            }
            
        })
        .catch((error) => {
            // Errors when calling the service; such as network error,
            // service offline, etc
            console.log("error")
            console.log(this.message + error);
        });
    },
    get_submit_data(data){
          this.selected_property_id = data
    }
  },
  mounted() {
                // on Vue instance created, load the book list
                this.findproperties();
                
            },
    watch: {
    // whenever question changes, this function will run
    selected_property_id(new_id) {
      this.$emit('submit_property_data', new_id)
      console.log('new_id'+new_id)

    }
  },
  props:[
    'agent_id_prop',
  ],

}

</script>

<style>

</style>