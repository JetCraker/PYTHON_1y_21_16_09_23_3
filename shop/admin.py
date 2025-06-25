from django.contrib import admin
from .models import Stuff, Rating, Bucket, Order, OrderItem


admin.site.register(Bucket)

@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ('stuff_name', 'price', 'create_at', 'average_rating')
    list_filter = ('create_at', )
    search_fields = ('stuff_name', 'stuff_desc')
    readonly_fields = ('average_rating', )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_filter = ('stuff', 'user', 'stars', 'created_at')
    list_display = ('stars', )
    search_fields = ('stuff__stuff_name', 'user__username')
