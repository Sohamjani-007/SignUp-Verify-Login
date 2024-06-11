from django.urls import path
from .views import (HomePageView, AccountPageView, ShopCheckoutView, ShopContactsView, ShopFaqView, ShopGoodsCompareView,
                    ShopIndexView, ShopIndexHeaderFixView, ShopIndexLightFooterView, ShopItemView, ShopPrivacyPolicyView,
                    ShopProductListView, ShopSearchResultView, ShopShoppingCartView, ShopShoppingCartNullView,
                    ShopStandardFormsView, ShopTermsConditionsPageView, ShopWishListView)


urlpatterns = [
    path("shop-about/", HomePageView.as_view(), name="shop-about"),
    path("shop-account/", AccountPageView.as_view(), name="shop-account"),
    path("shop-checkout/", ShopCheckoutView.as_view(), name="shop-checkout"),  # We do not need checkout for now.
    path("shop-contacts/", ShopContactsView.as_view(), name="shop-contacts"),
    path("shop-faq/", ShopFaqView.as_view(), name="shop-faq"),
    path("shop-goods-compare/", ShopGoodsCompareView.as_view(), name="shop-goods-compare"),
    path("shop-index/", ShopIndexView.as_view(), name="shop-index"),
    path("shop-index-header-fix/", ShopIndexHeaderFixView.as_view(), name="shop-index-header-fix"),
    path("shop-index-light-footer/", ShopIndexLightFooterView.as_view(), name="shop-index-light-footer"),
    path("shop-item/", ShopItemView.as_view(), name="shop-item"),
    path("shop-privacy-policy/", ShopPrivacyPolicyView.as_view(), name="shop-privacy-policy"),
    path("shop-product-list/", ShopProductListView.as_view(), name="shop-product-list"),
    path("shop-search-result/", ShopSearchResultView.as_view(), name="shop-search-result"),
    path("shop-shopping-cart/", ShopShoppingCartView.as_view(), name="shop-shopping-cart"),
    path("shop-shopping-cart-null/", ShopShoppingCartNullView.as_view(), name="shop-shopping-cart-null"),
    path("shop-standard-forms/", ShopStandardFormsView.as_view(), name="shop-standard-forms"),
    path("shop-terms-conditions-page/", ShopTermsConditionsPageView.as_view(), name="shop-terms-conditions-page"),
    path("shop-wishlist/", ShopWishListView.as_view(), name="shop-wishlist")




]


