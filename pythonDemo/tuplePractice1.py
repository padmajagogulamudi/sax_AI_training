tup1=(1,2,3,4)
tup2 = ("apple", "banana", "cherry")
tup3="ammu","kitty","surya"
tup4=tuple((101,"puppy",True,93.2))
print("========creating the tuple items========")
print(type(tup3))
print(type(tup4))
print("========accessing the tuple items========")
print(tup3[-3:-2])
print("========changing the tuple items========")

print(type(list1:=list(tup4)))
print(list1[0])
list1[0]="kitty"
print(list1[0])
print(type(tup4:=tuple(list1)))

print("========adding the tuple items========")
#same as changing the item ->convert to list ->add the ele->convert to tuple
# allowed to add tuple to tuple
tup4+=tup3
print(tup4)
print("-------- packing and unpacking the tuple----------------")
x=(100,200,300)
(ax,by,cz)=x
print(ax,"\n",by,"\n",cz)
