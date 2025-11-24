from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    profile_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'admin'

class Farmer(models.Model):
    f_id = models.CharField(max_length=50, primary_key=True, db_column='F_ID')
    f_name = models.CharField(max_length=500)
    m_name = models.CharField(max_length=50, null=True, blank=True)
    l_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    province = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    municipal = models.CharField(max_length=50, null=True, blank=True)
    ward = models.CharField(max_length=10, null=True, blank=True)
    tole = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    whatsapp = models.CharField(max_length=15, null=True, blank=True, db_column='WhatsApp')
    facebook = models.CharField(max_length=200, null=True, blank=True, db_column='Facebook')
    join_date = models.DateTimeField(auto_now_add=True)
    profile_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'farmer'

class Consumer(models.Model):
    c_id = models.CharField(max_length=50, primary_key=True, db_column='C_ID')
    f_name = models.CharField(max_length=500)
    m_name = models.CharField(max_length=50, null=True, blank=True)
    l_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'consumer'

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=50, primary_key=True, db_column='wallet_ID')
    f_id = models.OneToOneField(Farmer, on_delete=models.CASCADE, db_column='F_ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'wallet'

class Verification(models.Model):
    v_id = models.CharField(max_length=50, primary_key=True, db_column='V_ID')
    f_id = models.OneToOneField(Farmer, on_delete=models.CASCADE, db_column='F_ID')
    status = models.CharField(max_length=20, default='Pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'verification'

class Product(models.Model):
    p_id = models.CharField(max_length=50, primary_key=True, db_column='P_ID')
    f_id = models.ForeignKey(Farmer, on_delete=models.CASCADE, db_column='F_ID')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    organic = models.CharField(max_length=40, default='non-organic')
    quantity_available = models.IntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    produced_date = models.DateField(null=True, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    delivery_option = models.CharField(max_length=100, default='not-available')

    class Meta:
        db_table = 'product'

class ProductMedia(models.Model):
    media_id = models.AutoField(primary_key=True, db_column='media_ID')
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='P_ID')
    media_url = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'product_media'

class OrderRequest(models.Model):
    order_id = models.CharField(max_length=50, primary_key=True, db_column='order_ID')
    c_id = models.ForeignKey(Consumer, on_delete=models.RESTRICT, db_column='C_ID')
    order_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    fulfillment_status = models.CharField(max_length=20, default='PLACED')
    shipping_address = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'order_request'

class OrdProdLink(models.Model):
    order_id = models.ForeignKey(OrderRequest, on_delete=models.CASCADE, db_column='order_ID')
    p_id = models.ForeignKey(Product, on_delete=models.RESTRICT, db_column='P_ID')
    quantity = models.IntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ord_prod_link'
        unique_together = ('order_id', 'p_id')

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, primary_key=True, db_column='transaction_ID')
    order_id = models.OneToOneField(OrderRequest, on_delete=models.CASCADE, db_column='order_ID')
    payment_method = models.CharField(max_length=50)
    transaction_id_gateway = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction'

class FarmerRating(models.Model):
    r_id = models.CharField(max_length=50, primary_key=True, db_column='R_ID')
    f_id = models.ForeignKey(Farmer, on_delete=models.CASCADE, db_column='F_ID')
    c_id = models.ForeignKey(Consumer, on_delete=models.RESTRICT, db_column='C_ID')
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'farmer_rating'

class ProductRating(models.Model):
    prating_id = models.CharField(max_length=50, primary_key=True, db_column='PRating_ID')
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='P_ID')
    c_id = models.ForeignKey(Consumer, on_delete=models.RESTRICT, db_column='C_ID')
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_rating'
