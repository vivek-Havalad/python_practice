 
def create_dict():
    a = [1,2,3]
    b = [4,5,6]
    c = {}
    i = 0
    while i < len(a) and i < len(b):
        c[a[i]] = b[i]
        i+=1
    print("dict",c)

def remove_duplicates():
    a = [1,2,3,4,1,2]
    temp = []
    for item in a:
        if item not in temp:
            temp.append(item)
    #print("unique list",temp)
    c = [i for index,i in enumerate(a) if i not in a[:index] ]
    print(c)

def find_balance_of_paranthesis():
    pass

def func(xyz=[]):
    xyz.append(4)
    print(xyz)
    xyz = [5,6,7]
    return       

class Staff:
    
    name = None
    count = 0

    def __init__(self,name):
        self.name = name
        Staff.count+=1

obj1 = Staff("A")
obj2 = Staff("B")
print("No .of objects have been created is ",Staff.count)

create_dict()
#remove_duplicates()
#find_balance_of_paranthesis()
