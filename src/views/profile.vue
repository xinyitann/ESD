<template>
    <div style="height:100vh; background-color:#243F5A; margin-right:0px;" class="d-flex justify-content-center align-items-center row">
        <div class="col-6 p-5 rounded-3" style="background-color:white;">
            <div class="row pb-5">
                <div class="d-flex justify-content-end align-items-center col">
                    <img src="../assets/profile_image.jpg" style="border-radius:50%; height:100px; width: 100px;">
                </div>
                <div class="col d-flex justify-content-start align-items-center">
                    <h5>{{information.name}}</h5>
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
                                {{ information.phone }}
                            </td>
                            <td v-else class="col-7">
                                <input v-model="newPhone" type="text" placeholder="New phone number" class="form-control">
                            </td>
                        </tr>
                        <tr class="row">
                            <th class="col-5 d-flex align-items-center">
                                Email Address
                            </th>
                            <td v-if="editing==false" class="col-7">
                                {{information.email}}
                            </td>
                            <td v-else class="col-7 py-2">
                                <input v-model="newEmail" type="email" placeholder="Input new email" class="form-control">
                            </td>
                        </tr>
                    </table>
                    <div v-if="editing==false" class="d-flex justify-content-center">
                        <button class="btn mt-3" style="background-color: #447098; color: white;" @click="editDetails">Edit Details</button>
                    </div>
                    <div v-else class="d-flex justify-content-between">
                        <button class="btn mt-3" style="background-color: #6d8363; color: white;" @click="cancelEdit">Cancel</button>
                        <button  class="btn mt-3" style="background-color: #447098; color: white;" @click="updateDetails">Confirm Change</button>
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
            information: [],
            newPhone: '',
            newEmail: '',
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
        },
        async updateDetails(){
            this.editing = false
            if(this.newPhone.length != 7){
                alert('invalid phone number')
            }
            if (this.newEmail.includes('email.com') || this.newEmail.includes('gmail.com') || this.newEmail.includes('yahoo.com')){
                if(this.user_type=='user'){
                    var myHeaders = new Headers();
                    myHeaders.append("Content-Type", "application/json");

                    var raw = JSON.stringify({
                    "email": this.newEmail,
                    "name": this.information.name,
                    "phone": this.newPhone
                    });
                    console.log(raw)

                    var requestOptions = {
                    method: 'PUT',
                    headers: myHeaders,
                    body: raw,
                    redirect: 'follow'
                    };
                    var URLL = "http://localhost:5003/agent/"+String(this.agent_id_prop)
                    await fetch(URLL, requestOptions)

                    this.information.phone = this.newPhone
                    this.newPhone = ''
                    this.information.email = this.newEmail
                    this.newEmail = ''
                 
                }
                else{
                    myHeaders = new Headers();
                    myHeaders.append("Content-Type", "application/json");

                    raw = JSON.stringify({
                    "email": this.newEmail,
                    "name": this.information.name,
                    "phone": this.newPhone
                    });

                    requestOptions = {
                    method: 'PUT',
                    headers: myHeaders,
                    body: raw,
                    redirect: 'follow'
                    };
                    URLL = "http://localhost:5700/customer/"+String(this.customer_id_prop)
                    await fetch(URLL, requestOptions)
                  
                    this.information.phone = this.newPhone
                    this.newPhone = ''
                    this.information.email = this.newEmail
                    this.newEmail = ''
                }
                
            }
            else{
                alert('invalid email')
            }
        }
    },
    props: [
        'customer_id_prop',
        'agent_id_prop',
        'user_type',
    ],
    async created() {
        console.log(this.customer_id_prop)
        console.log(this.agent_id_prop)
        console.log(this.user_type)
        if(this.user_type=='user'){
            var URLL = "http://127.0.0.1:5123/profile_page/" + String(this.agent_id_prop) + "/agent"
            var response1 = await fetch(URLL);
            var data = await response1.json(); 
        }
        else{
            URLL = "http://127.0.0.1:5123/profile_page/" + String(this.customer_id_prop) + "/user"
            response1 =await fetch(URLL) ;
            data = await response1.json(); 
        }
        data = data['data']
        console.log(data)
        if('agent_id' in data){
            data['user_id'] = data['agent_id']
            delete data['agent_id']
        }
        else{
            data['user_id'] = data['customer_id']
            delete data['customer_id']
        }
        this.information = data
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
