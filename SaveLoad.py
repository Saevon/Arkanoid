import random

def cipher(char, change = 1, sign = "+", add_char = ",.?!~`'|-"):
    """
    --> str
    Returns a ciphered form of the given character
        char(str)     --> The character to cipher
        change(int)   --> Move ordinate by how much
        add_char(str) --> Characters to add to the standard space, alphabet & numbers
                          anything not added isnt ciphered
    """
    pos = "Kjcf4IOdetx8STr3DN16Lay 2FGPZ07Wh9QEYbBiVlsuAUXCgmqopvk5wzRJHnM" + add_char
    if char in pos:
        exec "num = pos.find(char) %s %i" % (sign, int(change))
        while num >= len(pos) or num < 0:
            if num >= len(pos):
                num -= len(pos)
            elif num < 0:
                num += len(pos)
        char = pos[num]
    return char

def savegame(name, info, tocipher = True, ext = ".txt"):
    """
    --> None
    Saves data into a file and possibly ciphers it
        name(str)      --> filename & location
        info(str)      --> data to save
        tocipher(bool) --> True: cipher savefile
        loc(str)       --> location of the file
        ext(str)       --> Extension, if one is given in the filename this is ignored
    """
    if "." not in name:
        name += ext
    if tocipher:
        info1, info2 = "", ""
        for char in info:
            num = int(random.random() * 10)
            info1 += "%i" %(num)
            info2 += cipher(char, change = num)
        info = info1 + "EORN" + info2
    save = open(name, "w")
    save.write(info)
    save.close()

def loadgame(name, tocipher = True, ext = ".txt"):
    """
    --> str
    Loads data from a file and possibly deciphers it
        name(str)      --> filename & location
        tocipher(bool) --> True: decipher savefile
        ext(str)       --> Extension, if one is given in the filename this is ignored
    """
    if "." not in name:
        name += ext
    load = open(name, "r")
    info = load.read()
    if tocipher:
        old_info = info[info.find("EORN") + 4:]
        changes = info[:info.find("EORN")]
        info = ""
        for loc in range(len(old_info)):
            try:
                info += cipher(old_info[loc], change = changes[loc], sign = "-")
            except:
                pass
    load.close()
    return info
