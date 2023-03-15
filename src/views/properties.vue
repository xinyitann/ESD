<template>
    <div>

    <div class="container">
        <div class="row">
            <div class="col-md-6"></div>
            <div class="col-md-6"></div>
        </div>
    </div>
    <div class="container">
        <div class="row">
            <div class="col-md-4"></div>
            <div class="col-md-4">
                <h1 class="text-center align-content-center" style="padding-bottom: 10px;padding-top: 10px;margin-top: 16px;margin-bottom: 20px;">All Properties&nbsp;</h1>
            </div>
            <div class="col-md-4"></div>
        </div>
    </div>

    <!-- search bar-->
    <div class="container " style="position: sticky;overflow: visible;">
        <div class="row justify-content-center" style="border-bottom-color: var(--bs-pink);box-shadow: 0px 0px 0px;text-align: center;">
            <div class="col-4 col-md-3 col-xl-6"><input type="search" placeholder="Search">
                <div class="btn-group"><button class="btn btn-light" type="button">Property</button><button class="btn btn-light dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false" type="button"></button>
                    <div class="dropdown-menu"><a class="dropdown-item" href="#">Condo</a><a class="dropdown-item" href="#">HDB</a><a class="dropdown-item" href="#">Landed</a></div>
                </div>
                <div class="btn-group"><button class="btn btn-light" type="button">Price</button><button class="btn btn-light dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false" type="button"></button>
                    <div class="dropdown-menu"><a class="dropdown-item" href="#">First Item</a><a class="dropdown-item" href="#">Second Item</a><a class="dropdown-item" href="#">Third Item</a></div>
                </div>
                <div class="btn-group"><button class="btn btn-light" type="button">Bedroom</button><button class="btn btn-light dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false" type="button"></button>
                    <div class="dropdown-menu"><a class="dropdown-item" href="#">First Item</a><a class="dropdown-item" href="#">Second Item</a><a class="dropdown-item" href="#">Third Item</a></div>
                </div>
            </div>
        </div>
    </div>

    <div class="container py-4 py-xl-5">
        <div class="row gy-4 row-cols-1 row-cols-xl-3 text-start justify-content-center">
            <div class="col-xl-9">
                <div class="card">
                    <div class="card-body shadow " style="padding-top: 0px;padding-left: 0px;padding-right: 0px;">
                        <div class="carousel slide" data-bs-ride="false" id="carousel-1">
                            <div class="carousel-inner">
                                <div class="carousel-item active"><img class="w-100 d-block fit-cover" src="../assets/room2.jpg" alt="Slide Image" ></div>
                                <div class="carousel-item"><img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image"></div>
                                <div class="carousel-item"><img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image"></div>
                            </div>
                            <div><a class="carousel-control-prev" href="#carousel-1" role="button" data-bs-slide="prev"><span class="carousel-control-prev-icon"></span><span class="visually-hidden">Previous</span></a><a class="carousel-control-next" href="#carousel-1" role="button" data-bs-slide="next"><span class="carousel-control-next-icon"></span><span class="visually-hidden">Next</span></a></div>
                            <ol class="carousel-indicators">
                                <li data-bs-target="#carousel-1" data-bs-slide-to="0" class="active"></li>
                                <li data-bs-target="#carousel-1" data-bs-slide-to="1"></li>
                                <li data-bs-target="#carousel-1" data-bs-slide-to="2"></li>
                            </ol>
                        </div>
                        <br>
                        <div class="card-body p-4">
                            <h5 class="card-text">Blk 345<br>Halloween Avenue 6<br>Singapore 672044</h5>
                            <h5 class="card-text">1216 sqft</h5>
                            <h5 class="card-text">$600,000</h5>
                            <h5 class="card-text text-end">Bidding in progress</h5>
                            <router-link to="/propertyDetails">
                             <a class="btn btn-light float-end" type="button" style="background-color: #447098; color: white;" >View Details</a>
                            </router-link>
                        </div>
                        <!-- <div class="d-flex"><img class="rounded-circle flex-shrink-0 me-3 fit-cover" width="50" height="50" src="https://cdn.bootstrapstudio.io/placeholders/1400x800.png">
                            <div>
                                <p class="fw-bold mb-0">John Smith</p>
                                <p class="text-muted mb-0">Erat netus</p>
                            </div>
                        </div> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
</template>

<script>

export default {
name: 'PropertiesPage',
    components: {
    },
}

</script>

<style>

</style>