
num = 100
def func():
    global num
    num = 200
    print(num)
 
func()
print(num)