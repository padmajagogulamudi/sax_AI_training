dict1=dict(name="paddu",age="22",gen='F')
dict2={
    "name":"Ram",
    "age":20,
    "gen":'M'
}
# print(dict2)
print(dict2["age"])
dict3={1:3,4:20,3:40,9:50}
print(dict3[3])
print(dict3.get(3))
print("====================removing the dict item===============")
print(dict3)
dict3.pop(1)
dict3.popitem()
print(dict3)
print("====================looping the dict item===============")
# for k,v in dict1.items():
#     print(k+" : "+v)
emp={
    101:{
         "name":"Ram",
            "age":20,
            "gen":'M'
    },
    102:{
         "name":"sub",
            "age":21,
            "gen":'F'
    },
    103:{
         "name":"kitty",
            "age":30,
            "gen":'M'
    }
}

for x in emp:
    data=emp[x].values()
    print(data)
    print(type(data))
    (name,age,gen)=data
    print(type(data))
    print(msg:=f"sending msg to {name} of age {age} and gender {gen}")
print("============================")
list1={"s","t","o","p"}
(a,b,c,d)=list1
print(a)