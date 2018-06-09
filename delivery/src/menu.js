import Vue from 'vue'
import axios from 'axios'

Vue.filter('media', function(value){
    return '/media/'+value;
})

Vue.filter('bgimage', function(value){
    return `background: url('/media/${value}') center center`
})

Vue.filter('concat', (value, string) => {
    return `${string}${value}`
})

let food_item = Vue.component('food-item',{
    props:['food'],
    template:`
    <div class="food-item">
        <div class="row">
            <div class="col-xs-12 col-sm-12 col-lg-8">
                <div class="rest-logo pull-left">
                    <img v-bind:src="food.pic" class="restaurant-logo pull-left" alt="Food logo">
                </div>
                <div class="rest-descr">
                    <h6>
                        {{food.name}}
                    </h6>
                    <p> {{food.description}}</p>
                </div>
            </div>
            <div class="col-xs-12 col-sm-12 col-lg-4 pull-right item-cart-info">
                <span class="price pull-left">N {{food.price}}</span>
                <a href="#" class="btn btn-small btn btn-secondary pull-right" data-target="">&#43;</a>
            </div>
        </div>
    </div>
    `
})

let category_item = Vue.component('category-item', {
    props:['category'],
    template:`
        <div class="card">
            <div class="card-header" id="category.id | concat(heading)">
                <h5 class="mb-0">
                    <button class="btn btn-link" type="button" data-toggle="collapse" data-target="category.id | concat(#collapse)" aria-expanded="true" aria-controls="category.id | concat(collapse)">
                        {{category.name}}
                    </button>
                </h5>
            </div>
            <div id="category.id | concat(collapse)" class="collapse show" aria-labelledby="category.id | concat(heading)" data-parent="#menuAccordion">
                <slot></slot>
            </div>
        </div>
    `,
    
})

let menu_app = new Vue({
    el:'#menu-page',
    components:{
        category_item:category_item
    },
    data:{
        categories:[],
    },
    created(){
        this.getCategories();
    },    
    methods:{
        getCategories: function(){
            let vm = this
            let restaurant_id = document.querySelector('#restaurant_id').innerText
            let url = `/api/menus/restaurant/${restaurant_id}/categories`
            axios.get(url)
            .then(function(response){
                vm.categories = response.data
                console.log(response.data)
            })
            .catch(function (error) {
                console.log(error);
            });
        },
    }

})