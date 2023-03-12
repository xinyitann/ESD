import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/landing.vue'
import LoginPage from '../views/login.vue'
import ProfilePage from '../views/profile.vue'
import PropertiesPage from '../views/properties.vue'
import PropertyDetailsPage from '../views/propertyDetails.vue'
import BookingPage from '../views/booking.vue'
import PaymentPage from '../views/payment.vue'
import ErrorPage from '../views/error.vue'

const routes = [
    {
        path: '/',
        name: 'Landing',
        component: LandingPage
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfilePage
    },
    {
        path: '/properties',
        name: 'Properties',
        component: PropertiesPage
    },
    {
        path: '/propertydetails',
        name: 'PropertyDetails',
        component: PropertyDetailsPage
    },
    {
        path: '/booking',
        name: 'Booking',
        component: BookingPage
    },
    {
        path: '/payment',
        name: 'Payment',
        component: PaymentPage
    },
    {
        path: "/:pathMatch(.*)*",
        name: "Error",
        component: ErrorPage,
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router