<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
            <div class="col-10 col-md-8 col-lg-7 my-3">
                <h2 class="text-center my-4">Book An Appointment</h2>
                <form>
                    <div class="mb-3">
                        <label for="customerID" class="form-label">Customer ID</label>
                        <input type="text" class="form-control" id="customerID" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="agentID" class="form-label">Agent ID</label>
                        <input type="text" class="form-control" id="agentID" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="propertyID" class="form-label">Property ID</label>
                        <input type="text" class="form-control" id="propertyID" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="bookingDate" class="form-label">Select a Date*</label>
                        <input type="date" class="form-control" id="bookingDate" v-model="bookingDate">
                    </div>
                    <div class="mb-3">
                        <label for="bookingStartTime" class="form-label">Select Start Time*</label>
                        <select class="form-select" id="bookingStartTime" v-model="bookingStartTime">
                            <option selected>hh:mm</option>
                            <option value="0900">09:00</option>
                            <option value="1000">10:00</option>
                            <option value="1100">11:00</option>
                            <option value="1200">12:00</option>
                            <option value="1300">13:00</option>
                            <option value="1400">14:00</option>
                            <option value="1500">15:00</option>
                            <option value="1600">16:00</option>
                            <option value="1700">17:00</option>
                            <option value="1800">18:00</option>
                            <option value="1900">19:00</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="bookingEndTime" class="form-label">Select End Time*</label>
                        <select class="form-select" id="bookingEndTime" v-model="bookingEndTime">
                            <option selected>hh:mm</option>
                            <option value="1000">10:00</option>
                            <option value="1100">11:00</option>
                            <option value="1200">12:00</option>
                            <option value="1300">13:00</option>
                            <option value="1400">14:00</option>
                            <option value="1500">15:00</option>
                            <option value="1600">16:00</option>
                            <option value="1700">17:00</option>
                            <option value="1800">18:00</option>
                            <option value="1900">19:00</option>
                            <option value="2000">20:00</option>
                        </select>
                    </div>
                    <div class="d-flex justify-content-around">
                        <router-link to="/">
                            <button type="submit" class="btn" style="background-color: #6d8363; color: white;">Cancel</button>
                        </router-link>
                        <button type="submit" class="btn" style="background-color: #447098; color: white;">Book Now</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

export default {
name: 'BookingPage',
    components: {
    },
    
    data(){
        return{
            customerID:"123",
            agentID: "456",
            propertyID: "789",
            bookingDate:"",
            bookingStartTime:"",
        }
    }
}

</script>

<style scoped>

</style>