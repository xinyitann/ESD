<template>
    <div>
        <div id="bgPic">
            <div id="firstSectionOverlay" class="d-flex align-items-center justify-content-center">
                <div class="h-50 d-flex align-items-center text-white p-3">
                    <div>
                        <h1 class="text-center">Discover your dream home with Haven</h1>
                        <p class="text-center fs-5">The ultimate seamless and stress-free home buying experience</p>
                        <div class="d-flex justify-content-center my-5">
                            <button type="button" class="btn btn-lg" style="background-color: #6d8363; color: white;">
                                <router-link to="/properties" class="nav-link">Explore Now</router-link>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="py-5" style="height: 100vh;">
            <div class="my-5 mx-3">
                <h2 class="text-center">We make it easy for u</h2>
                <h5 class="text-center text-body-secondary mb-5">Follow these three simple steps to get your dream home</h5>
            </div>
            <div class="row w-100 pt-4">
                <div class="col-12 col-md-4">
                    <div class="d-flex justify-content-center" >
                        <img src="../assets/searchImg.png" class="w-25" >
                    </div>
                    <h5 class="text-center my-3">
                        Search for your ideal property
                    </h5>
                </div>
                <div class="col-12 col-md-4">
                    <div class="d-flex justify-content-center" >
                        <img src="../assets/bookImg.png" class="w-25" >
                    </div>
                    <h5 class="text-center my-3">
                        Schedule a viewing appointment
                    </h5>
                </div>
                <div class="col-12 col-md-4">
                    <div class="d-flex justify-content-center">
                        <img src="../assets/bidImg.png" class="w-25">
                    </div>
                    <h5 class="text-center my-3">
                        Place a bid to secure your dream home
                    </h5>
                </div>
            </div>
        </div>
    </div>
    <!-- <div id="backgroundhome">
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
    </div> -->
</template>

<script>
export default {
name: 'LandingPage',
    components: {
    },
}
</script>

<style>
#bgPic {
    background-image: url("../assets/backgroundImage.jpg");
    height: 100vh;
    width: 100%;
    background-repeat: no-repeat;
    background-size: cover;
    opacity: 95%;
}
#firstSectionOverlay {
    position: absolute;
    top:0;
    bottom:0;
    right:0;
    left: 0;
}
    /* #homeinfo{
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
        height: 100%;
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
    } */
</style>
