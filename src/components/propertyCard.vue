<template>
    <div class="col-12 col-sm-6 col-md-4 col-xl-3 p-4">
        <div class="card">
            <div class="card-body shadow " style="padding-top: 0px;padding-left: 0px;padding-right: 0px;">
                <div class="carousel slide" data-bs-ride="false" :id="carouselIdStr">
                    <div class="carousel-inner">
                        <div class="carousel-item active"><img class="w-100 d-block fit-cover" :src=getimage(property_image) alt="Slide Image" ></div>
                        <!-- <div class="carousel-item"><img class="w-100 d-block" v-bind:src=getimage(property_image) alt="Slide Image"></div> -->
                        <!-- <div class="carousel-item"><img class="w-100 d-block" src="../assets/room2.jpg" alt="Slide Image"></div> -->
                    </div>
                    <div>
                        <a class="carousel-control-prev" :href="carouselHrefStr" role="button" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon"></span>
                            <span class="visually-hidden">Previous</span>
                        </a>
                        <a class="carousel-control-next" :href="carouselHrefStr" role="button" data-bs-slide="next">
                            <span class="carousel-control-next-icon"></span>
                            <span class="visually-hidden">Next</span>
                        </a>
                    </div>
                    <ol class="carousel-indicators">
                        <li :data-bs-target="carouselHrefStr" data-bs-slide-to="0" class="active"></li>
                        <!-- <li :data-bs-target="carouselHrefStr" data-bs-slide-to="1"></li>
                        <li :data-bs-target="carouselHrefStr" data-bs-slide-to="2"></li> -->
                    </ol>
                </div>
                <div class="card-body p-4">
                    <h5 class="card-title my-3">{{ property_name }}</h5>
                    <p class="card-text">{{property_add}}</p>
                    <p class="card-text">{{property_image}}</p>
                    <p class="card-text">{{estimated_cost}}</p>
                   
                        <a class="btn btn-light float-end" type="button" style="background-color: #447098; color: white;" @click="submit_property_data()">
                            View Details
                        </a>
                </div>
                <!-- <div class="d-flex">
                    <img class="rounded-circle flex-shrink-0 me-3 fit-cover" width="50" height="50" src="https://cdn.bootstrapstudio.io/placeholders/1400x800.png">
                    <div>
                        <p class="fw-bold mb-0">John Smith</p>
                        <p class="text-muted mb-0">Erat netus</p>
                    </div>
                </div> -->
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PropertyCard',
    props: [
        'carouselNum',
        'property_name',
        'property_add',
        'estimated_cost',
        'property_image',
        'property_id_card',
],
    data(){ // or could put it in props
        return{
            carouselHrefStr:"#carousel-" + this.carouselNum,
            carouselIdStr: "carousel-" + this.carouselNum,
            imageSrc:'',
            imagename: "",
            imagename2: ""

        }
    },
    methods:{
    submit_property_data(){
        console.log('current_id:'+this.property_id_card)
      this.$emit('submit_property_data', this.property_id_card)
      this.$router.push('/propertydetails')

    },
    getimage(image){
        return require('@/assets/' + image)
    }
    // handleClick() {
    //   this.$emit('property-clicked', this.propertyId);
    // }
    },

    
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>


