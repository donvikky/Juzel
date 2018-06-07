import Vue from 'vue'

Vue.filter('media', function(value){
    return '/media/'+value;
})

Vue.filter('bgimage', function(value){
    return `background: url('/media/${value}') center center`
})

var top_meal = Vue.component('top-meal',{
    props:['menu'],
    template:`
    <div class="col-12 col-md-6 col-lg-4 food-item">
            <div class="food-item-wrap">
                <div class="figure-wrap bg-image" v-bind:style="menu.menu_image | bgimage">
                </div>
                <div class="content">
                    <h5>
                        <a href="menu.html" v-text="menu.food"></a>                                    
                    </h5>
                    <div class="product-name" v-text="menu.description"></div>
                    <div class="price-btn-block">
                        <span class="price" v-html="menu.price"></span>
                        <a href="#" class="btn theme-btn-outline float-right">Order Now</a>
                    </div>
                </div>
                <div class="restaurant-block">
                    <div class="left">
                        <a class="float-left" href="menu.html">
                            <img :src="menu.restaurant_logo | media" alt="Restaurant logo"> </a>
                        <div class="float-left right-text">
                            <a href="#" v-text="menu.restaurant"></a>
                            <span v-text="menu.restaurant_address"></span>
                        </div>
                    </div>
                    <div class="right-like-part float-right">
                        <i class="fa fa-heart-o"></i>
                        <span v-text="menu.likes"></span>
                    </div>
                </div>
            </div>
        </div>
    `,
    data(){
        return{
            likes:200,
        }
    }
})

var meal_app = new Vue({
    el:'#meal-app',
    components:{
        top_meal:top_meal,
    },
    data:{
        menus:[],
    },
    created: function(){ //once component is created, fetch menu items
        this.getMenus()
    },
    methods:{
        getMenus(){
            var vm = this; //this keyword will not work inside axios
            axios.get('/api/menus/')
            .then(function(response){
                vm.menus = response.data
                alert('before mount: '+ this.menus.length)
            })
            .catch(function(error){
                //alert('No menus could be loaded')
            })
        }
    }
})