<template>
    <div class="container-fluid">
        <div class = "row d-flex justify-content-center">
            <div class="col-10 col-md-8 col-lg-7 my-3">
                <h2 class="text-center my-4">Make Payment</h2>
                <h5 class="my-4">Checkout using a credit card</h5>

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
                

                <div class="d-flex justify-content-around my-5">
                    <router-link to="/"> <!--depends on where was the user-->
                        <button type="button" class="btn" style="background-color: #6d8363; color: white;">Cancel</button>
                    </router-link>
                    <button type="submit" class="btn" style="background-color: #447098; color: white;">Pay Now</button>
                </div>

                <div style="position: relative; width: 100%;">
                  <hr class="my-4" style="border-top: 1px solid #ccc;">
                  <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background-color: white; padding: 0 10px;">OR</div>
                </div>
                <div style="text-align: center;">
                  <div ref="paypal"></div>
                </div>
                
            </div>
        </div>
    </div>
</template>


<script>

export default {
  name: 'PaymentPage',
  components: {},
  data() {
    return {
        
        totalBill: 0,
        cardholderName: "",
        cardNumber: "",
        expiration: "",
        cvv: "",
        postalCode: "",
        auction_id:[],
        product:[]
    };
  },
  mounted: function() {
    const CLIENT_ID = process.env.VUE_APP_PAYPAL_CLIENT_ID ;
    const script = document.createElement("script");
    script.src =
      "https://www.paypal.com/sdk/js?client-id=" + CLIENT_ID;
    script.addEventListener("load", this.setLoaded);
    document.body.appendChild(script);
  },
  created() {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Access-Control-Allow-Origin", "*");

    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };
    fetch(`http://127.0.0.1:5002/auctions/option_fee/${this.auction_id}`,requestOptions)
      .then(response => response.json())
      .then(data => {
        this.product = data;
      });
  },
  
  methods: {
    setLoaded: function() {
      this.loaded = true;
      window.paypal
        .Buttons({
          createOrder: (data, actions) => {
            return actions.order.create({
              purchase_units: [
                {
                  description: this.product.description,
                  amount: {
                    currency_code: "USD",
                    value: this.product.price
                  }
                }
              ]
            });
          },
          onApprove: async (data, actions) => {
            const order = await actions.order.capture();
            this.paidFor = true;
            console.log(order);
          },
          onError: err => {
            console.log(err);
          }
        })
        .render(this.$refs.paypal);
    }
  }
};
</script>


<style>

</style>
