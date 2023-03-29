<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
            <div class="col-10 col-md-8 col-lg-7 my-3">
                <h2 class="text-center my-4">Make Payment</h2>
                <h5 class="my-4">Payment Details</h5>
                <button type="button" class="btn btn-outline-secondary border-secondary-subtle border-1 w-100 p-3">
                    <img src="../assets/paypal.png" style="height:25px;">
                </button>

                <p class="my-4 fw-bold">or checkout using a credit card</p>

                <form class="border rounded-2 border-1 border-secondary-subtle p-4 w-100 ms-0 mb-5">
                    <div class="mb-3">
                        <label for="cardholderName" class="form-label">Cardholder Name</label>
                        <input type="text" class="form-control" id="cardholderName" v-model="cardholderName">
                    </div>
                    <div class="mb-3">
                        <label for="cardNumber" class="form-label">Card Number</label>
                        <input type="text" class="form-control" id="cardNumber" placeholder="4111 1111 1111 111" v-model="cardNumber">
                    </div>
                    <div class="row">
                        <div class="col-6">
                            <div class="mb-3">
                                <label for="expiration" class="form-label">Expiration</label>
                                <input type="text" class="form-control" id="expiration" placeholder="MM/YY" v-model="expiration">
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="mb-3">
                                <label for="cvv" class="form-label">CVV</label>
                                <input type="text" class="form-control" id="cvv" placeholder="123" v-model="cvv">
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="postalCode" class="form-label">Postal Code</label>
                        <input type="text" class="form-control" id="postalCode" placeholder="Postal or ZIP Code" v-model="postalCode">
                    </div>
                </form>

                <hr class="my-4">

                <div class="row mb-3">
                    <div class="col-6 fw-bold">
                        Total Bill
                    </div>
                    <div class="col-6 d-flex justify-content-end fw-bold">
                        ${{ totalBill }}
                    </div>
                </div>

                <div class="d-flex justify-content-around my-5">
                    <router-link to="/"> <!--depends on where was the user-->
                        <button type="button" class="btn" style="background-color: #6d8363; color: white;">Cancel</button>
                    </router-link>
                    <button type="submit" class="btn" style="background-color: #447098; color: white;">Pay Now</button>
                </div>
                
            </div>
        </div>
    </div>
</template>

<script>

export default {
name: 'PaymentPage',
    components: {
    },

    data(){
        return{
            totalBill:0,
            cardholderName:"",
            cardNumber:"",
            expiration:"",
            cvv: "",
            postalCode:"",
        }
    }
}

</script>

<style>

</style>