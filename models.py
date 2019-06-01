from django.db import models

# Create your models here.
class User_table(models.Model):
	u_key = models.CharField(primary_key=True ,max_length = 30)
	field = models.CharField(max_length = 20)
	education =  models.CharField(max_length = 10)
	salary = models.IntegerField(default = 0)
	def get_or_create(user_key):
		try:
			return User_table.objects.get(u_key = user_key)
		except:
			User_table.objects.create(u_key=user_key)
			return User_table.objects.get(u_key=user_key)
			
	def set_field(self, s_text):
		self.field = s_text
		self.save()
		
	def set_education(self, s_text):
		self.education = s_text
		self.save()
		
	def set_salary(self, s_text):
		self.salary = s_text
		self.save()
		
		
class recruitbot(models.Model):
	cmp_name = models.CharField(primary_key=True ,max_length = 50)
	date = models.CharField(max_length = 20)
	recruit_msg = models.CharField(max_length = 200)

class test(models.Model):
	comp_name = models.CharField(primary_key=True, null=False, max_length=50)
	j_type = models.CharField(max_length=10)
	j_level = models.CharField(max_length=10)
	r_level = models.CharField(max_length=10)
	r_cnt = models.IntegerField(default=0)
	a_cnt = models.IntegerField(default=0)
	k_word = models.CharField(max_length=150)
	comp_salary = models.CharField(max_length=30)
	submit_date = models.IntegerField(default=0)
	view_act = models.IntegerField(default=1)
	field = models.CharField(max_length=10)

class url_list2(models.Model):
	comp_url = models.CharField(primary_key=True, max_length=300)

class new_recruit_info2(models.Model):
	comp_name = models.CharField(primary_key=True, null=False, max_length=100)
	com_id = models.CharField(max_length=20)
	field = models.CharField(max_length=20)
	j_type = models.CharField(max_length=20)
	j_level = models.CharField(max_length=20)
	r_level = models.CharField(max_length=20)
	r_cnt = models.IntegerField(default=0)
	a_cnt = models.IntegerField(default=0)
	k_word = models.CharField(max_length=3000)
	comp_salary = models.CharField(max_length=30)
	submit_date = models.IntegerField(default=0)
	view_act = models.IntegerField(default=1)
	score = models.FloatField(default=-1)
