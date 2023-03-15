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
          <li class="nav-item mx-2">
            <router-link to="/properties" class="nav-link">Properties</router-link>
          </li>
          <li class="nav-item mx-2">
            <router-link to="/booking" class="nav-link">Booking</router-link>
          </li>
          <li class="nav-item mx-2">
            <router-link to="/profile" class="nav-link">
              <i class="bi bi-person-circle" style="font-size: 19px;"></i>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
  },
  data(){ // or could put it in props
    return{

    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bg-blue {
  background-color: #243F5A;
}
</style>
