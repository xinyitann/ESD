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
                :property_name= "properties.name"
                :estimated_cost= "properties.estimated_cost"
                :property_add= "properties.address"
                v-bind:key="properties"
                :property_image = "properties.image"
                :property_id = "properties.property_id"
                :auction_id = "properties.auction_id"
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
        agent_id:1
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
  },
  mounted() {
                // on Vue instance created, load the book list
                this.findproperties();
                
            },

}

</script>

<style>

</style>