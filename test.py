message = "找本子 chinese big breast"
temp = message.split(" ")
tag = ""
tagCnt = 1
print(len(temp))
for i in temp:
    tag += temp[tagCnt]
    if tagCnt < len(temp)-1:
        tag += '+'
        tagCnt += 1
    print(tag)
    