myString = "rW2v"
color = ""

def remAryan(myString, color):
    myList = [char for char in myString]
    unwanted = {"w", "h", "i", "t", "e", "b", "l", "a", "c", "k", "v"}
    if "w" in myList or "b":
        myNewList = []
        for ele in myList:
            if ele not in unwanted: myNewList.append(ele)
            else: color += ele

    piece = ""
    for x in myNewList: piece += x
    
    return piece, color

print(remAryan(myString, color))

# myString.replace("v", "")
# print(myString)


