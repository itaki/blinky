# class Thing:
#     def __init__(self, name):
#         self.name = name

# mylist = ["foo","bar","thingy"]

# for i in mylist:
#     i = Thing(i)
#     # here I want i to be "foo" so I can later call foo.name









# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# # 

class Student:
    def __init__(self, name, age, courses):
        self.name = name
        self.age = age
        self.courses = courses
    def dosomething():
        return True


students = [
    {
        "Name": "Bob",
        "Age": 30,
        "Courses": ["maths", "reading"]
    },
    { 
        "Name": "Glenda",
        "Age": 16,
        "Courses": ["maths", "reading"]   
    },
    { 
        "Name": "Britt",
        "Age": 55,
        "Courses": ["maths", "reading"]
    }
]

student_objects = {}

for student in students:
    student_objects[student['Name']] = Student(student['Name'], student['Age'], student['Courses'])

print (student_objects)
print (student_objects['Bob'].age)
for student in student_objects:
    print (student_objects[student].age)





# print (student_list)
# # for student in student_objects: 
# #     #print (student)
# #     print (student.name)
# #     print (student.courses)
# Carl = Student('Carl',12,["engish", "marksmanship"])
# print (Carl.courses)
# Carl.dosomething()
