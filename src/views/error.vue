<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12 col-md-6 d-flex justify-content-center">
                <img src="../assets/error.jpg" class="w-75"/>
            </div>
            <div class="col-12 col-md-6 d-flex justify-content-center align-items-center p-4">
                <div>
                    <h1>Oops!</h1>
                    <h3>Error 404 - Page not found</h3>
                    <p>The page you requested could not be found. We are working on it.</p>
                    <router-link to="/">
                        <button class="btn btn-primary">Back to Home</button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
name: 'ErrorPage',
    components: {
    },
}

</script>

<style>

</style>