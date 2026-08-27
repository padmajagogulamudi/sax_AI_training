print("============Generators ====================")
def my_generator1(n):
    count=0
    while count<=n:
        yield count
        count+=1
for val in my_generator1(10):
    print(val)