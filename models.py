from django.db import models

# Create your models here.
class recruituser(models.Model):
	user = models.CharField(primary_key=True, max_length=100)
	u_field = models.CharField(max_length=20)
	u_education = models.CharField(max_length=10)
	salary = models.CharField(max_length=10)
	def get_or_create(user_key):
		try:
			return recruituser.objects.get(user=user_key)
		except:
			recruituser.objects.create(user=user_key)
			return recruituser.objects.get(user=user_key)
	def set_field(self, s_text):
		self.u_field = s_text
		self.save()
	def set_education(self, s_text):
		self.u_education = s_text
		self.save()
	def set_salary(self, s_text):
		self.salary = s_text
		self.save()

class recruitinfo(models.Model):
	cmp_name = models.CharField(primary_key=True, max_length=100)
	date = models.CharField(max_length=20)
	recruit_content = models.CharField(max_length=200)

			
class companyinfo(models.Model):
	comp_name = models.CharField(primary_key=True, null=False, max_length=100)
	j_type = models.CharField(max_length=20)
	j_level = models.CharField(max_length=20)
	r_level = models.CharField(max_length=20)
	r_cnt = models.IntegerField(default=0)
	a_cnt = models.IntegerField(default=0)
	k_word = models.CharField(max_length=500)
	comp_salary = models.CharField(max_length=30)
	submit_date = models.IntegerField(default=0)
	view_act = models.IntegerField(default=1)

class test(models.Model):
	comp_name = models.CharField(primary_key=True, null=False, max_length=100)
	j_type = models.CharField(max_length=20)
	j_level = models.CharField(max_length=20)
	r_level = models.CharField(max_length=20)
	r_cnt = models.IntegerField(default=0)
	a_cnt = models.IntegerField(default=0)
	k_word = models.CharField(max_length=500)
	comp_salary = models.CharField(max_length=30)
	submit_date = models.IntegerField(default=0)
	view_act = models.IntegerField(default=1)
	field = models.CharField(max_length=20)

class rank(models.Model):
	comp_name = models.CharField(primary_key=True, null=False, max_length=100)
	j_type = models.CharField(max_length=20)
	j_level = models.CharField(max_length=20)
	r_level = models.CharField(max_length=20)
	r_cnt = models.IntegerField(default=0)
	a_cnt = models.IntegerField(default=0)
	comp_salary = models.CharField(max_length=30)
	submit_date = models.IntegerField(default=0)
	field = models.CharField(max_length=20)
	result = models.FloatField(default=0)




