<template>
    <div>

        <!--Carousel room images-->
        <div class="carousel slide" data-bs-ride="false" id="carousel-1">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img class="w-100 d-block"  :src=getimage(property_result.image) alt="Slide Image" width="1393" height="525">
                </div>
                <!-- <div class="carousel-item">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
                <div class="carousel-item">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div> -->
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
                        <p>
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
                <div v-if='!bidSuccess' class="my-5">
                    <div class="row mb-3">
                        <div class="col">
                            <p class="text-center fw-bold">
                                ${{property_result.estimated_cost}}
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">Minimum Bid</small>
                            </p>
                        </div>
                        <!-- <div class="col">
                            <p class="text-center fw-bold">
                                $13771
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">My Current Bid</small>
                            </p>
                        </div> -->
                        <div class="col">
                            <p class="text-center fw-bold">
                                ${{ highestBid }}
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">Highest Bid</small>
                            </p>
                        </div>
                    </div>
                    <div class="input-group mb-3">
                        <input v-model='bidAmount' type="text" class="form-control" placeholder="Enter your bid" aria-label="Enter your bid" aria-describedby="button-addon1">
                        <button class="btn" type="button" style="background-color: #447098; color: white;" id="button-addon"  @click="submitBid(jsonBody)">Place Bid</button>
                    </div>
                </div>
                <div v-else>
                    <p class="text-center fw-bold my-5"> Your bid is successful</p>
                    <!-- <router-link to="/mybids">
                        <button class="btn" type="button" style="background-color: #447098; color: white;" id="button-addon"  @click="submitBid()">View Bid</button>
                    </router-link> -->
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

    },
    props: [
    'property_id_prop',
    'customer_id_prop'
    ],
    data(){
        return{
            //return property details
            property_result:[],
            agent_result:[],
            bid_result:[],
            message: "",
            // property_id:"1",//passed in from propertycard
            // customer_id:"1", //passed in from propertycard
            filtered_result:[],
            biddingStartTime:"",
            biddingEndTime:"",
            imagename2: "",

            // customerId:1,
            // propertyId:1,
            bidAmount:0,
            bidSuccess:false,
            highestBid: 0,

        }
    },

    async created() {

        // on Vue instance created, load the book list
        this.findpropertydetails();
        this.findagentdetails();
        this.findauctiondetails();
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
        },
        jsonBody(){
            return {
                "customer_id": this.customer_id_prop,
                "bid_amount": parseFloat(this.bidAmount),
                "property_id":this.property_id_prop
            }
        }


    },

    methods:{
        //get property details based on complex microservice
        findpropertydetails() {
        console.log("here")
        // this.property_id_prop={{}}
        console.log("property_id:"+this.property_id_prop)
        var search_url = get_all_URL + '/'+ this.property_id_prop +'/'+this.customer_id_prop
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
            this.findHighestBid()

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
            const newKey = capitalizedKey.replace(/_/g, ' ');
            filtered_result[newKey] = value;
            }
        })

        this.filtered_result=filtered_result
        console.log(filtered_result)

        // }
        },

        findagentdetails() {
        console.log("here is agent")
        var search_url = get_all_URL + '/'+ this.property_id_prop +'/'+this.customer_id_prop
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
        var search_url = get_all_URL + '/'+ this.property_id_prop +'/'+this.customer_id_prop
        console.log(search_url)
        const response = fetch(search_url)
        .then((response) => response.json())
        .then((data) => {
            console.log(response);
            
            if (data.code === 404) {
            // no book in db
            this.message = data.message;
            console.log("error")
            } else {
            this.bid_result = data.data.bid_result.data;
            console.log(this.bid_result)
            if (this.bid_result==true){
                this.bidSuccess=true
            }
            else this.bidSuccess=false
            
            }
        })
        .catch((error) => {
            // Errors when calling the service; such as network error,
            // service offline, etc
            console.log("266")
            console.log(this.message + error);
        });
        },
        async submitBid(jsonBody){
            console.log(jsonBody)
            console.log('hello')
            try {
                const submit_url = "http://localhost:5900/make_bid";
                const options = {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jsonBody)
                };

                const response = await fetch(submit_url, options);
                const result = await response.json();
                console.log(result)
                alert("Bid has been made.")

            } catch (error) {
                console.error(error);
                alert("Creation of bid failed.")
            }
        },
        //idk if it works :o
        // async submitBid(){
        //     // let dateTimeStart = this.date_time_end
        //     // let dateTimeEnd = this.date_time_end
            

        //     var myHeaders = new Headers();
        //     myHeaders.append("Content-Type", "application/json");

        //     var raw = JSON.stringify({

        //     "customer_id": this.customer_id_prop,
        //     "bid_amount": parseInt(this.bidAmount),
        //     "property_id":this.property_id_prop
        
        //     });
        //     console.log(raw)
        //     var requestOptions = {
        //     method: 'POST',
        //     headers: myHeaders,
        //     body: raw,
        //     redirect: 'follow'
        //     };

        //     const data_fetch = await fetch("http://localhost:5900/make_bid", requestOptions)
        //     this.check = await data_fetch.json()
        //     console.log(data_fetch)
        //     if (data_fetch['status'] == 201){
        //         alert('Bid has been submitted')
        //     } 
        //     else{
        //         alert('Bid creation failed')
        //     }
        // },
        getimage(image){
        return require('@/assets/' + image)
        },

        async findHighestBid(){
            console.log(this.property_result.auction_id)
            console.log(this.property_result)
            console.log('hgoebgbekjg ')

            try {
                var get_property_url = "http://localhost:5500/bids/highest_bid/" + String(this.property_result.auction_id);
                var response = await fetch(get_property_url);

                if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
                }

                var data = await response.json();
                console.log(data)
                this.highestBid = data['data']['highest_bid']

            } catch (error) {
                console.error(error);
            }
            console.log('-------')
        }

    }
};

</script>

<style></style>