from .models import Products, ProductReviews, Category, ProductViews
from rest_framework import serializers      


from django.utils.translation import gettext_lazy as _



class CategoryReadSerializer(serializers.ModelSerializer):        
    url = serializers.SerializerMethodField()  
    class Meta:
        model = Category
        fields = ( 'id',"title","slug","url")
             
    
    def get_fields(self):
        fields = super(CategoryReadSerializer, self).get_fields()
        fields['children'] = CategoryReadSerializer(many=True,required=False)
        return fields
    
    def get_url(self,obj):
       request = self.context.get('request')
       abs_url = obj.get_absolute_url()
       return request.build_absolute_uri(abs_url)
   
    
   

class ProductWriteSerializer(serializers.ModelSerializer):
    description = serializers.CharField(style={'base_template':'textarea.html','rows':15})
    seller = serializers.HiddenField(default =serializers.CurrentUserDefault())  
    image = serializers.ImageField(max_length=None,allow_empty_file =True, use_url=True,allow_null=False,required=False)      
    image2 = serializers.ImageField(max_length=None,allow_empty_file =True, use_url=True,allow_null=True,required=False)           
    image3 = serializers.ImageField(max_length=None,allow_empty_file =True, use_url=True,allow_null=True,required=False)           
    class Meta:
        model = Products   
         
        fields = ['seller','category','title',"secondhand",'image','image2','image3','description',"product_price","quantity","brand","size","color"]   
        
        


class ProductsReadSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source='seller.get_full_name')
    category = serializers.CharField(source="category.title")
    image_url = serializers.SerializerMethodField('get_image_url')  
    image2_url = serializers.SerializerMethodField('get_image2_url')
    image3_url = serializers.SerializerMethodField('get_image3_url')
    img_thumbnail_url = serializers.SerializerMethodField('get_img_thumbnail_url')
    img2_thumbnail_url = serializers.SerializerMethodField('get_img2_thumbnail_url')
    img3_thumbnail_url = serializers.SerializerMethodField('get_img3_thumbnail_url')  
    img_mid_url = serializers.SerializerMethodField('get_img_mid_url')  
    img2_mid_url = serializers.SerializerMethodField('get_img2_mid_url')
    img3_mid_url = serializers.SerializerMethodField('get_img3_mid_url')
    url = serializers.SerializerMethodField()  
    quantity_list = serializers.SerializerMethodField()
    
    
    class Meta:
        model =Products
        fields = ["id","slug","category","seller","brand","url","size","color","quantity_list","secondhand","title","image2","image3","img_thumbnail_url","img2_thumbnail_url","img3_thumbnail_url","image_url","image2_url","image3_url","description","price","created","updated","is_active","status","quantity","views","img_mid_url","img2_mid_url","img3_mid_url"]
        read_only_fields = fields
        depth = 1
        
    def get_quantity_list(self, obj):
        quantity = obj.quantity
        quantity_dict= {}
        if quantity > 1:
            for i in range(1,quantity+1):
                quantity_dict[i] = i
            return quantity_dict
                
        return quantity
        
    def get_image_url(self, obj):
        return obj.image.url
    def get_image2_url(self, obj):
        if bool(obj.image2):            
            return obj.image2.url
        else:
            return []
    def get_image3_url(self, obj):
        if bool(obj.image3):            
            return obj.image3.url
        else:
            return []
    def get_img_thumbnail_url(self, obj):
        return obj.img_thumbnail.url
    def get_img2_thumbnail_url(self, obj):
        if bool(obj.image2):
            return obj.img2_thumbnail.url
        else:
            return []
    def get_img3_thumbnail_url(self, obj):
        if bool(obj.image3):
            return obj.img3_thumbnail.url
        else:
            return []
        
    def get_img_mid_url(self, obj):
        return obj.img_mid.url
    
    def get_img2_mid_url(self, obj):
        if bool(obj.image2):            
            return obj.img2_mid.url
        else:
            return []
        
    def get_img3_mid_url(self, obj):
        if bool(obj.image3):            
            return obj.img3_mid.url
        else:
            return []
        
    def get_url(self,obj):
       request = self.context.get('request')
       abs_url = obj.get_absolute_url()
       return request.build_absolute_uri(abs_url)
        
    
 
 



        
class ProductReviewsSerializer(serializers.ModelSerializer):  
       
       
    class Meta:
        model = ProductReviews
        fields = ["id","product_id","user_id","review","rating","created_at"]
        depth = 1
    
    
        
        
class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        fields = "__all__"
        