<template>
  <nav class="navbar navbar-expand-lg bg-blue sticky-top" data-bs-theme="dark">
    <div class="container-fluid">
      <router-link to="/" class="nav-link">
        <img src="../assets/logo.jpg" class="w-50">
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation" style="color: white;">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarText">
        <ul class="navbar-nav me-2">
          <li v-if="user_type =='user'" class="nav-item mx-2">
            <router-link to="/properties" class="nav-link">Discover</router-link>
          </li>
          <li v-if="user_type != ''" class="nav-item mx-2">
            <router-link to="/mybooking" class="nav-link">My Bookings</router-link>
          </li>
          <li v-if="user_type=='user'" class="nav-item mx-2">
            <router-link to="/mybids" class="nav-link">My Bids</router-link>
          </li>
          <li v-if="user_type=='agent'" class="nav-item mx-2">
            <router-link to="/myproperty" class="nav-link">My Properties</router-link>
          </li>
          <li v-if="user_type==''" class="nav-item mx-2">
            <router-link to="/login" class="nav-link">Log In</router-link>
          </li>
          <li v-else class="nav-item mx-2">
            <router-link to="/profile" class="nav-link">Profile</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  props: [
      'user_type',
  ],
  data(){ 
    return{
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bg-blue {
  background-color: #243F5A;
}
</style>
