<template>
    <div id="backgroundhome">
    <div class="container">
        <div class="center">
            <span style="font-size: 40px;color:white">Reimagine Home</span> 
            <br>
            we will help you to find the place you love.
            <br>
            <br>
            <input type="text" placeholder="search for a location">
        </div>
    </div>
        
        
   
    </div>
   
    
    
</template>

<script>

export default {
name: 'HomePage',
    components: {
    },
}

</script>

<style>
    #homeinfo{
        padding: 30px;
        text-align: center;
        font-family: sans-serif;
    }
    #homeimg{
        margin: auto;
        display: block;
        width: 100%;
        height:600px;
        margin-bottom: 50px;
    }
    #backgroundhome{
        color: white;
        background-image: url('../assets/backgroundhome.jpg');
        height: 100vh;
        background-repeat: no-repeat;
        background-size: cover;
    }
    .container {
        height: 100vh;
        position: relative;
    }

    .center {
        position: absolute;
        top: 50%;
        left: 50%;
        text-align: center;
        transform: translate(-50%,-50%);
        opacity: 0.9;
        padding-top: 30px;
        padding-bottom: 30px;
        padding-left: 70px;
        padding-right: 70px;
        font-family: sans-serif;
        width:60%;
        background-color: blueviolet;
        border-radius: 20px;
    }
</style>
