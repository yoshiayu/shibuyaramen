from django.contrib import admin
from .models import RamenShop, Review, Likes
from .scraping import scrape_ramen_shops  # スクレイピング関数をインポート

@admin.register(RamenShop)
class RamenShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance_from_station', 'category', 'dinner_price', 'lunch_price')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    actions = ['import_scraped_data']

    def import_scraped_data(self, request, queryset):
        scrape_ramen_shops()
        self.message_user(request, "スクレイピングデータをインポートしました。")
    import_scraped_data.short_description = "スクレイピングでデータをインポート"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ramen_shop', 'rating', 'comment')
    search_fields = ('ramen_shop__name', 'user__username', 'comment')
    list_filter = ('rating',)

@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ramen_shop')
    search_fields = ('user__username', 'ramen_shop__name')
