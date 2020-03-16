import gensim
import time
import os
import multiprocessing
import numpy as np
import pandas as pd
print(os.path.dirname(os.path.abspath(__file__)))
project=os.path.dirname(os.path.abspath(__file__)).replace("\\","/")

sentences=[]
with open("result/user_add_goods.txt","r",encoding="utf-8") as file:
    for line in file.readlines():
        sentences.append(line.strip().split(" "))
print("corups size:",len(sentences))

model = gensim.models.word2vec.Word2Vec(sentences=sentences,sg=1,workers=multiprocessing.cpu_count())
model = gensim.models.word2vec.Word2Vec.load("models/model.deepwalk")  # 加载旧模型
model.build_vocab(sentences, update=True)  # 更新词汇表
model.train(sentences=sentences,total_examples=model.corpus_count,epochs=30)
model.save("models/model.deepwalk")

words = ['u4594864', 'u5017752']
start = time.time()
for word in words:
    result = model.wv.most_similar(word,topn=10)
    print(result)
end = time.time()
print(end - start)

print('word-dim：', np.shape(model.wv.vectors),np.shape(model.wv.index2word))
martix=model.wv.vectors
idx2word=model.wv.index2word
print(type(martix),type(idx2word))
emb_df=pd.DataFrame(martix)
print(emb_df.head())
idx2word_df=pd.DataFrame(idx2word)
print(idx2word_df.head())
emb_df.to_csv("result/embedding.tsv",sep="\t",encoding="utf-8",index=False,header=False)
idx2word_df.to_csv("result/meta.tsv",sep="\t",encoding="utf-8",index=False,header=False)

goods_file=open("result/goods_embedding.txt","w",encoding="utf-8")
user_file=open("result/user_embedding.txt","w",encoding="utf-8")
category_file=open("result/category_embedding.txt","w",encoding="utf-8")
brand_file=open("result/brand_embedding.txt","w",encoding="utf-8")
for index in range(len(idx2word)):
   kw=idx2word[index]
   embedding=",".join([str(v) for v in martix[index]])
   if(kw[0]=='g'):
       # print("g",kw[1:],embedding)
       goods_file.write(kw[1:]+"\t"+embedding+"\n")
   elif(kw[0]=='u'):
       # print("u",kw[1:],embedding)
       user_file.write(kw[1:]+"\t"+embedding+"\n")
   elif(kw[0]=='c'):
       # print("c",kw[1:],embedding)
       category_file.write(kw[1:]+"\t"+embedding+"\n")
   else:
       # print("b",kw[1:],embedding)
       brand_file.write(kw[1:]+"\t"+embedding+"\n")
goods_file.close()
user_file.close()
category_file.close()
brand_file.close()


