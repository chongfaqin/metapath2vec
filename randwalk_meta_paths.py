# coding=utf-8
import sys
import os
import random
from collections import Counter
import goods_rel as gr

class MetaPathGenerator:
	def __init__(self):
		self.goods_brand = dict()
		self.goods_category = dict()
		self.brand_goods = dict()
		self.categroy_goods = dict()
		self.user_goods = dict()
		self.goods_user = dict()

	def read_data(self, dirpath):

		self.goods_brand,self.brand_goods=gr.get_goods_brands()
		self.goods_category,self.categroy_goods=gr.get_goods_categorys()
		gr.close_db()
		with open(dirpath + "/user_add_goods.data",encoding="utf-8") as adictfile:
			for line in adictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					key = "u" + str(toks[0])
					val = "g" + str(toks[1])
					if(key not  in self.user_goods):
						self.user_goods[key]=[val]
					else:
						self.user_goods[key].append(val)

					if(val not in self.goods_user):
						self.goods_user[val]=[key]
					else:
						self.goods_user[val].append(key)

		print("#goods_brands", len(self.goods_brand))
		print("#brands",len(self.brand_goods))
		print("#goods_categorys", len(self.goods_category))
		print("#categorys",len(self.categroy_goods))
		print("#users",len(self.user_goods))
		print("#goods_users",len(self.goods_user))


	def generate_random_data(self, outfilename, numwalks, walklength):

		outfile = open(outfilename, 'w',encoding="utf-8")
		for userkey in self.user_goods:
			loop_userkey = userkey
			for j in range(0, numwalks): #wnum walks
				outline=[]
				outline.append(userkey)
				for i in range(0, walklength):
					goods_list = self.user_goods[loop_userkey]
					numa = len(goods_list)
					goods_index = random.randrange(numa)
					goods_id = goods_list[goods_index]
					outline.append(goods_id)
					if(i%2==0):#category metapath
						# random-walk into category
						if(goods_id not in self.goods_category):
							print("not in goods-category:",goods_id)
							continue
						category_list= self.goods_category[goods_id]
						numc = len(category_list)
						category_index = random.randrange(numc)
						category_id = category_list[category_index]
						outline.append(category_id)

						# random-walk into goods
						if(category_id not in self.categroy_goods):
							print("not in category-goods",category_id)
							continue
						goods_list=self.categroy_goods[category_id]
						numc=len(goods_list)
						goods_index=random.randrange(numc)
						goods_id=goods_list[goods_index]
						outline.append(goods_id)

						#random-walk into user
						if(goods_id in self.goods_user):
							user_list=self.goods_user[goods_id]
							numc=len(user_list)
							user_index=random.randrange(numc)
							user_id=user_list[user_index]
							outline.append(user_id)

							loop_userkey=user_id
					else:#brand metapath
						# random-walk into brand
						if(goods_id not in self.goods_brand):
							print("not goods-brand:",goods_id)
							continue
						brand_list = self.goods_brand[goods_id]
						numc = len(brand_list)
						brand_index = random.randrange(numc)
						brand_id = brand_list[brand_index]
						outline.append(brand_id)

						# random-walk into goods
						if(brand_id not in self.brand_goods):
							print("not brand-goods:",brand_id)
							continue
						goods_list = self.brand_goods[brand_id]
						numc = len(goods_list)
						goods_index = random.randrange(numc)
						goods_id = goods_list[goods_index]
						outline.append(goods_id)

						# random-walk into user
						if (goods_id in self.goods_user):
							user_list = self.goods_user[goods_id]
							numc = len(user_list)
							user_index = random.randrange(numc)
							user_id = user_list[user_index]
							outline.append(user_id)

							loop_userkey = user_id

						loop_userkey = user_id
				outfile.write(" ".join(outline) + "\n")
		outfile.close()

numwalks = 30
walklength = 7


dirpath = "data"
outfilename = "result/user_add_goods_squence.txt"

def main():
	mpg = MetaPathGenerator()
	mpg.read_data(dirpath)
	mpg.generate_random_aca(outfilename, numwalks, walklength)


if __name__ == "__main__":
	main()






























