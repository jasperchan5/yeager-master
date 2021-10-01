import numpy as np
arr = np.array([("a",1,2,6),("a",2,3,7),("a",3,4,8),("a",4,5,9)])
print(arr)
total = 0
cnt = 0
avg = [0,0,0,0]
for i in range(0,4):
    total = 0
    for j in range(1,4):
        total += int(arr[i][j])
    print(total)
    avg[cnt] = total/3
    cnt += 1
print(avg)