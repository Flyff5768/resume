from snownlp import SnowNLP



text = '來看你喜歡的海\n.\n.\n.\n#vsco #vscodaily #vscotaiwan #iseetaiwan #igerstaiwan #igerstaipei #bravotaiwan #bpintaiwan #popdaily #bns_taiwan #instataiwan #instameettaiwan #ig_taiwan #wowtoplay #台灣 #台北 #台北景點 #日常 #thai #thailand #bangkok #bkk #pattaya #dongtan #jomtien'

text = '來看你喜歡的海台灣台北台北景點日常'



s = SnowNLP(text)
print(s.words)
s_senti = s.sentiments
print(s_senti)
#0.9893759430974675