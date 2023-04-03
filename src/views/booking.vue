<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
            <div class="col-10 col-md-8 col-lg-7 my-3">
                <h2 class="text-center my-4">Book An Appointment</h2>
                <div v-if="check_make_booking==false">
                    <form>
                    <div class="mb-3">
                        <label for="customerID" class="form-label">Customer ID</label>
                        <input type="text" class="form-control" id="customerID" v-bind:value="customer_id_prop" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="agentID" class="form-label">Agent ID</label>
                        <input type="text" class="form-control" id="agentID" v-bind:value="agent_id_prop" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="propertyID" class="form-label">Property ID</label>
                        <input type="text" class="form-control" id="propertyID" v-bind:value="property_id_prop" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="bookingDate" class="form-label">Select a Date*</label>
                        <input type="date" class="form-control" id="bookingDate" v-model="bookingDate">
                    </div>
                    <div class="mb-3">
                        <label for="bookingStartTime" class="form-label">Select Start Time*</label>
                        <select class="form-select" id="bookingStartTime" v-model="bookingStartTime">
                            <option selected>hh:mm</option>
                            <option value="0900">09:00</option>
                            <option value="1000">10:00</option>
                            <option value="1100">11:00</option>
                            <option value="1200">12:00</option>
                            <option value="1300">13:00</option>
                            <option value="1400">14:00</option>
                            <option value="1500">15:00</option>
                            <option value="1600">16:00</option>
                            <option value="1700">17:00</option>
                            <option value="1800">18:00</option>
                            <option value="1900">19:00</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="bookingEndTime" class="form-label">Select End Time*</label>
                        <select class="form-select" id="bookingEndTime" v-model="bookingEndTime">
                            <option selected>hh:mm</option>
                            <option value="1000">10:00</option>
                            <option value="1100">11:00</option>
                            <option value="1200">12:00</option>
                            <option value="1300">13:00</option>
                            <option value="1400">14:00</option>
                            <option value="1500">15:00</option>
                            <option value="1600">16:00</option>
                            <option value="1700">17:00</option>
                            <option value="1800">18:00</option>
                            <option value="1900">19:00</option>
                            <option value="2000">20:00</option>
                        </select>
                    </div>
                    <div class="d-flex justify-content-around">
                        <router-link to="/">
                            <button type="submit" class="btn" style="background-color: #6d8363; color: white;">Cancel</button>
                        </router-link>
                        <button @click="call_makebooking()" type="button" class="btn" style="background-color: #447098; color: white;">Book Now</button>
                    </div>
                </form>
                </div>
                <div v-else>
                    <div style="text-align: center;">Booking successful</div>
                    <br>
                    <br>
                    <div style="text-align: center;">Agent information</div>
                    <br>
                    <div class="row">
                        <div class="col">
                            Agent Name:
                        </div>
                        <div class="col">
                            {{ check['name'] }}
                        </div>
                    <div class="row">
                        <div class="col">
                            Agent Contact Information:
                        </div>
                        <div class="col">
                            {{ check['phone'] }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Agent Email:
                        </div>
                        <div class="col">
                            {{ check['email'] }}
                        </div>
                    </div>
                    <br>
                    <br>
                    <div style="text-align: center;">Property Information</div>
                    <br>
                    <br>
                    <div class="row">
                        <div class="col">
                            Property Name
                        </div>
                        <div class="col">
                            {{ check['property_name'] }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Property Address
                        </div>
                        <div class="col">
                            {{ check['address'] }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Booking start time
                        </div>
                        <div class="col">
                            {{ bookingStartTime }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Booking end time
                        </div>
                        <div class="col">
                            {{ bookingEndTime }}
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
name: 'BookingPage',
    components: {
    },
    props: [
        'customer_id_prop',
        'agent_id_prop',
        'property_id_prop',
    ],
    
    data(){
        return{
            customerID: this.customer_id_prop,
            agentID: this.agent_id_prop,
            propertyID: this.property_id_prop,
            bookingDate:"",
            bookingStartTime:"",
            bookingEndTime:"",

            name: "",
            email: "",
            contact: "",
            propertyAddress: "",
            check: [],
            check_make_booking : false,

        }
    },
    computed: {
        date_time_start(){
            let final = this.bookingDate
            let timing = this.bookingStartTime.slice(0,2)
            timing = timing + ':' + '00'+':'+'00'
            final = final + ' ' + timing
            return final
        },
        date_time_end(){
            let final = this.bookingDate
            let timing = this.bookingEndTime.slice(0,2)
            timing = timing + ':' + '00'+':'+'00'
            final = final + ' ' + timing
            return final
        }
    },
    methods: {
            async call_makebooking(){
            //let dateTimeStart = this.date_time_end
            //let dateTimeEnd = this.date_time_end
            

            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({
            "agent_id": this.agentID,
            "customer_id": this.customerID,
            "property_id": this.propertyID,
            "datetimestart": this.date_time_start,
            "datetimeend": this.date_time_end,
            "status": "pending"
            });
            var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
            };

            const data_fetch = await fetch("http://127.0.0.1:5800/make_booking", requestOptions)
           
            let item = await data_fetch.json()
            this.check = item

            if (data_fetch['status'] != 200){
                alert('Booking creation failed')
            } 
            else{
                this.check_make_booking = true
                console.log(this.check)
            }
                    },   
    },
}

</script>

<style scoped>

</style>
