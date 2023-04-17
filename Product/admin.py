from django.contrib import admin
from .models import Products, ProductReviews, ProductTransaction, Category
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin


admin.site.register(ProductReviews)
admin.site.register(ProductTransaction)

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id","title","seller","created","updated","price","category","quantity","status","is_active","views"]
    list_display_links= ["id","title","seller","created","updated","price","category","quantity"]
    class Meta:
        model = Products
        
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Category.objects.add_related_count(qs,Products,'category','products_cumulative_count',cumulative=True)
        qs = Category.objects.add_related_count(qs,Products,'category','products_count',cumulative=False)
        return qs
    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific˓category)'
    
    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
    
admin.site.register(Category, CategoryAdmin)
    

    
    
