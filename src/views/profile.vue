<template>
    <div style="height:100vh; background-color:#243F5A; margin-right:0px;" class="d-flex justify-content-center align-items-center row">
        <div class="col-6 p-5 rounded-3" style="background-color:white;">
            <div class="row pb-5">
                <div class="d-flex justify-content-end align-items-center col">
                    <img src="../assets/profile_image.jpg" style="border-radius:50%; height:100px; width: 100px;">
                </div>
                <div class="col d-flex justify-content-start align-items-center">
                    <h5>Full Name</h5>
                </div>
            </div>
            <div class="d-flex justify-content-center align-items-center">
                <div>
                    <table class="table table-borderless text-center">
                        <tr class="row">
                            <th class="col-5 d-flex align-items-center">
                                Phone number
                            </th>
                            <td v-if="editing==false" class="col-7">
                                +65 91234567
                            </td>
                            <td v-else class="col-7">
                                <input type="text" placeholder="CurrentPhoneNum" class="form-control">
                            </td>
                        </tr>
                        <tr class="row">
                            <th class="col-5 d-flex align-items-center">
                                Email Address
                            </th>
                            <td v-if="editing==false" class="col-7">
                                agentOrCustomer@gmail.com
                            </td>
                            <td v-else class="col-7 py-2">
                                <input type="email" placeholder="CurrentEmail" class="form-control">
                            </td>
                        </tr>
                    </table>
                    <div v-if="editing==false" class="d-flex justify-content-center">
                        <button class="btn mt-3" style="background-color: #447098; color: white;" @click="editDetails">Edit Details</button>
                    </div>
                    <div v-else class="d-flex justify-content-between">
                        <button class="btn mt-3" style="background-color: #6d8363; color: white;" @click="cancelEdit">Cancel</button>
                        <button  class="btn mt-3" style="background-color: #447098; color: white;" @click="editDetails">Confirm Change</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- <div id="main">
        <img id="userprofileimg" src="../assets/profile_image.jpg" alt="">
        <br>
        <div id="information">
        <div class="row">
            <div class="col-4 type">
                ID:
            </div>
            <div class="col-8 display">
                input ID
            </div>
        </div>
        <br>
        <div class="row">
            <div class="col-4 type">
                Email:
            </div>
            <div class="col-8 display">
                input Email
            </div>
        </div>
        <br>
        <div class="row">
            <div class="col-4 type">
                Name:
            </div>
            <div class="col-8 display">
                input Name 
            </div>
        </div>
        <br>
        <div class="row">
            <div class="col-4 type">
                Phone:
            </div>
            <div class="col-8 display">
                input Phone
            </div>
        </div>
        </div>
    
        
    </div> -->
</template>

<script>
export default {
    name: 'UserProfile',
    data(){
        return{
            editing: false,
        }
    },
    components: {
    },
    methods: {
        // dosomething(){
        //     console.log(this.$hostname)
        // }
        editDetails(){
            this.editing= true
        },
        cancelEdit(){
            this.editing=false
        }
    }
}

</script>

<style>

/* #userprofileimg {
    width: 20%;
    border-radius: 50%;
    margin-bottom: 20px;
}
#main {
    background-color: white;
    margin-left: auto;
    margin-right: auto;
    width: 70%;
    text-align: center;
    font-family: sans-serif;
    margin-top: 20px;
    border: rgba(36,63,90,255) solid 5px;
    padding-top: 20px;
    padding-bottom: 20px;
    margin-bottom: 20px;
}
#text_box{
    border: black solid 1px;
    margin: auto; 
    display: inline-block
}
#information{
    width: 70%;
    margin: auto;
}
.type{
    text-align: end;
}
.display {
    font-weight: 300;
    border: grey solid 1px;
    width: 45%;
} */
</style>
