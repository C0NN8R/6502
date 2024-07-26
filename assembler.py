# 6502 Assembler for a few select instructions

# Define instruction set with addressing modes and opcodes
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
    # Add more instructions and their addressing modes here as needed
}

# Get Addressing Type
def GetAddressType(arg):
    if arg.startswith("#"):
        return "imm"
    elif arg.startswith("$"):
        if len(arg) == 5:
            return "abs"
        elif len(arg) == 3:
            return "zer"
    elif arg.startswith("("):
        if len(arg) == 7:
            return "abs-ind"
    if "X" in arg:
        if len(arg) == 7 and arg.startswith("$"):
            return "x-abs"
        elif len(arg) == 7 and arg.startswith("("):
            return "x-zer-ind"
        elif len(arg) == 5:
            return "x-zer"
    if "Y" in arg:
        if len(arg) == 7 and arg.startswith("$"):
            return "y-abs"
        elif len(arg) == 7 and arg.startswith("("):
            return "y-zer-ind"
        elif len(arg) == 5:
            return "y-zer"
    return None

# Sample input instructions
ins = "LDA #$AB LDA $3B4A EXT"

# Split instructions into list
insList = list(ins.replace('\n', ' ').split(" "))

# Assemble the instructions
def Exec():
    i = 0
    while i < len(insList):
        instruction = insList[i]
        if instruction in instrSet:
            opcode_dict = instrSet[instruction]
            if isinstance(opcode_dict, dict):
                try:
                    arg = insList[i + 1]
                    addrType = GetAddressType(arg)
                    if addrType and addrType in opcode_dict:
                        opcode = opcode_dict[addrType]
                        print(f"Assembling {instruction} with {addrType} addressing:")
                        print_opcode(opcode, addrType, arg)
                        i += 1
                    else:
                        print(f"Error: Unsupported or missing addressing type for {instruction}!")
                except IndexError:
                    print(f"Error: Missing operand for {instruction}!")
            else:
                print(f"Assembling {instruction} with implied addressing:")
                print(f"0x{opcode_dict},")
        else:
            print(f"Error: Unknown instruction '{instruction}'!")
        i += 1

def print_opcode(opcode, addrType, arg):
    if addrType == "imm":
        print(f"0x{opcode}, 0x{arg[2:4]},")
    elif addrType in ["abs", "x-abs", "y-abs"]:
        print(f"0x{opcode}, 0x{arg[3:5]}, 0x{arg[1:3]},")
    elif addrType == "abs-ind":
        print(f"0x{opcode}, 0x{arg[4:6]}, 0x{arg[2:4]},")
    elif addrType in ["zer", "x-zer", "y-zer"]:
        print(f"0x{opcode}, 0x{arg[1:3]},")
    elif addrType in ["x-zer-ind", "y-zer-ind"]:
        print(f"0x{opcode}, 0x{arg[2:4]},")

Exec()
