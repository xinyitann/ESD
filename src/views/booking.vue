<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
            <div class="col-10 col-md-8 col-lg-7 my-3">
                <h2 class="text-center my-2">Book Appointment</h2>
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
                        <label for="bookingDate" class="form-label">Select a Date</label>
                        <input type="date" class="form-control" id="bookingDate" v-model="bookingDate">
                    </div>
                    <div class="mb-3">
                        <label for="bookingTime" class="form-label">Select a Time</label>
                        <select class="form-select" id="bookingTime" v-model="bookingTime">
                            <option selected>hh:mm - hh:mm</option>
                            <option value="0900-1000">09:00 - 10:00</option>
                            <option value="1000-1100">10:00 - 11:00</option>
                            <option value="1100- 1200">11:00 - 12:00</option>
                            <option value="1200-1300">12:00 - 13:00</option>
                            <option value="1300-1400">13:00 - 14:00</option>
                            <option value="1400- 1500">14:00 - 15:00</option>
                            <option value="1500-1600">15:00 - 16:00</option>
                            <option value="1600-1700">16:00 - 17:00</option>
                            <option value="1700- 1800">17:00 - 18:00</option>
                            <option value="1800-1900">18:00 - 19:00</option>
                            <option value="1900-2000">19:00 - 20:00</option>
                        </select>
                    </div>
                    <div class="d-flex justify-content-around">
                        <button type="submit" class="btn" style="background-color: #6d8363; color: white;">Cancel</button>
                        <button type="submit" class="btn" style="background-color: #447098; color: white;">Submit</button>
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
            bookingTime:"",
        }
    }
}

</script>

<style scoped>

</style>