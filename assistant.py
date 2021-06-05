import JarvisAI
import re
res=input()

obj = JarvisAI.JarvisAssistant()

while True:
    if re.search('tell me about', res):
        topic = res.split(' ')[-1]
        wiki_res = obj.tell_me(topic)
        print(wiki_res)