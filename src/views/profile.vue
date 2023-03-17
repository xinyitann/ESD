<template>
    <div id="main">
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
    
        
    </div>
</template>

<script>
export default {
name: 'UserProfile',
    components: {
    },
    methods: {
     dosomething(){
        console.log(this.$hostname)
     }
            }
}

</script>

<style>
   
    #userprofileimg {
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
    }
</style>
