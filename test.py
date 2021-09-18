message = "找本子 chinese big breast netorare nakadashi"
temp = message.split(" ")
print(temp)
tag = ""
tagCnt = 0
for i in temp:
    if tagCnt != 0:
        print(tagCnt)
        print(temp[tagCnt])
        tag += temp[tagCnt]
        if tagCnt < len(temp)-1:
            tag += '+'
            tagCnt += 1
    else:
        tagCnt += 1
print(tag)
    