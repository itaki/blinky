class A:
    def __init__(self, var_number):
        my_personal_variable = var_number
        self.added_class = B()


class B:
    def __init__(self):
        class_b_var = "the B var"
    def funct(self):
        print("printing funct in class B")


x = A(10)
y = A(20)
new_list = [x,y]
print (new_list)


print(x.added_class.funct())
