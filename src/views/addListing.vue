<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
                <h2 class="text-center my-5">Add Listing</h2>
                <form>
                    <div class="row">
                        <div class="col-12 col-md-6 px-5">
                            <div class="mb-3">
                                <label for="address" class="form-label">Customer ID*</label>
                                <input v-model="customer_id" type="text" class="form-control" id="address">
                            </div>
                            <div class="mb-3">
                                <label for="address" class="form-label">Address*</label>
                                <input v-model="address" type="text" class="form-control" id="address">
                            </div>
                            <div class="mb-3">
                                <label for="address" class="form-label">Name*</label>
                                <input v-model="name" type="text" class="form-control" id="address">
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
                                <label for="buildYear" class="form-label">Build Year*</label>
                                <input v-mode="buildyear" type="text" class="form-control" id="buildYear">
                            </div>
                            <div class="mb-3">
                                <label for="size" class="form-label">Size in Square Feet*</label>
                                <input v-model="size" type="text" class="form-control" id="size">
                            </div>
                            <div class="mb-3">
                                <label for="roomNo" class="form-label">Number of Rooms*</label>
                                <input v-model="rooomNo" type="number" class="form-control" id="roomNo">
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
                                <input type="text" class="form-control" id="optionFee">
                            </div>
                            <div class="mb-3">
                                <label for="minBidAmount" class="form-label">Minimum Bid Amount*</label>
                                <input type="text" class="form-control" id="minBidAmount">
                            </div>
                            <div class="mb-3">
                                <label for="startBidDate" class="form-label">Bidding Start Date*</label>
                                <input type="date" class="form-control" id="startBidDate" v-model="startBidDate">
                            </div>
                            <div class="mb-3">
                                <label for="images" class="form-label">Images*</label>
                                <input type="file" id="images" name="images" accept="image/*" class="form-control" multiple>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-center my-5">
                        <router-link to="/myproperty">
                            <button type="submit" class="btn mx-4" style="background-color: #6d8363; color: white;">Cancel</button>
                        </router-link>
                        <button type="submit" class="btn mx-4" style="background-color: #447098; color: white;" @click="submit_add_listing()">Add Listing</button>
                    </div>
                </form>
        </div>
    </div>
</template>

<script>

export default {
name: 'AddListingPage',
    components: {
    },
    data(){
        return {
            agent_id: this.agent_id_prop,
            customer_id: '',
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
            status: 'open'
        }   
    },
    methods: {
        async submit_add_listing(){
            
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
            redirect: 'follow'
            };

            const data_fetch = await fetch("http://127.0.0.1:5100/make_booking", requestOptions)
            if(data_fetch['code']==201){
                alert("listing has been created")
            }
        }
    },
    props: [
        'agent_id_prop',
    ],
}

</script>

<style>

</style>


