import json
from time import sleep

# Debugging utilities

# List of breakpoints (addresses where execution will pause)
breakpoints = []

# Function to set a breakpoint
def set_breakpoint(address):
    if address not in breakpoints:
        breakpoints.append(address)
        print(f"Breakpoint set at 0x{address:04X}")
    else:
        print(f"Breakpoint already exists at 0x{address:04X}")

# Function to check if the current address is a breakpoint
def check_breakpoint(address):
    if address in breakpoints:
        print(f"Breakpoint hit at 0x{address:04X}")
        return True
    return False

# Load addrSet and insSet from JSON files
with open('addrSet.json') as f:
    addrSet = json.load(f)

with open('insSet.json') as f:
    insSet = json.load(f)

def AddrType(operand):
    abstracted_operand = ''.join('n' if c in "123456789ABCDEF" else c for c in operand)
    print(" [] - Operand abstracted as: " + abstracted_operand)
    if abstracted_operand in addrSet:
        print(" [] - Addressing Type match: " + addrSet[abstracted_operand])
        return addrSet[abstracted_operand]
    print("\n! Incorrect Addressing Type format: " + operand)
    return 0

def Exec():
    code = ""
    i = 0
    while i < len(insList):
        sleep(.15)

        if insList[i] not in insSet:
            print("\n! Unsupported Operation at i == " + str(i) + ": " + insList[i])
            return 0

        print(f"\nAssembling at i == {str(i)}: {insList[i]}")

        # Check for breakpoints
        if check_breakpoint(i):
            print("Execution paused at breakpoint.")
            input("Press Enter to continue...")

        # If non-implied addressing type (= with operand):
        if insList[i] not in ["BRK", "CLC", "CLD", "CLI", "CLV", "DEX", "DEY", "INX", "INY", "NOP", "PHA", "PHP", "PLA", "PLP",
                                "RTI", "RTS", "SEC", "SED", "SEI", "TAX", "TAY", "TSX", "TXA", "TXS", "TYA", "EXT"]:
            
            # If branch instruction:
            if insList[i] in ["BCC", "BCS", "BEQ", "BMI", "BNE", "BPL", "BVC", "BVS"]:
                addrType = "rel"
            else:
                addrType = AddrType(insList[i+1])

            try:
                opcode = insSet[insList[i]][addrType]
            except:
                print("\n! Non-compatible Addressing Type at i == " + str(i) + ": " + insList[i])
                return 0

            print(f" - Addressing type == {addrType} and opcode == {opcode}")

            if addrType == "imm":
                code += f"0x{opcode}, 0x{insList[i+1][2:4]}, "
                print(f" -> 0x{opcode}, 0x{insList[i+1][2:4]}, ")
                i+=1

            elif addrType == "abs" or addrType == "x-abs" or addrType == "y-abs":
                code += f"0x{opcode}, 0x{insList[i+1][3:5]}, 0x{insList[i+1][1:3]}, "
                print(f" -> 0x{opcode}, 0x{insList[i+1][3:5]}, 0x{insList[i+1][1:3]}, ")
                i+=1

            elif addrType == "abs-ind":
                code += f"0x{opcode}, 0x{insList[i+1][4:6]}, 0x{insList[i+1][2:4]}, "
                print(f" -> 0x{opcode}, 0x{insList[i+1][4:6]}, 0x{insList[i+1][2:4]}, ")
                i+=1

            elif addrType == "zer" or addrType == "x-zer" or addrType == "y-zer":
                code += f"0x{opcode}, 0x{insList[i+1][1:3]}, "
                print(f" -> 0x{opcode}, 0x{insList[i+1][1:3]}, ")
                i+=1

            elif addrType == "y-zer-ind" or addrType == "x-zer-ind":
                code += f"0x{opcode}, 0x{insList[i+1][2:4]}, "
                print(f" -> 0x{opcode}, 0x{insList[i+1][2:4]}, ")
                i+=1

            elif addrType == "acc":
                code += f"0x{opcode}, "
                print(f" -> 0x{opcode}, ")
                i+=1
            
            # Branch exclusive Addressing Type
            elif addrType == "rel":
                code += "branch, "
                print("branch ")
                i+=1

        else:
            opcode = insSet[insList[i]]["imp"]
            print(" - Addressing type == imp and Opcode == " + str(opcode))
            code += f"0x{opcode}, "
            print(f" -> 0x{opcode}, ")

        i+=1

    print("\nFinal Assembled Code:")
    print(code)

# Example usage
insList = ["LDA", "#$01", "STA", "$0200", "LDX", "#$08", "STX", "$0001", "LDY", "#$FF", "STY", "$0201"]
Exec()
