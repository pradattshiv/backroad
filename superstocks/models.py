from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from django.core.paginator import Paginator
import re
from django_google_maps import fields as map_fields
from passlib.hash import pbkdf2_sha256
from cryptography.fernet import Fernet
from django.utils import timezone

from django.db.models.query import QuerySet
from django.contrib.auth.models import User,Group
from smart_selects.db_fields import ChainedForeignKey





class State(models.Model):
    State_name=models.CharField(primary_key=True,max_length=100)
    Created=models.DateField(auto_now_add=True)
    
    

    def __str__(self):
        return self.State_name


class City(models.Model):
    City_Name=models.CharField(primary_key=True,max_length=100)
    State_Id=models.ForeignKey('State',on_delete=models.CASCADE,default='')
    Created=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.City_Name
    
    



class Village(models.Model):
   

    
    
    
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING,default='')
    city = ChainedForeignKey(City,
        
        chained_field="state",
        chained_model_field="State_Id",
        show_all=False,
        auto_choose=True,
        
        )
    Village_Name=models.CharField(primary_key=True,max_length=100,default='')
    Created=models.DateField(auto_now_add=True)

    
    
    
   

# for tick
    def __str__(self):
        return self.Village_Name




class SluggedModelMixin(models.Model):
    """
    Adds a `slug` field which is generated from a Hashid of the model's pk.
    `slug` is generated on save, if it doesn't already exist.
    In theory we could use the Hashid'd slug in reverse to get the object's
    pk (e.g. in a view). But we're not relying on that, and simply using
    Hashid as a good method to generate unique, short URL-friendly slugs.
    """
    slug = models.SlugField(max_length=10, null=False, blank=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if not self.slug:
    #         # self.slug = self._generate_slug(self.pk)
    #         # Don't want to insert again, if that's what was forced:
    #         # kwargs['force_insert'] = False
    #         self.save(*args, **kwargs)

    

class NaturalSortField(models.CharField):

    def naturalize(self, string):
        def naturalize_int_match(match):
            return '%08d' % (int(match.group(0)),)

        string = string.lower()
        string = string.strip()
        string = re.sub(r'^the\s+', '', string)
        string = re.sub(r'\d+', naturalize_int_match, string)

        return string
    def pre_save(self, model_instance, add):
        return self.naturalize(getattr(model_instance, self.for_field))

   

class ManageBrand(models.Model): 
    Name=models.CharField(primary_key=True,max_length=60) 
    Description=models.TextField(blank=True)     
    Logo=models.ImageField(upload_to='images') 
    active_inactive=models.BooleanField(default=True) 
    class Meta:
        ordering = ('Name',)

    def __str__(self):
        return self.Name 


class SuperStokist(SluggedModelMixin, models.Model):
    
    Stockist_Name=models.CharField(primary_key=True, max_length=100)
    created=models.DateField(auto_now_add=True)
    Register_Address=models.CharField(max_length=100,default='')
    Landmark_Address=models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city = ChainedForeignKey(City,
        
        chained_field="state",
        chained_model_field="State_Id",
        show_all=False,
        auto_choose=True,
        
        )
    PinCode=models.SlugField(max_length=6)
    
    Email = models.CharField(max_length=50,validators=[RegexValidator(regex='[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}', message="Enter Valid Email Address eg : Grishabh282@gmail.com")])
    Password=models.CharField(max_length=50)

   
    Mobile_Number=models.CharField(max_length=10,validators= [RegexValidator(regex='^(\+\d{1,3})?,?\s?\d{10}', message="Enter Valid mobile Number eg : 9999999999")])
    
    Alternate_Contactno=models.CharField(max_length=10,blank=True,validators=[RegexValidator(regex='^(\+\d{1,3})?,?\s?\d{10}', message="Enter Valid mobile 10 digit Mobile Number eg : 9999999999")])
    
    # ss=ManageBrand.objects.values()
    # my_list = []
    # dic={}
    # for i in range (0,len(ss)):
    #    my_list.append(ss[i]['Name'])
    

    # for j in range(0,len(my_list)):
    #     dic[j]=my_list[j]
    
    # t=((k,v) for k,v in dic.items())
    
    Brand = models.ManyToManyField(ManageBrand)
    
   
    STATUS = ((0, 'De-active'), (1, 'Active'),(2,'Deleted'))
    CURRENT_STATUS = models.SmallIntegerField(choices=STATUS,default='')
    COUNTRIES = {   
         "ZM": ("Zambia"),
         "ZW": ("Zimbawe")
    }

    COUNTRY_CHOICES = [(k, v) for k, v in COUNTRIES.items()]

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    address = models.CharField(max_length=255)

    country = models.CharField(
        null=False,
        blank=True,
        max_length=2,
        choices=COUNTRY_CHOICES,
        help_text="The ISO 3166-1 alpha-2 code, e.g. 'GB' or 'FR'",
    )

    Activate = ((0, 'Activate'), (1, 'Deleted'))
    Delete=models.BooleanField(default=0,choices=Activate)
    def is_SuperStokist(self):
        if self.Delete==1:
            return '1'
        return '0'

    def __str__(self):
        return self.Stockist_Name
    
    def save(self):
        obj = User.objects.create_user(username = self.Stockist_Name, password = self.Password, email = self.Email)
        obj.save()
        my_group = Group.objects.get(name='SSgroup')
        my_group.user_set.add(obj)        

        return super().save()

    


class Retailer(SluggedModelMixin,models.Model) :
    Retailer_id = models.AutoField(primary_key=True)
    Retailer_name = models.CharField(max_length=50,null = False)
    Retailer_address = models.CharField(max_length = 100,null = False)
    
    
    created=models.DateField(auto_now_add=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING,default='')
    city = ChainedForeignKey(City,
        
        chained_field="state",
        chained_model_field="State_Id",
        show_all=False,
        auto_choose=True,
        
        )
    Area_Village=ChainedForeignKey(Village,
        
        chained_field="city",
        chained_model_field="Village_In_city",
        show_all=False,
        auto_choose=True,
        
        )
    PinCode=models.CharField(max_length=6,help_text="Enter six digit Area code")
    Contact_Person_Name=models.CharField(max_length=100)
    Email = models.CharField(max_length=50,validators=[RegexValidator(regex='[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}', message="Enter Valid Email Address eg : Grishabh282@gmail.com")])
    Password=models.CharField(max_length=15,validators=[RegexValidator(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$.!%*?&]{8,}$',message="Enter correct Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character")],help_text="Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character")
    Mobile_Number=models.CharField(max_length=10,validators= [RegexValidator(regex='^(\+\d{1,3})?,?\s?\d{10}', message="Enter Valid mobile Number eg : 9999999999")])
    
    Alternate_Contactno=models.CharField(max_length=10,blank=True,validators=[RegexValidator(regex='^(\+\d{1,3})?,?\s?\d{10}', message="Enter Valid mobile 10 digit Mobile Number eg : 9999999999")])
    PanCard_Number=models.CharField(max_length=100,blank=True,help_text="Enter Your Pan Card Details")
    Supporting_Document=models.CharField(max_length=100,blank=True,help_text="Enter Your Availlable Goverment Details")

    COUNTRIES = {
         "ZM": ("Zambia"),
         "ZW": ("Zimbawe")
    }

    COUNTRY_CHOICES = [(k, v) for k, v in COUNTRIES.items()]
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    country = models.CharField(
        null=False,
        blank=True,
        max_length=2,
        choices=COUNTRY_CHOICES,
        help_text="The ISO 3166-1 alpha-2 code, e.g. 'GB' or 'FR'",
    )

    

    address = models.CharField(null=False, blank=True, max_length=255)
    Activate = ((0, 'Activate'), (1, 'Deleted'))
    Delete=models.BooleanField(default=0,choices=Activate)
    def is_Retailer(self):
        if self.Delete==1:
            return '1'
        return '0'
    
    Activate = ((1, 'Spoc'), (0, 'Retailer'))
    Spoc=models.BooleanField(default=0)
    def is_Spoc(self):
        if self.Spoc==1:
            return True
        return False 
    is_Spoc.boolean=True

    def __str__(self):
        return self.Retailer_name
    class Meta:
        ordering = ('Retailer_name',)
    



class MapStockistwithRetailer(models.Model):
    Stockist=models.ForeignKey(SuperStokist,on_delete=models.CASCADE,default='')
    
    Brand = models.ManyToManyField(ManageBrand)
    Retailer_Name = models.ManyToManyField(Retailer)
   

   
    Updated_Date=models.DateField(auto_now_add=True)





class ProductCategory(models.Model):
    
    Category = models.CharField(primary_key=True,max_length=50)
    # Sub_Category = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    
    # def __str__(self):
    #         return self.Category.username
    Description=models.TextField(blank=True)     
    Image=models.ImageField(upload_to='images') 
    active=((1, 'Deactive'), (0, 'Active'))
    Status=models.BooleanField(default=True,choices=active) 
    def is_ManageProduct(self):
        if self.Status==1:
            return True
        return False 
    is_ManageProduct.boolean=True
    def __str__(self):
       return self.Category

class ProductSubCategory(models.Model):
    Category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE,default='')
    SubCategory = models.CharField(primary_key=True,max_length=50)
    
    # Sub_Category = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    
    # def __str__(self):
    #         return self.Category.username
    Description=models.TextField(blank=True)     
    Image=models.ImageField(upload_to='images') 
    active=((1, 'Deactive'), (0, 'Active'))
    Status=models.BooleanField(default=True,choices=active) 
    def is_SubManageProduct(self):
        if self.Status==1:
            return True
        return False 
    is_SubManageProduct.boolean=True
    def __str__(self):
        return self.SubCategory
    

    

class ManageProduct(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING,default='')
    subategory= ChainedForeignKey(ProductSubCategory,
        
        chained_field="category",
        chained_model_field="Category",
        show_all=False,
        auto_choose=True,
        
        )
    Brand=models.ForeignKey(ManageBrand,on_delete=models.CASCADE,default='')
    Product_Name= models.CharField(max_length=50)
    Description=models.CharField(max_length=50)
    Image=models.ImageField(upload_to='images') 
    Product_SKU=models.CharField(max_length=50)
    Product_Price=models.IntegerField()
    Discount_On_Price=models.IntegerField()
    Related_Products=models.CharField(max_length=50)
    active=((1, 'Deactive'), (0, 'Active'))
    Status=models.BooleanField(default=True,choices=active) 
    def is_ManageProduct(self):
        if self.Status==1:
            return True
        return False 
    is_ManageProduct.boolean=True
    class Meta:
        ordering = ('Product_Name',)

class Manage_Promotions(models.Model):
    CHOICES=[('promotions on free items','Promotions On Free Items'),('value','Value'),('percentage','Percentage')] 
    Promotion_type=models.CharField(max_length=30, choices=CHOICES,)
    Promotion_Name=models.CharField(max_length=30)
    Associated_Product_ID=models.ManyToManyField(ManageProduct)
    Quantity_Buy=models.IntegerField()
    Free_Product_ID=models.IntegerField()
    Discount=models.IntegerField()
    Active_Inactive=models.BooleanField(default=True)
    def __str__(self):
        return self.Promotion_Name

