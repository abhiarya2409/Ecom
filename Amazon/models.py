from django.db import models

# Create your models here.

class Registrations(models.Model):
    first_name = models.CharField(max_length=50, default="", null=True)
    last_name = models.CharField(max_length=50, default="", null=True)
    email = models.CharField(max_length=50, default="", null=True)
    password = models.CharField(max_length=255, default="", null=True)
    mobile = models.BigIntegerField(default=1)
    gender = models.CharField(max_length=50, default="", null=True)

    def __str__(self):
        return self.first_name

class Category(models.Model):
    category_image = models.ImageField(upload_to="upload/category/")
    category_name = models.CharField(max_length=100, default="", null=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_image = models.ImageField(upload_to="upload/product/")
    product_name = models.CharField(max_length=100, default="", null=True)
    product_price = models.BigIntegerField(default=1)
    product_description = models.TextField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    address = models.CharField(max_length=200, default="", null=True)
    mobile = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Registrations, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)  # Assuming status is a boolean field

    def __str__(self):
        return self.product.product_name
    
class Best_of_Fashion(models.Model):
    product_image = models.ImageField(upload_to="upload/Best_of_Fashion/")
    product_name = models.CharField(max_length=100, default="", null=True)
    product_price = models.BigIntegerField(default=1)
    product_description = models.TextField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name


class Best_of_Fitness(models.Model):
    product_image = models.ImageField(upload_to="upload/Best_of_Fitness/")
    product_name = models.CharField(max_length=100, default="", null=True)
    product_price = models.BigIntegerField(default=1)
    product_description = models.TextField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name




    