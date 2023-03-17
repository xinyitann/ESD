<template>
    <div style="font-family: sans-serif;font-size: 40px;text-align: center;">
        Booking
     </div>
    <div id="bookingtemplate">
        <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="pending-tab" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true">pending</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="accepted-tab" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">accepted</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="rejected-tab" data-bs-toggle="tab" data-bs-target="#contact" type="button" role="tab" aria-controls="contact" aria-selected="false">rejected</button>
        </li>
        </ul>
        <div class="tab-content" id="myTabContent">
        <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
<table class="table">
  <thead>
    <tr>

        <th scope="col">Name</th>
        <th scope="col">Address</th>
        <th scope="col">Confirmation</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="item in pending" :key="item" class="table-style">
     
      <td>{{item.CustomerName}}</td>
      <td>{{item.Address}}</td>
      <td>
        <div class="col">
            <div class="row">
                <button type="button" class="btn btn-success bookingbutton">accept</button>
            </div>
            <br>
            <div class="row">
                <button type="button" class="btn btn-danger bookingbutton">reject</button>
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
      
        <th scope="col">Name</th>
        <th scope="col">Address</th>
    </tr>
  </thead>
  <tbody>
    <tr class="table-style" v-for="item in accepted" :key="item">
  
      <td>{{item.CustomerName}}</td>
      <td>{{item.Address}}</td>
      <td>
        
        </td>
    </tr>
  </tbody>
</table>
        </div>
        <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
            <table class="table">
  <thead>
    <tr>

        <th scope="col">Name</th>
        <th scope="col">Address</th>
    </tr>
  </thead>
  <tbody>
    <tr class="table-style" v-for="item in rejected" :key="item">

      <td>{{item.CustomerName}}</td>
      <td>{{item.Address}}</td>
      <td>
       
        </td>
    </tr>
  </tbody>
</table>
        </div>
        </div>
    </div>
</template>

<script>

export default {
name: 'ViewBooking',
    components: {
    },
    data(){
        return{
            //update the array accordingly
            pending:  [{'Address':'123','CustomerName':'john'},{'Address':'456','CustomerName':'peter'}],
            accepted: [{'Address':'123','CustomerName':'ben'},{'Address':'456','CustomerName':'peter'}],
            rejected: [{'Address':'123','CustomerName':'ben'},{'Address':'456','CustomerName':'john'}],
        }
    },
    methods: {
        increment_pending(){
            this.num_pending += 1 
        },
        increment_accepted(){
            this.num_accepted++
        },
        increment_rejected(){
            this.num_rejected++
        }
    }
}

</script>

<style>
    #bookingtemplate{
        border: rgba(36,63,90,255) 5px solid;
        width: 80%;
        height: 100vh;
        margin: auto;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    #pending-tab{
        background-color: aqua;
    }
    #accepted-tab {
        background-color: greenyellow;
    }
    #rejected-tab {
        background-color: red;
        color: black;
    }
    .table-style{
        background-color: antiquewhite;
    }
    .bookingbutton{
        width: 30%;
    }
   
   
</style>
