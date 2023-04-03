<template>
    <div class="col-12 col-sm-6 col-md-4 col-xl-3 p-4">
        <div class="card">
            <div class="card-body shadow " style="padding-top: 0px;padding-left: 0px;padding-right: 0px;">
                <div class="carousel slide" data-bs-ride="false" :id="carouselIdStr">
                    <div class="carousel-inner">
                        <div class="carousel-item active"><img class="w-100 d-block fit-cover" src="../assets/room1.jpg" alt="Slide Image" ></div>
                        <div class="carousel-item"><img class="w-100 d-block" v-bind:src="imageSrc" alt="Slide Image"></div>
                        <div class="carousel-item"><img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image"></div>
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
                        <li :data-bs-target="carouselHrefStr" data-bs-slide-to="1"></li>
                        <li :data-bs-target="carouselHrefStr" data-bs-slide-to="2"></li>
                    </ol>
                </div>
                <div class="card-body p-4">
                    <h5 class="card-title my-3">{{ property_name }}</h5>
                    <p class="card-text">{{ property_add }}</p>
                    <p class="card-text">${{ bid.bid_amount }}</p>
                    <div class="d-flex justify-content-between">
                        <a class="btn btn-light float-end" type="button" style="background-color: #6d8363; color: white;" @click="retractBid(bid.bid_id)">
                            Retract Bid
                        </a>
                        <a class="btn btn-light float-end" type="button" style="background-color: #447098; color: white;" data-bs-toggle="modal" data-bs-target="#updateModal">
                            Update Bid
                        </a>
                    </div>
                </div>
                <!-- Modal -->
                <div class="modal fade" id="updateModal" tabindex="-1" aria-labelledby="updateModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="updateModalLabel">Update Bid</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="updateBidAmount" class="form-label">Updated Bid Amount</label>
                                    <input type="text" class="form-control" id="updateBidAmount" v-model="updatedBid">
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" style="background-color: #6d8363; color: white;">Close</button>
                                <button type="button" class="btn btn-primary" @click="updateBid(bid.bid_id, updatedBidJson)" style="background-color: #447098; color: white;" data-bs-dismiss="modal">Save Changes</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BidPropertyCard',
    props: {
        bid: Object,
        index: Number,
        property_name: String,
        property_add: String,
        estimated_cost: Number,
        property_image:String,
    },
    data(){ // or could put it in props
        return{
            updatedBid: "",
            carouselHrefStr:"#carousel-" + this.carouselNum,
            carouselIdStr: "carousel-" + this.carouselNum,
            imageSrc:'../assets/room2.jpg'
        }
    },
    computed:{
        updatedBidJson() {
            return {
            "bid_amount": Number(this.updatedBid)
            }
        }
    },
    methods:{
        async retractBid(bid_id){
            try {
                const delete_url = "http://localhost:5500/bids/" + String(bid_id);
                const response = await fetch(delete_url, {
                    method: "DELETE",
                });
                const result = await response.json();
                console.log(result);
                alert("Bid has been retracted")
                // location.reload();
            } catch (error) {
                console.error(error);
                alert("Retraction of bid has failed")
            }
        },
        async updateBid(bid_id, updatedBidData){
            console.log(updatedBidData)
            try {
                const update_url = "http://localhost:5500/bids/" + String(bid_id);
                const options = {
                    method: 'PUT',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updatedBidData)
                };

                const response = await fetch(update_url, options);
                const result = await response.json();
                console.log(result)
                alert("Bid details has been updated.")

            } catch (error) {
                console.error(error);
                alert("Bid detail update has failed")
            }
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
