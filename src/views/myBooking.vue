<template>
    <div style="min-height:100vh;">
        <h2 class="text-center my-4">
            Booking
        </h2>
        <div class="row justify-content-center d-flex">
            <div class="col-11 col-sm-10 col-md-9">
                <ul class="nav nav-tabs mb-5 mt-2" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button :class="{ active: isActive, 'nav-link':true }" @click="isActive = !isActive" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true">Pending Confirmation</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" :class="{ active: isActive, 'nav-link':true }" @click="isActive = !isActive" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">Accepted Bookings</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" :class="{ active: isActive, 'nav-link':true }" @click="isActive = !isActive" data-bs-toggle="tab" data-bs-target="#contact" type="button" role="tab" aria-controls="contact" aria-selected="false">Rejected Bookings</button>
                    </li>
                </ul>
                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                        <table class="table text-center">
                            <thead>
                                <tr>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Time</th>
                                    <th scope="col">Confirmation</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in pending" :key="item" class="table-style">
                                    <td>{{item.customer_name}}</td>
                                    <td>{{item.address}}</td>
                                    <td width="20%">{{item.datetime }}</td>
                                    <td>
                                        <div class="col" style="width:auto">
                                            <div class="row">
                                                <button type="button" class="btn btn-success bookingbutton" @click="accept(item.booking_id)">accept</button>
                                            </div>
                                            <br>
                                            <div class="row">
                                                <button type="button" class="btn btn-danger bookingbutton" @click="reject(item.booking_id)">reject</button>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                        <table class="table text-center">
                            <thead>
                                <tr>
                                
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="table-style" v-for="item in accepted" :key="item">
                            
                                    <td>{{item.customer_name}}</td>
                                <td>{{item.address}}</td>
                                <td width="20%">{{item.datetime }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
                        <table class="table text-center">
                            <thead>
                                <tr>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="table-style" v-for="item in rejected" :key="item">

                                    <td>{{item.customer_name}}</td>
                                <td>{{item.address}}</td>
                                <td width="20%">{{item.datetime }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>


export default {
name: 'MyBookingPage',
    components: {
    },
    data(){
        return{
            //update the array accordingly
            pending:  [],
            accepted: [],
            rejected: [],
        }
    },
    methods: {
        async accept(booking_id){
            let id = this.$route.params.id
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({});

            var requestOptions = {
            method: 'PUT',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
            };

            await fetch(`http://127.0.0.1:5000/booking/booking_action/${booking_id}/accept`, requestOptions)

            const response1 = await fetch(`http://127.0.0.1:5000/booking/pending/${id}`);
            const data1 = await response1.json(); 
            console.log(data1)
            if (data1.code != 404) {
                this.pending =  data1.data.books
            }
            else{
                this.pending = []
            }
            
            const response2 = await fetch(`http://127.0.0.1:5000/booking/accepted/${id}`);
            const data2 = await response2.json();
            console.log(data2)
            this.accepted =  data2.data.books
        },

        async reject(booking_id){
            let id = this.$route.params.id
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({});

            var requestOptions = {
            method: 'PUT',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
            };

            await fetch(`http://127.0.0.1:5000/booking/booking_action/${booking_id}/reject`, requestOptions)

            const response1 = await fetch(`http://127.0.0.1:5000/booking/pending/${id}`);
            const data1 = await response1.json(); 
            console.log(data1)
            if (data1.code != 404) {
                this.pending =  data1.data.books
            }
            else{
                this.pending = []
            }
            
            const response3 = await fetch(`http://127.0.0.1:5000/booking/rejected/${id}`);
            const data3 = await response3.json();
            if (data3.code != 404) {
                this.rejected =  data3.data.books
            }
            else{
                this.rejected = []
            }
        },       
        },

    async created() {
        let id = this.$route.params.id
        const response1 = await fetch(`http://127.0.0.1:5000/booking/pending/${id}`);
        const data1 = await response1.json(); 
        if (data1.code != 404  ) {
            this.pending =  data1.data.books
        }
        else {
            this.pending = []
        }
        
        

        const response2 = await fetch(`http://127.0.0.1:5000/booking/accepted/${id}`);
        const data2 = await response2.json();
        this.accepted =  data2.data.books
        if(data2.code != 404){
            this.accepted = data2.data.books
        }
        else{
            this.accepted = []
        }
        

        const response3 = await fetch(`http://127.0.0.1:5000/booking/rejected/${id}`);
        const data3 = await response3.json();
        this.rejected =  data3.data.books
        if(data2.code != 404){
            this.rejected = data3.data.books
        }
        else{
            this.rejected = []
        }
    }
}


</script>

<style>
.nav-link {
    color: black
}

.table-style{
    background-color: antiquewhite;
}
.bookingbutton{
    width: 30%;
}
</style>

