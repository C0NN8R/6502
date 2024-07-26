#
#   This is a really bad assembler for a few select 6502 instructions
#   None of them currently support more than one addressing mode
#

#ins = "LDA #$AB TAX PHA ADC #$1D CMP #$C8 BEQ $02 PHA NOP JMP $FFF9 EXT"

# Get Addressing Type
def GetAddressType(arg):
    if arg[:1] == "#":
        return("imm")
    
    elif arg[:1] == "$" and len(arg) == 5:
        return("abs")
    
    elif arg[:1] == "$" and len(arg) == 3:
        return("zer")
    
    elif arg[:1] == "(" and len(arg) == 7:
        return("abs-ind")
    
    elif "X" in arg:

        if len(arg) == 7 and arg[:1] == "$":
            return("x-abs")
        
        elif len(arg) == 7 and arg[:1] == "(":
            return("x-zer-ind")
        
        elif len(arg) == 5:
            return("x-zer")
        
    elif "Y" in arg:

        if len(arg) == 7 and arg[:1] == "$":
            return("y-abs")
        
        elif len(arg) == 7 and arg[:1] == "(":
            return("y-zer-ind")
        
        elif len(arg) == 5:
            return("y-zer")
        
    else:
        return()

instrSet = {
    "EXT": "EF",
    "LDA": {
        "imm": "A9",
        "abs": "AD",
        "x-abs": "BD",
        "y-abs": "B9",
        "zer": "A5",
        "x-zer": "B5",
        "x-zer-ind": "A1",
        "y-zer-ind": "B1",
    },
}

ins = "LDA #$AB LDA $3B4A"

insList = list(ins.replace('\n', ' ').split(" "))

def Exec():
    i = 0
    while i < len(insList):

        print("Assembling at i == " + str(i) + ": " + insList[i])

        if len(instrSet[insList[i]]) > 1:
            try:
                addrType = GetAddressType(insList[i+1])
            except: print("Incorrect Addressing Type detected!!! Aborting!!!"); break
            opcode = instrSet[insList[i]][addrType]

            print("Addressing type == " + str(addrType) + " and Opcode == " + str(opcode))

            if addrType == "imm":
                print("0x" + opcode + ", 0x" + insList[i+1][2:4] + ",")

            elif addrType == "abs" or addrType == "x-abs" or addrType == "y-abs":
                print("0x" + opcode + ", 0x" + insList[i+1][3:5] + ", 0x" + insList[i+1][1:3] + ",")

            elif addrType == "abs-ind":
                print("0x" + opcode + ", 0x" + insList[i+1][4:6] + ", 0x" + insList[i+1][2:4] + ",")

            elif addrType == "zer" or addrType == "x-zer" or addrType == "y-zer":
                print("0x" + opcode + ", 0x" + insList[i+1][1:3] + ",")

            elif addrType == "y-zer-ind" or addrType == "x-zer-ind":
                print("0x" + opcode + ", 0x" + insList[i+1][2:4] + ",")

            i+=1

        else:
            print("Addressing type == imp")
            opcode = instrSet[insList[i]]
            print(str(opcode) + ",")

        i+=1

Exec()
