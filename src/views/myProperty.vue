<template>
    <div>
        <h2 class="text-center my-5">All Properties</h2>

        <div class="d-flex justify-content-end">
            <router-link to="/addlisting">
                <button class="btn mx-5" style="background-color: #447098; color: white;">Add Listing</button>
            </router-link>
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

        </div>
    </div>  
</template>

<script>
import PropertyCard from '@/components/propertyCard.vue';
const get_all_URL = "http://localhost:5001/property/agent";


export default {
name: 'MyPropertyPage',
    components: {
        PropertyCard
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
            
            if (data.code === 404) {
            // no book in db
            this.message = data.message;
            } else {
            this.property_result = data.data.property_result.data;
            console.log(this.property_result)

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