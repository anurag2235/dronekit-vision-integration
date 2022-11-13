def getc():
 with open("filec", "r") as file:
    last_line1 = file.readlines()[-1]
    c=int(last_line1)
    return c
def geta():    
 with open("filea", "r") as file:
    last_line2 = file.readlines()[-1]
    a=int(last_line2)
    return a
def getb():    
 with open("fileb", "r") as file:
    last_line3 = file.readlines()[-1]
    b=int(last_line3)   
    return b   
