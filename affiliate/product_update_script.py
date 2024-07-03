# views.py
from django.shortcuts import render

def product_list(request):
    products = [
        {
            'image': 'affiliate/assets/pages/img/products/umi_stylish_look.jpg',
            'alt': 'UMI Stylish Table',
            'link': 'https://amzn.to/4choCwW',
            'name': 'Umi Stylish Look Round Wrought Iron Coffee Table Set of 2 (Golden)',
            'price': 'Rs. 3,751',
        },
        {
            'image': 'affiliate/assets/pages/img/products/dancing_candles.jpg',
            'alt': 'Berry Lace Dress',
            'link': 'https://amzn.to/3KASJ6u',
            'name': 'LTETTES LED Glass Cup Pillar Flameless Electric Candles with Flickering Faux Wick',
            'price': 'Rs. 1,777.00',
        },
        # Add more products here
    ]
    return render(request, 'your_template.html', {'products': products})



# <!-- your_template.html -->
# <div class="main">
#   <div class="container">
#     <!-- BEGIN SALE PRODUCT & NEW ARRIVALS -->
#     <div class="row margin-bottom-40">
#       <!-- BEGIN SALE PRODUCT -->
#       <div class="col-md-12 sale-product">
#         <h2>New Arrivals</h2>
#         <div class="owl-carousel owl-carousel5">
#           {% for product in products %}
#           <div>
#             <div class="product-item">
#               <div class="pi-img-wrapper">
#                 <img src="{% static product.image %}" class="img-responsive" alt="{{ product.alt }}">
#                 <div>
#                   <a href="{% static product.image %}" class="btn btn-default fancybox-button">Zoom</a>
#                   <a href="#product-pop-up" class="btn btn-default fancybox-fast-view">View</a>
#                 </div>
#               </div>
#               <h3><a href="{{ product.link }}">{{ product.name }}</a></h3>
#               <div class="pi-price">{{ product.price }}</div>
#               <a href="{{ product.link }}" class="btn btn-default add2cart">BUY</a>
#               <div class="sticker sticker-sale"></div>
#             </div>
#           </div>
#           {% endfor %}
#         </div>
#       </div>
#       <!-- END SALE PRODUCT -->
#     </div>
#     <!-- END SALE PRODUCT & NEW ARRIVALS -->
#   </div>
# </div>

