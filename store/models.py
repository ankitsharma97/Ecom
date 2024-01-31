from django.db import models
import datetime
# Create your models here.

# Category Class
class Category(models.Model):
    Name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Name
    
    @staticmethod
    def get_all_category():
        return Category.objects.all()
    
    
# Product class
class Product(models.Model):
    Name = models.CharField( max_length=50)
    Price = models.IntegerField(default=0)
    Description = models.CharField( max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE ,default=1)
    img = models.ImageField( upload_to='./media/prod/', height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.Name

    @staticmethod
    def get_product_id(ids):
        return Product.objects.filter(id__in = ids)
        
        
    @staticmethod
    def get_all_product():
        return Product.objects.all()
    
    # @staticmethod
    # def get_all_product_by_id(categoryId):
    #     if categoryId:
    #         return Product.objects.filter(category = categoryId)
    #     else:
    #         return Product.objects.all()
    
    @staticmethod
    def get_all_product_by_id(product_ids):
        # If product_ids is a single ID, convert it to a list
        if not isinstance(product_ids, list):
            product_ids = [product_ids]

        # Use the updated list of product IDs to retrieve products
        products = Product.objects.filter(id__in=product_ids)
        return products
        

# Customer 
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_no = models.CharField(max_length=15) 
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.email

    def register(self):
        self.save()

    @staticmethod
    def getCustomerByEmail(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None
    
    @classmethod
    def isExistEmail(cls, email):
        return cls.objects.filter(email=email).exists()
    
# Order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete =models.CASCADE)
    customer = models.ForeignKey(Customer ,on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    price = models.IntegerField(default = 0)
    address = models.TextField(default = "")
    phone = models.CharField( max_length=50)
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default = False)
    
    def placeOrder(self):
        self.save()
    
