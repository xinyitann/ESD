<template>
    <footer class="container-fluid text-white bg-blue">
        <div class="row p-5 justify-content-center">

        <div class="col-12 col-sm-6 col-md-3 gx-0">
            <h4 class="fw-bold">Haven</h4>
            <p class="text-gray-100 opacity-75">
            Designed and built by the Haven team for you to purchase your dream home easily
            </p>
            <div>
            <router-link to="#instagram" class="me-3">
                <i
                class="bi bi-instagram text-light footer-icon"
                style="font-size: 1.4rem"
                ></i>
            </router-link>
            <router-link to="#facebook" class="me-3">
                <i
                class="bi bi-facebook text-light footer-icon"
                style="font-size: 1.4rem"
                ></i>
            </router-link>
            <router-link to="#twitter">
                <i
                class="bi bi-twitter text-light footer-icon"
                style="font-size: 1.4rem"
                ></i>
            </router-link>
            </div>
        </div>

        <!-- Company Section -->
        <div
            class="col-12 col-sm-6 col-md-3 col-lg-2 offset-md-1 gy-5 gy-sm-0 gx-0 gx-sm-5 gx-md-0"
        >
            <h5 class="fw-bold">Company</h5>
            <hr
            class="opacity-100"
            style="width: 65px; border: 1px solid #6d8363; border-radius: 10px"
            />

            <ul class="list-unstyled mb-3">
            <li class="my-2">
                <router-link
                to="/aboutus"
                class="opacity-75 text-white text-decoration-none footer-link"
                >About Us</router-link
                >
            </li>
            <li class="my-2">
                <router-link
                to="/PageNotFound"
                class="opacity-75 text-white text-decoration-none footer-link"
                >Our Team</router-link
                >
            </li>
            <li class="my-2">
                <router-link
                to="/PageNotFound"
                class="opacity-75 text-white text-decoration-none footer-link"
                >Careers</router-link
                >
            </li>
            </ul>
        </div>

        <!-- Links Section -->
        <div class="col-12 col-sm-6 col-md-3 col-lg-2 gy-4 gy-md-0 gx-0">
            <h5 class="fw-bold">Links</h5>
            <hr
            class="opacity-100"
            style="width: 65px; border: 1px solid #6d8363; border-radius: 10px"
            />
            <ul class="list-unstyled mb-3">
            <li class="my-2">
                <router-link
                to="/properties"
                class="opacity-75 text-white text-decoration-none footer-link"
                >All Properties</router-link
                >
            </li>
            <li class="my-2">
                <router-link
                to="/booknow"
                class="opacity-75 text-white text-decoration-none footer-link"
                >Book An Appointment</router-link
                >
            </li>
            <li class="my-2">
                <router-link
                to="/viewbooking"
                class="opacity-75 text-white text-decoration-none footer-link"
                >My Bookings</router-link
                >
            </li>
            </ul>
        </div>

        <!-- Support Section -->
        <div class="col-12 col-sm-6 col-md-2 gy-4 gy-md-0 gx-0 gx-sm-5 gx-md-0">
            <h5 class="fw-bold">Support</h5>
            <hr
            class="opacity-100"
            style="width: 65px; border: 1px solid #6d8363; border-radius: 10px"
            />

            <ul class="list-unstyled mb-3">
            <li class="my-2">
                <router-link
                to="/PageNotFound"
                class="opacity-75 text-white text-decoration-none footer-link"
                >24/7 Support</router-link
                >
            </li>
            <li class="my-2">
                <router-link
                to="/PageNotFound"
                class="opacity-75 text-white text-decoration-none footer-link"
                >Community</router-link
                >
            </li>
            <li class="my-2">
                <router-link
                to="/PageNotFound"
                class="opacity-75 text-white text-decoration-none footer-link"
                >Events</router-link
                >
            </li>
            </ul>
        </div>
        <div class="col-0 col-lg-2"></div>
        </div>

        <!-- Company Description -->
        <div class="row py-5 d-flex border-top border-light mx-4">
        <div
            class="col-12 col-md-6 order-2 order-md-1 p-0 d-flex justify-content-start align-items-center"
        >
            <span class="opacity-75"
            >© {{ new Date().getFullYear() }} Haven All rights
            reserved.</span
            >
        </div>
        <div
            class="col-12 col-md-6 order-1 order-md-2 p-0 d-flex justify-content-start justify-content-md-end mb-2 mb-md-0"
        >
            <div class="d-flex justify-content-between">
            <router-link
                to="/PageNotFound"
                class="opacity-75 text-white footer-link text-decoration-none me-3"
                >Terms of Service</router-link
            >
            <router-link
                to="/PageNotFound"
                class="opacity-75 text-white footer-link text-decoration-none"
                >Privacy Policy</router-link
            >
            </div>
        </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'FooterComponent',
        components: {
        },
}
</script>

<style scoped>
.bg-blue {
    background-color: #243F5A;
}
.footer-link:hover {
color: #447098 !important;
opacity: 1 !important;
}

.footer-icon:hover {
color: #447098 !important;
transition: all 0.2s;
}
</style>