<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
                <h2 class="text-center my-5">Add Listing</h2>
                <form id="my-form">
                    <div class="row">
                        <div class="col-12 col-md-6 px-5">
                            <div class="mb-3">
                                <label for="customerid" class="form-label">Customer ID*</label>
                                <input v-model="customer_id" type="text" class="form-control" id="customerid">
                            </div>
                            <div class="mb-3">
                                <label for="address" class="form-label">Address*</label>
                                <input v-model="address" type="text" class="form-control" id="address">
                            </div>
                            <div class="mb-3">
                                <label for="name" class="form-label">Name*</label>
                                <input v-model="name" type="text" class="form-control" id="name">
                            </div>
                            <div class="mb-3">
                                <label for="neighbourhood" class="form-label">neighbourhood</label>
                                <input v-model="neighbourhood" type="text" class="form-control" id="neighbourhood">
                            </div>
                            <div class="mb-3">
                                <label for="PostalCode" class="form-label">Postal Code*</label>
                                <input v-model="postalcode" type="text" class="form-control" id="PostalCode">
                            </div>
                            <div class="mb-3">
                                <label for="build_year" class="form-label">Build Year*</label>
                                <input v-mode="build_year" type="text" class="form-control" id="build_year">
                            </div>
                            <div class="mb-3">
                                <label for="sqaure_feet" class="form-label">Size in Square Feet*</label>
                                <input v-model="square_feet" type="text" class="form-control" id="square_feet">
                            </div>
                            <div class="mb-3">
                                <label for="room" class="form-label">Number of Rooms*</label>
                                <input v-model="room" type="number" class="form-control" id="room">
                            </div>
                        </div>
                        <div class="col-12 col-md-6 px-5">
                            <div class="mb-3">
                                <label for="estimatedCost" class="form-label">Property Type</label>
                                <input v-model="property_type" type="text" class="form-control" id="estimatedCost">
                            </div>
                            <div class="mb-3">
                                <label for="facing" class="form-label">Facing</label>
                                <input v-model="facing" type="text" class="form-control" id="facing">
                            </div>
                            <div class="mb-3">
                                <label for="estimatedCost" class="form-label">Estimated Cost*</label>
                                <input type="text" class="form-control" id="estimatedCost">
                            </div>
                            <div class="mb-3">
                                <label for="optionFee" class="form-label">Option Fee*</label>
                                <input v-model="option_fee" type="text" class="form-control" id="optionFee">
                            </div>
                            <div class="mb-3">
                                <label for="starting_price" class="form-label">Minimum Bid Amount*</label>
                                <input v-model="starting_price" type="starting_price" class="form-control" id="starting_price">
                            </div>
                            <div class="mb-3">
                                <label for="startBidDate" class="form-label">Bidding Start Date*</label>
                                <input type="date" class="form-control" id="startBidDate" v-model="startBidDate">
                            </div>
                            <div class="mb-3">
                                <label for="images" class="form-label">Images*</label>
                                <input type="file" @change="handleFileUpload" id="images" name="images" class="form-control" multiple>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-center my-5">
                        <router-link to="/myproperty">
                            <button type="button" class="btn mx-4" style="background-color: #6d8363; color: white;">Cancel</button>
                        </router-link>
                        <button type="button" class="btn mx-4" style="background-color: #447098; color: white;" @click="submit_add_listing()">Add Listing</button>
                    </div>
                   
                </form>
        </div>
    </div>
</template>

<script>

import axios from 'axios'


export default {
name: 'AddListingPage',
    components: {
    },
    data(){
        return {
            agent_id: this.agent_id_prop, //from app
            customer_id: '', //input based on the customer who called the agent
            name: '',
            address: '',
            postalcode: '',
            property_type: '',
            square_feet: '',
            room: '',
            facing: '',
            build_year: '',
            estimated_cost: '',
            image: '',
            starting_price: '',
            option_fee: '',
            neighbourhood: '',
            status: 'open',
            file: '',
        }   
    },
    methods: {
        async submit_add_listing(){
            

           
            const formData = new FormData();
            formData.append('property_image', this.file);
            let link = await axios.post('http://127.0.0.1:5200/download_image/', formData);
          
            link =  '../src/assets/' + link['data']
            this.image = link
            console.log(link)
            


            
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({
            "agent_id" : this.agent_id,
            "customer_id": this.customer_id,
            "name": this.name,
            "address": this.address,
            "postalcode": this.postalcode,
            "property_type": this.property_type,
            "square_feet": this.square_feet,
            "room": this.room,
            "facing": this.facing,
            "build_year": this.build_year,
            "estimated_cost": this.estimated_cost,
            "image": this.image,
            "status": this.status,
            "starting_price": this.starting_price,
            "option_fee": this.option_fee,
            "neighbourhood": this.neighbourhood,

            });
            console.log(raw)
            var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            };

            const data_fetch = await fetch("http://localhost:5200/add_listing", requestOptions)
            console.log(data_fetch)
            if(data_fetch['status']==201){
                alert("Listing has been successfully created")
            }
        },
        handleFileUpload(event) {
            this.file = event.target.files[0];
        },
        
    },
    props: [
        'agent_id_prop',
    ],
}

</script>

<style>

</style>






