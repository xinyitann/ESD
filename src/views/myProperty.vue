<template>
    <div>
        <h2 class="text-center my-5">All Properties</h2>

        <div class="d-flex justify-content-end">
            <router-link to="/editlisting">
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
            <PropertyCard :carouselNum="1"></PropertyCard>
            <PropertyCard :carouselNum="2"></PropertyCard>
        </div>
    </div>  
</template>

<script>
import PropertyCard from '@/components/propertyCard.vue';

export default {
name: 'MyPropertyPage',
    components: {
        PropertyCard
    },
}

</script>

<style>

</style>