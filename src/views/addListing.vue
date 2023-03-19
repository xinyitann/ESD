<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
                <h2 class="text-center my-4">Add Listing</h2>
                <form>
                    <div class="row">
                        <div class="col-12 col-md-6 px-5">
                            <div class="mb-3">
                                <label for="address" class="form-label">Address*</label>
                                <input type="text" class="form-control" id="address">
                            </div>
                            <div class="mb-3">
                                <label for="PostalCode" class="form-label">Postal Code*</label>
                                <input type="text" class="form-control" id="PostalCode">
                            </div>
                            <div class="mb-3">
                                <label for="buildYear" class="form-label">Build Year*</label>
                                <input type="text" class="form-control" id="buildYear">
                            </div>
                            <div class="mb-3">
                                <label for="size" class="form-label">Size in Square Feet*</label>
                                <input type="text" class="form-control" id="size">
                            </div>
                            <div class="mb-3">
                                <label for="roomNo" class="form-label">Number of Rooms*</label>
                                <input type="number" class="form-control" id="roomNo">
                            </div>
                            <div class="mb-3">
                                <label for="bathroomNo" class="form-label">Number of Bathrooms*</label>
                                <input type="number" class="form-control" id="bathroomNo">
                            </div>
                        </div>
                        <div class="col-12 col-md-6 px-5">
                            <div class="mb-3">
                                <label for="estimatedCost" class="form-label">Estimated Cost*</label>
                                <input type="text" class="form-control" id="estimatedCost">
                            </div>
                            <div class="mb-3">
                                <label for="optionFee" class="form-label">Option Fee*</label>
                                <input type="text" class="form-control" id="optionFee">
                            </div>
                            <div class="mb-3">
                                <label for="minBidAmount" class="form-label">Minimum Bid Amount*</label>
                                <input type="text" class="form-control" id="minBidAmount">
                            </div>
                            <div class="mb-3">
                                <label for="startBidDate" class="form-label">Bidding Start Date*</label>
                                <input type="date" class="form-control" id="startBidDate" v-model="startBidDate">
                            </div>
                            <div class="mb-3">
                                <label for="bidEndDate" class="form-label">Bidding End Date*</label>
                                <input type="date" class="form-control" id="bidEndDate" v-model="bidEndDate">
                            </div>
                            <div class="mb-3">
                                <label for="images" class="form-label">Images*</label>
                                <input type="file" id="images" name="images" accept="image/*" class="form-control" multiple>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-center my-5">
                        <router-link to="/">
                            <button type="submit" class="btn mx-4" style="background-color: #6d8363; color: white;">Cancel</button>
                        </router-link>
                        <button type="submit" class="btn mx-4" style="background-color: #447098; color: white;">Add Listing</button>
                    </div>
                </form>
        </div>
    </div>
</template>

<script>

export default {
name: 'AddListingPage',
    components: {
    },
}

</script>

<style>

</style>