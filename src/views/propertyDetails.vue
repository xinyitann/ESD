<template>
    <div>

        <!--Carousel room images-->
        <div class="carousel slide" data-bs-ride="false" id="carousel-1">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
                <div class="carousel-item">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
                <div class="carousel-item">
                    <img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image" width="1393" height="525">
                </div>
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
                <h3 class="mb-3">Property Name</h3>
                <p class="fs-5">$47294423</p>
                <hr>
                <table class="table table-borderless">
                    <tr>
                        <th>
                            Address
                        </th>
                        <td>
                            Block 345 Halloween Avenue 6 #06-249
                        </td>
                    </tr>
                    <tr>
                        <th>
                            Postal Code
                        </th>
                        <td>
                            349345
                        </td>
                    </tr>
                    <tr>
                        <th>
                            Neighbourhood
                        </th>
                        <td>
                            Halloween
                        </td>
                    </tr>
                    <tr>
                        <th>
                            Property Type
                        </th>
                        <td>
                            HDB
                        </td>
                    </tr>
                    <tr>
                        <th>
                            Square Feet
                        </th>
                        <td>
                            10000
                        </td>
                    </tr>
                    <tr>
                        <th>
                            Number of Rooms
                        </th>
                        <td>
                            10
                        </td>
                    </tr>
                    <tr>
                        <th>
                            House Facing Direction
                        </th>
                        <td>
                            North
                        </td>
                    </tr>
                    <tr>
                        <th>
                            Build Year
                        </th>
                        <td>
                            10000
                        </td>
                    </tr>
                </table>
            </div>
            <div class="col-12 col-md-5">
                <div class="card p-3">
                    <h5 class="card-title text-center my-2">Interested?</h5>
                    <div class="card-body">
                        <p>
                            Contact Jonah @ +65 12345678 / jonah@gmail.com
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
                <div class="my-5">
                    <div class="row mb-3">
                        <div class="col">
                            <p class="text-center fw-bold">
                                $13771
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">Minimum Bid</small>
                            </p>
                        </div>
                        <div class="col">
                            <p class="text-center fw-bold">
                                $13771
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">My Current Bid</small>
                            </p>
                        </div>
                        <div class="col">
                            <p class="text-center fw-bold">
                                $13771
                            </p>
                            <p class="d-flex justify-content-center">
                                <small class="text-body-secondary">Highest Bid</small>
                            </p>
                        </div>
                    </div>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" placeholder="Enter your bid" aria-label="Enter your bid" aria-describedby="button-addon1">
                        <button class="btn" type="button" style="background-color: #447098; color: white;" id="button-addon">Place Bid</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

        <!-- <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <div class="row">
                        <div class="col-xxl-8">
                            <div class="card border-light">
                                <div class="card-body" style="background: var(--bs-white);border-style: none;">
                                    <h4 class="text-center card-title">$600,000</h4>
                                </div>
                            </div>
                            <p>Squarefeet : 1216 sqft</p>
                            <p>Room : 3 bedrooms, 2 toilets</p>
                            <p>Address :&nbsp;Blk 345<br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Halloween Avenue 6<br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Singapore 672044</p>
                            <p>Build Year : 1995</p>
                        </div>
                        <div class="col"></div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <div class="card border-light"></div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="row">
                        <div class="col"></div>
                        <div class="col-xxl-8">
                            <div class="card border-light">

                                <div class="card-body" style="background: var(--bs-gray-100);">
                                    <h4 class="text-center card-title">Jonah</h4>
                                    <div class="row">
                                        <div class="col d-xxl-flex justify-content-xxl-center align-items-xxl-center" style="text-align: center;">
                                            <p class="fs-5">Contact Information&nbsp;</p>
                                        </div>
                                        <div class="col">
                                            <p style="text-align: center;">+65 12345678&nbsp;</p>
                                            <p style="text-align: center;">hello@gmail.com&nbsp;</p>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col"></div>
                                        <div class="col-xxl-6 d-xxl-flex justify-content-xxl-center align-items-xxl-center">
                                            <router-link to="/bookingnow">
                                            <a class="btn btn-danger float-start" type="button">Book Appointment</a>
                                        </router-link></div>
                                            
                                        <div class="col"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col"></div>
                        <div class="col-xxl-8">
                            <div class="card border-light">

                                <div class="card-body">
                                    <h4 class="text-center card-title">Bidding Details&nbsp;</h4>
                                    <p class="d-xxl-flex justify-content-xxl-center card-text">5 days 3 hrs / Sunday 10 pm / 7 bids / $ 900,000</p>
                                    <div class="row">
                                        <div class="col"></div>
                                        <div class="input-group"><input class="form-control" type="text" placeholder="Enter your bid" fdprocessedid="4gn2t1a"><button class="btn " type="button" fdprocessedid="82x11p" style="background-color: #447098; color: white;" >Place Bid</button></div>
                                        <div class="col"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div> -->
</template>

<script>

export default {
name: 'PropertyDetailsPage',
    components: {
    },
}

</script>

<style>

</style>