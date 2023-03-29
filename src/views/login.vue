<template>
  <div id="login_main" class="row" style="margin-right:0px">
    <div id="login" class="col-11 col-sm-8 col-md-6 mx-auto my-1 py-3">
      <div>
        <img id="loginimg" src="../assets/Haven.png" alt="">
        <form class="mx-3 pb-0">
          <!-- Email input -->
          <div id="login-form">
            <div class="form-outline mb-4">
              <label class="form-label" for="form2Example1">Email Address</label>
              <input type="email" placeholder="Enter your email address" id="idinput" class="form-control" />
            </div>

            <!-- Password input -->
            <div class="form-outline mb-4">
              <label class="form-label" for="form2Example2">Password</label>
              <input type="password" placeholder="Enter your password" id="password_input" class="form-control" />
            </div>

            <!-- 2 column grid layout for inline styling -->
            <div class="row mb-4">
              <div class="col d-flex justify-content-center">
                <!-- Checkbox -->
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="form2Example31" checked />
                  <label class="form-check-label" for="form2Example31" style="font-size:small;">Remember me</label>
                </div>
              </div>

              <div class="col">
                <!-- Simple link -->
                <a href="#!" style="font-size: small; color: white;">Forgot password?</a>
              </div>
            </div>

            <!-- Submit button -->
            <div class="d-flex justify-content-center">
              <button type="button" style="background-color:#6d8363; color:white;" class="btn form-control" @click="redirectUser();sethost()">Log In</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'LoginPage',
  components: {

  },
  methods: {

    redirectUser () {
      //route to agent
      if (document.getElementById('password_input').value == 1234) {
        this.$router.push('/')
        // route to user
      } else if (document.getElementById('password_input').value == 123) {
        this.$router.push('/')
      }
    }
  }
}

</script>

<style>
    
#login_main{
  padding: 50px;
  background-image: url(../assets/loginBg.jpg);
  background-size: cover;
  height: 100vh
}
#login{
  color: white;
  background-color:  #243F5A;
  opacity: 95%;
  border-radius: 10px;
}

#loginimg{
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 40%;
}

</style>
