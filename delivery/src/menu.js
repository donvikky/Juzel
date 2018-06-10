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
                <a href="#" class="btn btn-small btn btn-secondary pull-right" data-target="" @click="addToCart">&#43;</a>
            </div>
        </div>
    </div>
    `,
    methods:{
        addToCart: function(evt){
            //let token = document.querySelector('#token').innerText
            //let csrf = document.querySelector('input').value
            //alert(csrf)
            
            let data = {
                id: this.food.id,
                name: this.food.name,
                price:this.food.price,
                qty: 1
            }
            let vm = this
            axios.post('/restaurant/add-to-cart/', data)
            .then((response)=>{
                //alert(response.data)
                vm.$emit('get-orders')
            })
            .catch((error) => {
                console.log(error)
            })
            //location.reload(true)
            evt.preventDefault();
            evt.stopPropagation();                       
        }
    }
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

let order_item = Vue.component('order-item', {
    props:['order'],
    template:`
        <div class="order-row">
            <div class="widget-body">
                <div class="title-row">{{order.name}}
                    <a data-target=''>
                        <a data-target='' @click="$emit('remove-item', order.id)"><i class="fa fa-trash pull-right"></i></a>
                    </a>
                </div>
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <label class="input-group-text" for="quantitySelect02">Quantity:</label>
                    </div>
                    <select class="custom-select" id="quantitySelect02">
                        <option selected>{{order.qty}}</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                    </select>
                </div>
                <h6>N {{order.price * order.qty}}</h6>
            </div>
        </div>
    `,
    
})

let menu_app = new Vue({
    el:'#menu-page',
    components:{
        category_item:category_item,
        order_item:order_item
    },
    data:{
        categories:[],
        orders:[],
    },
    created(){
        this.getCategories();
        this.getOrders();
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
        clearCart: function(){
            axios.get('/restaurant/empty-cart')
            .then((response) =>{
                this.orders = [];
            })
        },
        removeItem: function(item_id){
            //remove selected item from cart           
            
            axios.post('/restaurant/remove-item/',{
                id:item_id
            })
            .then((response) => {
                //console.log(response.data)
                this.getOrders()
                //location.reload(true)
            })
            .catch((error) => {
                console.log(error)
            })
        },
        getOrders: function(){
            let vm = this
            axios.get('/restaurant/get-orders')
            .then((response) => {
                //console.log(response.data)
                vm.orders = response.data
            })
            .catch((error) => {
                console.log(error)
            })
        }        
    },
    computed: {
        grandTotal: function(){
            let total = 0.0
            if (this.orders.length > 0){
                this.orders.forEach((order) => {
                    let cost = order.price * order.qty
                    total += cost
                })
                return total
            }else{
                return 0.00
            }
        }
    }

})