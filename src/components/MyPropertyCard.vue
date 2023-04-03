<template>
    <div class="col-12 col-sm-6 col-md-4 col-xl-3 p-4">
        <div class="card">
            <div class="card-body shadow " style="padding-top: 0px;padding-left: 0px;padding-right: 0px;">
                <div class="carousel slide" data-bs-ride="false" :id="carouselIdStr">
                    <div class="carousel-inner">
                        <div class="carousel-item active"><img class="w-100 d-block fit-cover" :src=getimage(property_image) alt="Slide Image" ></div>
                        <!-- <div class="carousel-item"><img class="w-100 d-block" v-bind:src=getimage(property_image) alt="Slide Image"></div> -->
                        <!-- <div class="carousel-item"><img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image"></div> -->
                    </div>
                    <div>
                        <a class="carousel-control-prev" :href="carouselHrefStr" role="button" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon"></span>
                            <span class="visually-hidden">Previous</span>
                        </a>
                        <a class="carousel-control-next" :href="carouselHrefStr" role="button" data-bs-slide="next">
                            <span class="carousel-control-next-icon"></span>
                            <span class="visually-hidden">Next</span>
                        </a>
                    </div>
                    <ol class="carousel-indicators">
                        <li :data-bs-target="carouselHrefStr" data-bs-slide-to="0" class="active"></li>
                        <!-- <li :data-bs-target="carouselHrefStr" data-bs-slide-to="1"></li>
                        <li :data-bs-target="carouselHrefStr" data-bs-slide-to="2"></li> -->
                    </ol>
                </div>
                <div class="card-body p-4">
                    <h5 class="card-title my-3">{{ property_name }}</h5>
                    <p class="card-text">{{ property_add }}</p>
                    <!-- <p class="card-text">{{property_image}}</p> -->
                    <p class="card-text">${{ property_estimated_cost }}</p>

                        <div class ="d-flex justify-content-between">
                            <a v-if="close==false" class="btn btn-light float-end" type="button" style="background-color: #6d8363; color: white;" @click="closeBidding(jsonBodyClose);set_closed();">
                                Close Bidding
                            </a>
                            <a v-else>

                            </a>
                            <a class="btn btn-light float-end" type="button" style="background-color: #447098; color: white;" data-bs-toggle="modal" data-bs-target="#modal">
                                Edit Listing
                            </a>
                        </div>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="modal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Update Property Details</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="propertyName" class="form-label">Property Name</label>
                        <input type="text" class="form-control" v-model="updatedName" id="propertyName">
                    </div>
                    <div class="mb-3">
                        <label for="propertyAddress" class="form-label">Address</label>
                        <input type="text" class="form-control" v-model="updatedAddress" id="propertyAddress">
                    </div>
                    <div class="mb-3">
                        <label for="propertyPC" class="form-label">Postal Code</label>
                        <input type="text" class="form-control" v-model="updatedPostalCode" id="propertyPC">
                    </div>
                    <div class="mb-3">
                        <label for="propertyType" class="form-label">Property Type</label>
                        <input type="text" class="form-control" v-model="updatedType" id="propertyType">
                    </div>
                    <div class="mb-3">
                        <label for="propertySquareFeet" class="form-label">Square Feet</label>
                        <input type="text" class="form-control" v-model="updatedSquareFeet" id="propertySquareFeet">
                    </div>
                    <div class="mb-3">
                        <label for="propertyRoom" class="form-label">Number of Rooms</label>
                        <input type="text" class="form-control" v-model="updatedRoom" id="propertyRoom">
                    </div>
                    <div class="mb-3">
                        <label for="propertyFacing" class="form-label">Property Facing Direction</label>
                        <input type="text" class="form-control" v-model="updatedFacing" id="propertyFacing">
                    </div>
                    <div class="mb-3">
                        <label for="propertyBuildYear" class="form-label">Build Year</label>
                        <input type="text" class="form-control" v-model="updatedBuildYear" id="propertyBuildYear">
                    </div>
                    <div class="mb-3">
                        <label for="propertyEstimatedCost" class="form-label">Estimated Cost</label>
                        <input type="text" class="form-control" v-model="updatedEstimatedCost" id="propertyEstimatedCost">
                    </div>
                    <div class="mb-3">
                        <label for="propertyNeighourhood" class="form-label">Neigbourhood</label>
                        <input type="text" class="form-control" v-model="updatedNeighbourhood" id="propertyNeigbourhood">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal" style="background-color: #6d8363; color: white;" >Close</button>
                    <button type="button" class="btn btn-primary ms-2" style="background-color: #447098; color: white;" @click="editListing(jsonBodyEdit)"  data-bs-dismiss="modal">Save changes</button>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PropertyCard',
    props: [
        'carouselNum',
        'property_name',
        'property_add',
        'property_postal_code',
        'property_type',
        'property_square_feet',
        'property_room',
        'property_facing',
        'property_build_year',
        'property_estimated_cost',
        'property_neighbourhood',
        'property_image',
        'property_id',
        'auction_id',
        'property_agent_id',
        'property_customer_id'
],
    data(){ // or could put it in props
        return{
            carouselHrefStr:"#carousel-" + this.carouselNum,
            carouselIdStr: "carousel-" + this.carouselNum,
            imageSrc:'',
            imagename: "",
            imagename2: "",
            updatedName: this.property_name,
            updatedAddress: this.property_add,
            updatedPostalCode: this.property_postal_code,
            updatedType: this.property_type,
            updatedSquareFeet: this.property_square_feet,
            updatedRoom: this.property_room,
            updatedFacing: this.property_facing,
            updatedBuildYear: this.property_build_year,
            updatedEstimatedCost: this.property_estimated_cost,
            image: 'room1.jpg',
            updatedNeighbourhood: this.property_neighbourhood,
            close: ''
        }
    },
    computed:{
        jsonBodyClose(){
            return {
                "auction_id": Number(this.auction_id),
                "status": "close"
            }
        },
        jsonBodyEdit(){
            return {
                
                "agent_id": this.property_agent_id,
                "customer_id": this.property_customer_id,
                "name": this.updatedNeighbourhood,
                "address": this.updatedAddress,
                "postalcode": this.updatedPostalCode,
                "property_type": this.updatedType,
                "square_feet": this.updatedSquareFeet,
                "room": this.updatedRoom,
                "facing": this.updatedFacing,
                "build_year": this.updatedBuildYear,
                "estimated_cost": this.updatedEstimatedCost,
                "image": this.property_image,
                "neighbourhood": this.updatedNeighbourhood
            }
        }
    },
    methods:{
    // submit_property_data(){
    //     console.log('current_id:'+this.property_id_card)
    //   this.$emit('submit_property_data', this.property_id_card)
    //   this.$router.push('/propertydetails')

    // },
    getimage(image){
        return require('@/assets/' + image)
    },
    // handleClick() {
    //   this.$emit('property-clicked', this.propertyId);
    // }
    
    async closeBidding(jsonBody){
        console.log(jsonBody)
            try {
                const update_url = 'http://localhost:5801/close_bid';
                const options = {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jsonBody)
                };

                const response = await fetch(update_url, options);
                const result = await response.json();
                console.log(result)
                alert("Bidding has been successfully closed")
            } catch (error) {
                console.error(error);
                alert("Something went wrong! Please try to close the bidding again.")
            }
        },

    async editListing(jsonBody){
        console.log(jsonBody)
            try {
                const update_url = 'http://localhost:5001/property/' + String(this.property_id);
                console.log(update_url)
                const options = {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jsonBody)
                };

                const response = await fetch(update_url, options);
                const result = await response.json();
                console.log(result)
                alert("Property Details have been successfully changed")
            } catch (error) {
                console.error(error);
                alert("Something went wrong! Please try to update the details again.")
            }
        },
        set_closed(){
            this.close = true
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>


