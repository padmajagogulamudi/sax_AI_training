# marks=457
# txt=f"my  score is {marks}"
# txt1="hello"+marks
# print(txt)
# print(txt1)
# ====================Python List====================
list1=["paddu","akki","subbu"]
print(type(list1))
list2=list(("mom",101,True))
print("====\n",type(list2))
# --------------accessing List---------------------
print("====\n",list2[2])
print(list2[-3:-1])
list3 = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
list4 = ["apple", "banana", "cherry"]
print(list3[:6])
if "apple" in list3:
    print("yes apple is present")
if list4  in list3:
    print("yes the sub list is present")
else:
    print("no !!!!!!sub list is not present")
print("========changing the list items========")

# need to check here
# --------------accessing List---------------------
l1=["a","b","c","d","e"]
l1[1:4]=[1,2]
print(l1)
l1.insert(2,list1)
print(l1[2])
# --------------adding List---------------------
print("========adding the list items========")
l1.append(8)
print(l1)
l1.extend(list2)
print(l1)
tup1=('x','y','z')
l1.extend(tup1)
# print("************")
print(l1)
print("========removing the list items========")
rli1=[1,2,3,4]
rli1.remove(1)#remove ele,if have duplicate remove the first occurance
print(rli1)
rli1.pop(2)
print(rli1)#remove the ele at specied position,if position(index) not specified removes last ele
#del rli1
#print(rli1)
rli1.clear()
print(rli1)

print("========loop the list items========")
print("----for loop------")

for item in list3:
    print(item)
print("----------")
for i in range(len(list3)):
    print(list3[i])
print("----list comprehension------")
# list3 = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
new_list1=[x for x in list3 if "a" in x]
print(new_list1)

new_list2=[x  if x=="apple" else "z" for x in list3 ]
print(new_list2)
print("========sorting the list items========")
list3.sort()
list3.sort(reverse=True)
print(list3)
list5= [100, 50, 65, 82, 23]
def myfunc1(n):
    return abs(n-50)
list5.sort(key=myfunc1)
print(list5)
list5.reverse()
print(list5)
print("========copying the list items========")
l1=["ab","cd","ef"]
l2=l1.copy()
print(l1 is l2)
l3=l2# same object will be referred
print(l1==l3)
print(l2 is l3)
l4=list(l1)
print(l1 is l4)
l5=l4[:]
print(l5 is l4)
print("=====================================================")
l6=[0,9,7,65,2]
l7=l6*2
l7=l7*2
print(l7)
print("*******")
# del l7[50]
print(l7)
print(l7.pop(1))
