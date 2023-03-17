<template>
    <div id="login_main">
        <div id="login">
        <img id="loginimg" src="../assets/Haven.png" alt="">

        <form>
  <!-- Email input -->
  <div id="login-form">
  <div class="form-outline mb-4">
    <input type="email" id="idinput" class="form-control" />
    <label class="form-label" for="form2Example1">ID</label>
  </div>

  <!-- Password input -->
  <div class="form-outline mb-4">
    <input type="password" id="password_input" class="form-control" />
    <label class="form-label" for="form2Example2">Password</label>
  </div>

  <!-- 2 column grid layout for inline styling -->
  <div class="row mb-4">
    <div class="col d-flex justify-content-center">
      <!-- Checkbox -->
      <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="form2Example31" checked />
        <label class="form-check-label" for="form2Example31"> Remember me </label>
      </div>
    </div>

    <div class="col">
      <!-- Simple link -->
      <a href="#!">Forgot password?</a>
    </div>
  </div>

  <!-- Submit button -->
  <button type="button"  class="btn btn-primary btn-block mb-4" @click="redirectUser();sethost()">Sign in</button>


 
  </div>
</form>
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
        margin-top: 50px;
        position: absolute;
        bottom: 0;
        top: 0;
        width: 100%;
        background-image: url(../assets/loginbackground.jpg);
        background-size: cover;
    }
    #login{
        margin-top: 70px;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
        font-family: sans-serif;
        color: white;
        border: solid white 3px;
        padding: 20px;
        background-color:  rgba(36,63,90,255);
        opacity: 0.9;
    }

    form {
        
            margin-left: 25%;
            margin-right:25%;
            width: 50%;
    }

    #loginimg{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 40%;
    }
   
</style>
