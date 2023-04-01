<template>
    <div style="min-height:100vh;">
        <h2 class="text-center my-5">
            My Bookings
        </h2>
        <div class="row justify-content-center d-flex">
            <div class="col-11 col-sm-10 col-md-9">
                <ul class="nav nav-tabs mb-5 mt-2" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true" style="color:black">Pending Confirmation</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" :class="{ active: isActive, 'nav-link':true }" @click="isActive = !isActive" data-bs-toggle="tab" data-bs-target="#profile" role="tab" aria-controls="profile" aria-selected="false" style="color:black">Accepted Bookings</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" :class="{ active: isActive, 'nav-link':true }" @click="isActive = !isActive" data-bs-toggle="tab" data-bs-target="#contact" role="tab" aria-controls="contact" aria-selected="false" style="color:black">Rejected Bookings</button>
                    </li>
                </ul>
                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                        <table class="table">
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
                                    <td width="20%">{{item.booking_time }}</td>
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
                        <table class="table">
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
                                <td width="20%">{{item.booking_time }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
                        <table class="table">
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
                                <td width="20%">{{item.booking_time }}</td>
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
    props: [
        'agent_id_prop'
    ],
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
            for(let item of this.pending){
                if(booking_id == item['booking_id']){
                    item['status'] = 'accepted'
                    let to_add = {}
               
                    for(let add in item){
                        to_add[add] = item[add]
                    }
                    var myHeaders = new Headers();
                    myHeaders.append("Content-Type", "application/json");
                    console.log(to_add)
                    var raw = JSON.stringify({
                        to_add
                    });
                 
                    raw = raw.slice(10)
                    raw = raw.slice(0,raw.length -1 )
                    console.log(raw)
                    var requestOptions = {
                    method: 'PUT',
                    headers: myHeaders,
                    body: raw,
                    redirect: 'follow'
                    };
                    await fetch("http://127.0.0.1:5101/accept_booking", requestOptions)

                    let indexOf = this.pending.indexOf(item)
                    this.pending.splice(indexOf,1)
                    this.accepted.push(item)
                    break
                }
            }
        },   
        async reject(booking_id){
            for(let item of this.pending){
                if(booking_id == item['booking_id']){
                    item['status'] = 'rejected'
                    let to_add = {}
               
                    for(let add in item){
                        to_add[add] = item[add]
                    }
                    var myHeaders = new Headers();
                    myHeaders.append("Content-Type", "application/json");
                    console.log(to_add)
                    var raw = JSON.stringify({
                        to_add
                    });
                 
                    raw = raw.slice(10)
                    raw = raw.slice(0,raw.length -1 )
                    console.log(raw)
                    var requestOptions = {
                    method: 'PUT',
                    headers: myHeaders,
                    body: raw,
                    redirect: 'follow'
                    };
                    await fetch("http://127.0.0.1:5101/accept_booking", requestOptions)

                    let indexOf = this.pending.indexOf(item)
                    this.pending.splice(indexOf,1)
                    this.rejected.push(item)
                    break
                }
            }
        } 
        },

    async created() {
        var URLL = `http://127.0.0.1:5102/get_booking/` + this.agent_id_prop
        const response1 = await fetch(URLL);
        const data = await response1.json(); 
        let pending_data = data['pending']
        let accepted_data = data['accepted']
        let rejected_data = data['rejected']
    
        let all_list = pending_data.concat(accepted_data)
        all_list = all_list.concat(rejected_data)

        for(let item of all_list){
            let start_time = item['datetimestart'].split(' ')
            start_time = start_time.slice(0,5)
            start_time = start_time.join(' ')
            let end_time = item['datetimeend'].split(' ')[4]
            let final_time = start_time + ' - ' + end_time
            item['booking_time'] = final_time
        }

        for(let item of all_list){
            let customer_id = item['customer_id']
            const response2 = await fetch(`http://127.0.0.1:5102/get_booking_extra_info/${customer_id}`)
            const data2 = await response2.json();  
            item['address'] = data2['address']
            item['customer_name'] = data2['customer_name']
        }
        console.log(all_list)
     
        for(let item of all_list){
            if(item.status == 'pending'){
                this.pending.push(item)
            }
            else if(item.status == 'accepted'){
                this.accepted.push(item)
            }
            else{
                this.rejected.push(item)
            }
        }
        console.log(all_list)
    }
}


</script>

<style scoped>
.nav-link.active{
    background-color: #447098;
    font-weight: bold;
    color: white !important;
}
.table-style{
    background-color: antiquewhite;
}
.bookingbutton{
    width: 30%;
}
</style>





