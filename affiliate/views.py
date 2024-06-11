from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View

# Create your views here.


class HomePageView(View):
    def get(self, request):
        return render(request, "affiliate/shop-about.html")


class AccountPageView(View):
    def get(self, request):
        return render(request, "affiliate/shop-account.html")


class ShopCheckoutView(View):
    def get(self, request):
        return render(request, "affiliate/shop-checkout.html")


class ShopContactsView(View):
    def get(self, request):
        return render(request, "affiliate/shop-contacts.html")


class ShopFaqView(View):
    def get(self, request):
        return render(request, "affiliate/shop-faq.html")


class ShopGoodsCompareView(View):
    def get(self, request):
        return render(request, "affiliate/shop-goods-compare.html")


class ShopIndexView(View):
    def get(self, request):
        return render(request, "affiliate/shop-index.html")


class ShopIndexHeaderFixView(View):
    def get(self, request):
        return render(request, "affiliate/shop-index-header-fix.html")


class ShopIndexLightFooterView(View):
    def get(self, request):
        return render(request, "affiliate/shop-index-light-footer.html")


class ShopItemView(View):
    def get(self, request):
        return render(request, "affiliate/shop-item.html")


class ShopPrivacyPolicyView(View):
    def get(self, request):
        return render(request, "affiliate/shop-privacy-policy.html")


class ShopProductListView(View):
    def get(self, request):
        return render(request, "affiliate/shop-product-list.html")


class ShopSearchResultView(View):
    def get(self, request):
        return render(request, "affiliate/shop-search-result.html")


class ShopShoppingCartView(View):
    def get(self, request):
        return render(request, "affiliate/shop-shopping-cart.html")


class ShopShoppingCartNullView(View):
    def get(self, request):
        return render(request, "affiliate/shop-shopping-cart-null.html")


class ShopStandardFormsView(View):
    def get(self, request):
        return render(request, "affiliate/shop-standard-forms.html")


class ShopTermsConditionsPageView(View):
    def get(self, request):
        return render(request, "affiliate/shop-terms-conditions-page.html")


class ShopWishListView(View):
    def get(self, request):
        return render(request, "affiliate/shop-wishlist.html")