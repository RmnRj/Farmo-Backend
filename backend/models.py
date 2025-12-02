from django.db import models
from django.utils import timezone


class Users(models.Model):
	user_id = models.CharField(max_length=20, primary_key=True)
	profile_url = models.CharField(max_length=255, blank=True, null=True)
	user_type = models.CharField(max_length=50, blank=True, null=True)
	f_name = models.CharField(max_length=50)
	m_name = models.CharField(max_length=50, blank=True, null=True)
	l_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=15, unique=True)
	phone2 = models.CharField(max_length=15, blank=True, null=True)
	email = models.EmailField(max_length=100, unique=True)
	password = models.CharField(max_length=255, blank=True, null=True)
	province = models.CharField(max_length=50, blank=True, null=True)
	district = models.CharField(max_length=50, blank=True, null=True)
	ward = models.CharField(max_length=50, blank=True, null=True)
	tole = models.CharField(max_length=100, blank=True, null=True)
	dob = models.DateField(blank=True, null=True)
	whatsapp = models.CharField(max_length=15, blank=True, null=True)
	facebook = models.CharField(max_length=200, blank=True, null=True)
	join_date = models.DateTimeField(default=timezone.now)
	about = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return f"{self.f_name} {self.l_name} ({self.user_id})"


class Credentials(models.Model):
	id = models.CharField(max_length=50, primary_key=True)
	user = models.OneToOneField(Users, on_delete=models.PROTECT, related_name='credentials', db_column='user_id')
	password = models.CharField(max_length=20, blank=True, null=True)
	status = models.BooleanField()

	def __str__(self):
		return f"Credentials {self.id}"


class Wallet(models.Model):
	wallet_id = models.CharField(max_length=50, primary_key=True)
	user = models.OneToOneField(Users, on_delete=models.PROTECT, related_name='wallet', db_column='user_id')
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	pin = models.IntegerField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Wallet {self.wallet_id}: {self.amount}"


class Transaction(models.Model):
	transaction_id = models.CharField(max_length=50, primary_key=True)
	order = models.OneToOneField('OrderRequest', on_delete=models.PROTECT, related_name='transaction', db_column='order_id')
	payment_method = models.CharField(max_length=50)
	transaction_id_gateway = models.CharField(max_length=100, blank=True, null=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, default='PENDING')
	transaction_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Transaction {self.transaction_id}: {self.amount}"


class Product(models.Model):
	p_id = models.CharField(max_length=50, primary_key=True)
	user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='products', db_column='user_id')
	name = models.CharField(max_length=255)
	category = models.CharField(max_length=100, blank=True, null=True)
	organic = models.CharField(max_length=40, default='non-organic')
	quantity_available = models.IntegerField()
	cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	produced_date = models.DateField(blank=True, null=True)
	registered_date = models.DateTimeField(default=timezone.now)
	description = models.TextField(blank=True, null=True)
	delivery_option = models.CharField(max_length=100, default='not-available')
	product_status = models.CharField(max_length=100, default='AVAILABLE')

	def __str__(self):
		return f"{self.name} ({self.p_id})"


class ProductMedia(models.Model):
	media_id = models.AutoField(primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='media', db_column='p_id')
	media_url = models.CharField(max_length=255)
	media_type = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return f"Media {self.media_id} for {self.product.name}"


class ProductRating(models.Model):
	p_rating_id = models.CharField(max_length=50, primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='ratings', db_column='p_id')
	user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='product_ratings', db_column='user_id')
	score = models.IntegerField()
	comment = models.TextField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Rating {self.prating_id}: {self.score}"


class FarmerRating(models.Model):
	r_id = models.CharField(max_length=50, primary_key=True)
	farmer = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='farmer_ratings', db_column='Farmer_id')
	consumer = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='given_farmer_ratings', db_column='Consumer_id')
	score = models.IntegerField()
	comment = models.TextField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"FarmerRating {self.r_id}: {self.score}"


class Verification(models.Model):
	v_id = models.CharField(max_length=50, primary_key=True)
	user = models.OneToOneField(Users, on_delete=models.PROTECT, related_name='verification', db_column='user_id')
	status = models.CharField(max_length=20, default='Pending')
	id_type = models.CharField(max_length=50, blank=True, null=True)
	id_number = models.CharField(max_length=50, blank=True, null=True)
	id_front = models.CharField(max_length=50, blank=True, null=True)
	id_back = models.CharField(max_length=50, blank=True, null=True)
	selfie_with_id = models.CharField(max_length=50, blank=True, null=True)
	submission_date = models.DateTimeField(default=timezone.now)
	approved_date = models.DateTimeField(blank=True, null=True)
	approved_by = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return f"Verification {self.v_id}: {self.status}"


class OrderRequest(models.Model):
	order_id = models.CharField(max_length=50, primary_key=True)
	user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='orders', db_column='user_id')
	order_date = models.DateTimeField(default=timezone.now)
	total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	fullfilment_status = models.CharField(max_length=20, default='PLACED')
	shipping_address = models.TextField(blank=True, null=True)
	expected_delivery_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return f"Order {self.order_id}: {self.fullfilment_status}"


class OrdProdLink(models.Model):
	order = models.ForeignKey(OrderRequest, on_delete=models.PROTECT, related_name='order_items', db_column='order_id')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, db_column='P_id')
	quantity = models.IntegerField()
	price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		unique_together = ('order', 'product') 

	def __str__(self):
		return f"{self.quantity} x {self.product.name} in order {self.order.order_id}"