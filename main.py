import numpy as np
import pandas as pd
import random


# Subject : SubjectCode Matching
sub = {'CS501': 'TOC', 'CS502': 'DBMS', 'CS503': 'CS', 'CS504': 'IWT'}


# Teacher : SubjectCode Matching
teacher = {'CS501': ['Prof. Shusheel Gupta', 'Prof. Puneet Nema', 'Prof. Balram Purswani'],
           'CS502': ['Dr. Bhupesh Gour', 'Dr. Sadhana K. Mishra', 'Prof. Priyanka Asthana'],
           'CS503': ['Prof. Neelesh Gour', 'Prof. Sanjay Kumar Gupta', 'Prof. Himanshu Barhaiya'],
           'CS504': ['Prof. Aditya Patel', 'Prof. Vivek Kr Sharma','Prof. Vivek Kr Sharma']}


# Teacher : TeacherCode Matching
teacherHash = {'Prof. Shusheel Gupta': 0, 'Prof. Puneet Nema': 1, 'Prof. Balram Purswani': 2,
               'Dr. Bhupesh Gour': 3, 'Dr. Sadhana K. Mishra': 4, 'Prof. Priyanka Asthana': 5,
               'Prof. Neelesh Gour': 6, 'Prof. Sanjay Kumar Gupta': 7, 'Prof. Himanshu Barhaiya': 8,
               'Prof. Aditya Patel': 9, 'Prof. Vivek Kr Sharma': 10}


# Graph Data Structure To Handle Set
shape = (11, 11)
graph = np.zeros(shape, dtype='int32')


# Function To Add Teachers Pair In Graph
# Graph is Undirected And Symmetric
def AddEdge(choice):
    for i in range(len(choice) - 1):
        for j in range(i + 1, len(choice) - 1):
            graph[choice[i + 1]][choice[j + 1]] += 1
            graph[choice[j + 1]][choice[i + 1]] += 1


# Checks Pair Validity And Returns The Connectivity Score
# Connectivity Score = Total Number Of Edges Between The Valid Set
def ValidSet(set):
    sum = 0
    for i in set:
        for j in set:
            if i != j:
                if graph[teacherHash[i]][teacherHash[j]] == 0:
                    return 0 # If Pair Doesn't Exists Return Zero
                sum += graph[teacherHash[i]][teacherHash[j]] # Else Calculates The Number Of Edges Between The Valid Pairs
    return sum # Returns The Connectivity Score


# Generate Best Sets
# Generates All Possible Sets
# If Valid Returns The Best Possible Set With Maximum Connectivity Score
def GenerateSet():
    max = 0
    bestSet = []
    for _toc in teacher['CS501']:
        for _dbms in teacher['CS502']:
            for _cs in teacher['CS503']:
                for _iwt in teacher['CS504']:
                    edgeSum = ValidSet((_toc,_dbms,_cs,_iwt))# Checks For Valid Pair
                    if edgeSum:
                        if edgeSum>max:
                            max = edgeSum
                            bestSet = (_toc,_dbms,_cs,_iwt)# Saving The Best Set

    # Removing Teachers Included In Best Set
    teacher['CS501'].remove(bestSet[0])
    teacher['CS502'].remove(bestSet[1])
    teacher['CS503'].remove(bestSet[2])
    teacher['CS504'].remove(bestSet[3])

    # Returns The Best Set One At A Time
    return bestSet


# Loading CSV FILE
data = pd.read_excel('C:\\Users\\adity\\OneDrive\\Desktop\\Faculty Response.xlsx')


# Getting Individual Entries
roll  = list(data['Enrollment'])
CS501 = list(data[sub['CS501']])
CS502 = list(data[sub['CS502']])
CS503 = list(data[sub['CS503']])
CS504 = list(data[sub['CS504']])


# Creating 2-d Array --> Student : Choice
i = 0
for _ in roll:
    tuple_pack = roll[i], CS501[i], CS502[i], CS503[i], CS504[i]
    record = list(tuple_pack)
    # print(record)
    i += 1


# Doing Random Choices For Testing
enroll = []  # List Containing Roll Number Of Student
_TOC = []    # List Containing TOC Faculty Choice Roll Number-Wise
_DBMS = []   # List Containing DBMS Faculty Choice Roll Number-Wise
_CS = []     # List Containing CS Faculty Choice Roll Number-Wise
_IWT = []    # List Containing IWT Faculty Choice Roll Number-Wise
for number in range(1, 100):
    enroll.append(number)
    _TOC.append(random.choice(teacher['CS501']))
    _DBMS.append(random.choice(teacher['CS502']))
    _CS.append(random.choice(teacher['CS503']))
    _IWT.append(random.choice(teacher['CS504']))


# Adding Teachers Pair In Graph
StudentChoice = []
for roll, toc, dbms, cs, iwt in zip(enroll, _TOC, _DBMS, _CS, _IWT):
    tuple_pack = (roll, teacherHash[toc], teacherHash[dbms], teacherHash[cs], teacherHash[iwt])
    choice = list(tuple_pack)
    choice_raw = (roll, toc, dbms, cs, iwt)
    StudentChoice.append(list(choice_raw))
    AddEdge(choice) # Calling AddEdge Funtion


# Generating three Best Sets
# Storing The Best Sets In Pair Dictionary
# Key:Value <==> int:tuple
Pair = {}
for i in range(3):
    Pair[i] = GenerateSet()


# Matching The Student Choice With Generated Set
# Storing The Match In allocatedMatches(list)
allocatedMatches = []
for roll, toc, dbms, cs, iwt in zip(enroll, _TOC, _DBMS, _CS, _IWT):
    tuple_pack = roll,toc,dbms,cs,iwt
    individualMatch = list()
    individualMatch.append(roll)
    for i in Pair:
        num = 0
        if toc == Pair[i][0]  : num+=1
        if dbms == Pair[i][1] : num+=1
        if cs == Pair[i][2]   : num+=1
        if iwt == Pair[i][3]  : num+=1
        individualMatch.append(num)
    allocatedMatches.append(list(individualMatch))


# Sorts The Allocated Set According To The Number Of  Matches (Descending Order)
for i in range(len(allocatedMatches)):
    for j in range(i+1,len(allocatedMatches)):
        if max(allocatedMatches[i][1:])<max(allocatedMatches[j][1:]):
            allocatedMatches[i],allocatedMatches[j] = allocatedMatches[j],allocatedMatches[i]
            StudentChoice[i],StudentChoice[j] = StudentChoice[j],StudentChoice[i]


# Display The Chosen Set By Student And Allocated Set To Student
index = 0
for i in allocatedMatches:
    print(i[:],end=" ,maxMatch = ")
    print(max(i[1:]),end=" ,setIndex = ")
    print(i[1:].index(max(i[1:])),end="\nAllotted Set = ")
    print(Pair[i[1:].index(max(i[1:]))])
    print("Chosen Set   =",tuple(StudentChoice[index][1:]))
    index+=1
    print("-------------------------")