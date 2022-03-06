difficultyRef = {
    1 : "Very Easy",
    2 : "Easy",
    3 : "Medium",
    4 : "Hard",
    5 : "Very Hard"
}

def getKey(difficultyRef, val):

    temp = list(difficultyRef.values())

    for key, value in difficultyRef.items():
        if val == value:
            return key
        
    return 0

def getKeyNew(keyList, valueList, val, ind):

    if valueList[ind] == val:
        print(keyList[ind])
        return keyList[ind]
    if len(valueList) <= ind:
        print("didnt find")
        return 0

        
    return getKeyNew(keyList, valueList, val, ind + 1)
        



#print(getKey(difficultyRef, "Hard"))

temp = getKeyNew(list(difficultyRef.keys()), list(difficultyRef.values()),"Hard", 0)
print(temp)