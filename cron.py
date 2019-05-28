from models import recruitinfo, test
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
#import math

def get_subjects(url_list): # 채용 정보 크롤링 함수
	entlist = []

	for i in range(len(url_list)):
		req = requests.get(url_list[i])
		html = req.text
		soup = BeautifulSoup(html, 'html.parser')
		divs1 = soup.find_all("div", {"class": "item_recruit"})
		for company in divs1:
			content = company.find("div", {"class": "area_job"}).find("h2", {"class": "job_tit"}).find("a")
			company_content = content.get('title')
			grade1 = company.find("div", {"class": "area_job"}).find("div", {"class": "job_date"})
			grade2 = grade1.find("span", {"class": "date"})
			company_grade = grade2.text
			name = company.find("div", {"class": "area_corp"}).find("strong", {"class": "corp_name"}).find("a")
			company_title = name.get('title')
			try:
				recruitinfo.objects.get(cmp_name=company_title)
			except:
				recruitinfo.objects.create(
				cmp_name=company_title,
				date=company_grade,
				recruit_content=company_content
				)

			get_value = company.get("value")
			entlist.append(get_value)
			for ent_url in entlist:
				api_url = 'http://api.saramin.co.kr/job-search?id=' + ent_url + '&fields=count'
				html_result = requests.get(api_url)
				result_txt = html_result.text
				result_soup = BeautifulSoup(result_txt, 'html.parser')
				view_name = result_soup.find("company").find("name").text
				job_type = result_soup.find("job-type").text
				job_level = result_soup.find("experience-level").text
				require_level = result_soup.find("required-education-level").text


				read_cnt = result_soup.find("read-cnt").text
				view_cnt = int(read_cnt)

				apply_cnt = result_soup.find("apply-cnt").text
				view_apply = int(apply_cnt)

				keyword = result_soup.find('keyword').text
				salary = result_soup.find("salary").text


				view_date = result_soup.find("expiration-timestamp").text
				since_timestamp = time.mktime(datetime.today().timetuple())
				until_timestamp = int(view_date)

				days = (datetime.fromtimestamp(until_timestamp) - datetime.fromtimestamp(since_timestamp)).days

				act_num = result_soup.find("active").text
				view_active = int(act_num)

				if i == 0:
					try:
						test.objects.get(comp_name=view_name)
					except:
						test.objects.create(
						comp_name=view_name,
						j_type=job_type,
						j_level=job_level,
						r_level=require_level,
						r_cnt=view_cnt,
						a_cnt=view_apply,
						k_word=keyword,
						comp_salary=salary,
						submit_date=days,
						view_act=view_active,
						field = 'web')

				if i == 1:
					try:
						test.objects.get(comp_name=view_name)
					except:
						test.objects.create(
						comp_name=view_name,
						j_type=job_type,
						j_level=job_level,
						r_level=require_level,
						r_cnt=view_cnt,
						a_cnt=view_apply,
						k_word=keyword,
						comp_salary=salary,
						submit_date=days,
						view_act=view_active,
						field = 'system')

				if i == 2:
					try:
						test.objects.get(comp_name=view_name)
					except:
						test.objects.create(
						comp_name=view_name,
						j_type=job_type,
						j_level=job_level,
						r_level=require_level,
						r_cnt=view_cnt,
						a_cnt=view_apply,
						k_word=keyword,
						comp_salary=salary,
						submit_date=days,
						view_act=view_active,
						field = 'server')

	return entlist



url_list= ['http://www.saramin.co.kr/zf_user/search?cat_cd=404&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y',
		 'http://www.saramin.co.kr/zf_user/search?cat_cd=408&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y',
		 'http://www.saramin.co.kr/zf_user/search?cat_cd=402&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y']
list = get_subjects(url_list)

# def get_rank(type):
# 	if type == 'server':
# 		for key in test.objects.filter(field=type):
# 			app_cnt = key.a_cnt
# 			view_cnt = key.r_cnt
# 			date_cnt = key.submit_date
# 			a = pow(view_cnt, 2) / 1007
# 			aa = math.sqrt(a)
# 			aaa = aa / 7
#
# 			b = round((app_cnt / 10))
# 			if b > 10:
# 				result = 0.1
# 			else:
# 				result = switch(b)
# 			result_d = 1 / date_cnt
# 			result_num = aaa + result + result_d
#
#
#
# def switch(x):
# 	return {
# 		1: 1,
# 		2: 0.9,
# 		3: 0.8,
# 		4: 0.7,
# 		5: 0.6,
# 		6: 0.5,
# 		7: 0.4,
# 		8: 0.3,
# 		9: 0.2,
# 		10: 0.1,
# 	}.get(x)