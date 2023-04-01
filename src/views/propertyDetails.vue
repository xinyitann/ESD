<template>
    <div>

        <!--Carousel room images-->
        <div class="carousel slide" data-bs-ride="false" id="carousel-1">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
                <div class="carousel-item">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
                <div class="carousel-item">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
            </div>
            <div>
                <a class="carousel-control-prev" href="#carousel-1" role="button" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                    <span class="visually-hidden">Previous</span>
                </a>
                <a class="carousel-control-next" href="#carousel-1" role="button" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                    <span class="visually-hidden">Next</span>
                </a>
            </div>
            <ol class="carousel-indicators">
                <li data-bs-target="#carousel-1" data-bs-slide-to="0" class="active"></li>
                <li data-bs-target="#carousel-1" data-bs-slide-to="1"></li>
                <li data-bs-target="#carousel-1" data-bs-slide-to="2"></li>
            </ol>
        </div>

        <div class="p-5 row w-100">
            <div class="col-12 col-md-7 p-2">
                <h3 class="mb-3">{{ property_result.name }}</h3>
                <p class="fs-5">${{ property_result.estimated_cost }}</p>
                <hr>
                <table class="table table-borderless">
                    <tr v-for="(value, key) in filtered_result" :key="key" >
                    <th>{{ key }}</th>
                    <td>{{ value }}</td>
                    </tr>
                </table>
            </div>
            <div class="col-12 col-md-5">
                <div class="card p-3">
                    <h5 class="card-title text-center my-2">Interested?</h5>
                    <div class="card-body">
                        <p>{{ property_id }}
                            Contact {{ agent_result.name }} @ +65 {{ agent_result.phone }} / {{ agent_result.email }}
                        </p>
                        <div class="row">
                            <div class="col-4">
                                <hr>
                            </div>
                            <div class="col-4 text-center">OR</div>
                            <div class="col-4">
                                <hr>
                            </div>
                        </div>
                        <div class="d-flex justify-content-center mt-3">
                            <router-link to="/bookingnow">
                                <a class="btn" type="button" style="background-color: #447098; color: white;">
                                    Book Appointment Now
                                </a>
                            </router-link>
                        </div>
                    </div>
                </div>
                <div class="my-5">
                    <div class="row mb-3">
                        <div class="col">
                            <p class="text-center fw-bold">
                                ${{auction_result.starting_price}}
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">Minimum Bid</small>
                            </p>
                        </div>
                        <div class="col">
                            <p class="text-center fw-bold">
                                $13771
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">My Current Bid</small>
                            </p>
                        </div>
                        <div class="col">
                            <p class="text-center fw-bold">
                                ${{auction_result.highest_bid}}
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">Highest Bid</small>
                            </p>
                        </div>
                    </div>
                    <div class="input-group mb-3">
                        <input v-model='bidAmount' type="text" class="form-control" placeholder="Enter your bid" aria-label="Enter your bid" aria-describedby="button-addon1">
                        <button class="btn" type="button" style="background-color: #447098; color: white;" id="button-addon"  @click="submitBid()">Place Bid</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import PropertyCard from '@/components/propertyCard.vue';

//to edit later 
const get_all_URL = "http://localhost:5009/get_property_details";


export default {
name: 'PropertyDetailsPage',
    components: {
        // this.$router.push({ path: '/user/' + userId }),

    },
    props: {
    property_id: String 
 },
    data(){
        return{
            //return property details
            property_result:[],
            agent_result:[],
            auction_result:[],
            message: "",
            // property_id:"1",//passed in from properties
            customer_id:"1", //should not be search
            filtered_result:[],
            biddingStartTime:"",
            biddingEndTime:"",

            customerId:1,
            // propertyId:1,
            bidAmount:0,
            

        }
    },

    created() {
                // on Vue instance created, load the book list
                this.findpropertydetails();
                this.findagentdetails();
                
            },
    computed: {
        date_time_start(){
            let final = this.biddingDate
            let timing = this.biddingStartTime.slice(0,2)
            timing = timing + ':' + '00'+':'+'00'
            final = final + ' ' + timing
            return final
        },
        date_time_end(){
            let final = this.biddingDate
            let timing = this.biddingEndTime.slice(0,2)
            timing = timing + ':' + '00'+':'+'00'
            final = final + ' ' + timing
            return final
        }
    },

    methods:{
        //get property details based on complex microservice
        findpropertydetails() {
        console.log("here")
        // this.property_id={{}}
        console.log(this.property_id)
        var search_url = get_all_URL + '/'+ this.property_id +'/'+this.customer_id
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

        
            this.transformObject(this.property_result)
            }
        })
        .catch((error) => {
            // Errors when calling the service; such as network error,
            // service offline, etc
            console.log(this.message + error);
        });
        },

        transformObject(input) {
            const excludedKeys = ['agent_id', 'auction_id','image','property_id','name'];
        const filtered_result = {};
        
        Object.entries(input).forEach(([key, value]) => {
            if (!excludedKeys.includes(key)) {
            const capitalizedKey = key.charAt(0).toUpperCase() + key.slice(1);
            filtered_result[capitalizedKey] = value;
            }
        })

        this.filtered_result=filtered_result
        console.log(filtered_result)

        // }
        },

        findagentdetails() {
        console.log("here is agent")
        var search_url = get_all_URL + '/'+ this.property_id +'/'+this.customer_id
        console.log(search_url)
        const response = fetch(search_url)
        .then((response) => response.json())
        .then((data) => {
            console.log(response);
            
            if (data.code === 404) {
            // no book in db
            this.message = data.message;
            } else {
            this.agent_result = data.data.agent_result.data;
            console.log(this.agent_result)
            }
        })
        .catch((error) => {
            // Errors when calling the service; such as network error,
            // service offline, etc
            console.log(this.message + error);
        });
        },

        findauctiondetails() {
        console.log("here is auction")
        var search_url = get_all_URL + '/'+ this.property_id +'/'+this.customer_id
        console.log(search_url)
        const response = fetch(search_url)
        .then((response) => response.json())
        .then((data) => {
            console.log(response);
            
            if (data.code === 404) {
            // no book in db
            this.message = data.message;
            } else {
            this.auction_result = data.data.auction_result.data;
            console.log(this.auction_result)
            }
        })
        .catch((error) => {
            // Errors when calling the service; such as network error,
            // service offline, etc
            console.log(this.message + error);
        });
        },
        //idk if it works :o
        async submitBid(){
            // let dateTimeStart = this.date_time_end
            // let dateTimeEnd = this.date_time_end
            

            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({

            "customer_id": this.customerId,
            "bid_amount": parseInt(this.bidAmount),
            "property_id":this.propertyId
        
            });
            console.log(raw)
            var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
            };

            const data_fetch = await fetch("http://localhost:5900/make_bid", requestOptions)
            this.check = await data_fetch.json()
            console.log(data_fetch)
            if (data_fetch['status'] == 201){
                alert('bidding has been created')
            } 
            else{
                alert('bidding failed')
            }
                    },


}
};

</script>

<style></style>