from django.contrib import admin
from . models import State,City,SuperStokist,Retailer,Village,MapStockistwithRetailer,ManageBrand,ProductCategory, ManageProduct,ProductSubCategory,Manage_Promotions
from django.conf import settings
from django.core.paginator import Paginator



#State
class StateAdmin(admin.ModelAdmin):
    # def has_delete_permission(self,request,obj=None):
    #     return False if self.model.objects.filter(Delete='0') else super().has_delete_permission(request)
    # def get_queryset(self,*args,**kwargs):
    #     return State.objects.filter(Delete='0')
    list_display = ('State_name','Created',)
    list_filter = ('State_name',)
    search_fields = ('State_name',)
    list_per_page = 10
admin.site.register(State,StateAdmin)


class ManageProductAdmin(admin.ModelAdmin):
    class Media:
        js = (
        'js/admin/search.js')

admin.site.register(ManageProduct,ManageProductAdmin)
admin.site.register(ProductSubCategory)

#City
class CityAdmin(admin.ModelAdmin):
    # def has_delete_permission(self,request,obj=None):
    #     return False if self.model.objects.filter(Delete='0') else super().has_delete_permission(request)
    # def get_queryset(self,*args,**kwargs):
    #     return City.objects.filter(Delete='0')
    list_display=('City_Name','Created','State_Id')
    list_filter = ('City_Name',)
    search_fields = ('City_Name',)
admin.site.register(City,CityAdmin)

#Brand
class BrandAdmin(admin.ModelAdmin):
    # def has_delete_permission(self,request,obj=None):
    #     return False if self.model.objects.count()>0 else super().has_delete_permission(request)
    
    list_display=('Name',)
    list_filter = ('Name',)
    search_fields = ('Name',)

admin.site.register(ManageBrand, BrandAdmin)





# class CountryListFilter(admin.SimpleListFilter):


#     def lookups(self, request, model_admin):

#         list_of_countries = []

#         # We don't need the country_count but we need to annotate them in order
#         # to group the results.
#         qs = (
#             SuperStokist.objects.exclude(country="")
#             .values("country")
#             .annotate(country_count=Count("country"))
#             .order_by("country")
#         )
#         for obj in qs:
#             country = obj["country"]
#             list_of_countries.append((country, SuperStokist.COUNTRIES[country]))

#         return sorted(list_of_countries, key=lambda c: c[1])

    


    
#Village
class Villageadmin(admin.ModelAdmin):

   
    # def has_delete_permission(self,request,obj=None):
    #     return False if self.model.objects.count()>0 else super().has_delete_permission(request)
    
    # def get_queryset(self,*args,**kwargs):
    #     return Village.objects.filter(Delete='0')
   
    list_display =("Village_Name",)
    list_filter = ('Village_Name',)
    search_fields=('Village_Name',)
    list_per_page = 10
admin.site.register(Village,Villageadmin)

#Retailer
class Retaileradmin(admin.ModelAdmin):
    # def has_delete_permission(self,request,obj=None):
    #     return False if self.model.objects.count()>0 else super().has_delete_permission(request)

    # def get_queryset(self,*args,**kwargs):
    #     return Retailer.objects.filter(Spoc='1')
    fields = (('Retailer_name','Spoc'),'Retailer_address','state','city','Area_Village','Email','Password','Mobile_Number','Alternate_Contactno','PanCard_Number','Supporting_Document','address',('latitude','longitude'),'country', )
    list_display =['Retailer_name', 'is_Spoc','created','city',]
    list_filter = ('Retailer_name',)
    search_fields=('Retailer_name',)
    list_per_page = 10
    list_select_related = ('city',) 
    

    class Media:
        if settings.API_MAP:
            css = {'all': ('css/admin/location_picker.css',)}
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.API_MAP),
                'js/admin/location_picker.js',
            )

admin.site.register(Retailer,Retaileradmin)    

#SuperStockist
class SuperStokistAdmin(admin.ModelAdmin):
    def get_queryset(self,*args,**kwargs):
        return SuperStokist.objects.filter(Delete='0')
    def has_delete_permission(self,request,obj=None):
        return False if self.model.objects.count()>0 else super().has_delete_permission(request)
    list_display = ( "Stockist_Name","address","Password",)
    list_filter = ('Stockist_Name',)
    search_fields=('Stockist_Name',)
    list_per_page = 10
    filter_horizontal = ('Brand',)

    
    
    class Media:
        if settings.API_MAP:
            css = {'all': ('css/admin/location_picker.css',)}
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.API_MAP),
                'js/admin/location_picker.js',
            )
admin.site.register(SuperStokist,SuperStokistAdmin)
class MapStockistwithRetailerAdmin(admin.ModelAdmin):
    filter_horizontal=('Brand','Retailer_Name',)
   
    
admin.site.register(MapStockistwithRetailer,MapStockistwithRetailerAdmin)


class ProductAdmin(admin.ModelAdmin):

    list_display = ( "Category","is_ManageProduct",)


admin.site.register(ProductCategory,ProductAdmin) 


class ManagePromotionsAdmin(admin.ModelAdmin):
    filter_vertical=('Associated_Product_ID',)
admin.site.register(Manage_Promotions,ManageProductAdmin)
