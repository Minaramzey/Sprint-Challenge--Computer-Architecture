"""CPU functionality."""

import sys
# Operations that we can perform
HLT = 0b00000001
LDI = 0b10000010 
PRN = 0b01000111 
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8 
        self.ram = [0] * 256
        self.PC = 0  
        self.sp = 7
        self.register[self.sp] = 0xf4
        self.less = 0
        self.greater = 0
        self.equal = 0

    def load(self, filename):
        # print(sys.argv)
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1


        except FileNotFoundError: 
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)
    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8 
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]

        # for cmd in program:
        #     self.ram[address] = cmd
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b] 
        #elif op == "SUB": etc
        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
        
        elif op == CMP:
            if self.register[reg_a] < self.register[reg_b]:
                self.less = 1
            elif self.register[reg_a] > self.register[reg_b]:
                self.greater = 1
            elif self.register[reg_a] == self.register[reg_b]:
                self.equal = 1

        elif op == "AND":
             self.register[reg_a] &= self.register[reg_b]
        
        elif op == "OR":
             self.register[reg_a] |= self.register[reg_b]
        
        elif op == "XOR":
             self.register[reg_a] ^= self.register[reg_b]
        
        elif op == "NOT":
             self.register[reg_a] =~ self.register[reg_a]
        
        elif op == "SHL":
             self.register[reg_a] <<= self.register[reg_b]
        
        elif op == "SHR":
             self.register[reg_a] >>= self.register[reg_b]
        
        elif op == "MOD":
             self.register[reg_a] %= self.register[reg_b]     

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""

        running = True

        while running: 

            cmd = self.ram[self.PC] #cmd is the address of the location of the program counter in memory

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            # print(cmd)
 
            if cmd == HLT: 
                running = False
                self.PC += 1
                
            elif cmd == LDI:
                self.register[operand_a] = operand_b
                self.PC += 3 

            elif cmd == PRN:
                print(self.register[operand_a]) 
                self.PC += 2

            elif cmd == ADD:
                self.register[operand_a] += self.register[operand_b]
                self.PC += 3 

            elif cmd == MUL:
                self.alu(cmd, operand_a, operand_b)
                self.PC += 3                

            elif cmd == PUSH:
                # Decrement SP
                self.sp -= 1
                # Get value from register
                value = self.register[operand_a]
                self.ram[self.sp]= value
                self.PC += 2

            elif cmd == POP:
                #copy the value from the address pointed to by sp to the given register
                value = self.ram[self.sp]
                self.register[operand_a] = value
                # Incrament SP
                self.sp += 1
                self.PC += 2  

            elif cmd == CALL:
                self.register[self.sp] -= 1
                self.ram[self.register[self.sp]] = self.PC + 2
                self.PC = self.register[operand_a]

            elif cmd == RET:
                self.PC = self.ram[self.register[self.sp]]
                self.register[self.sp] += 1 

            elif cmd == JMP:
                self.PC = self.register[operand_a]
            
            elif cmd == JEQ:
                if self.equal == 1:
                    self.PC = self.register[operand_a]
                else:
                    self.PC += 2
            
            elif cmd == JNE:
                if self.equal == 0:
                    self.PC = self.register[operand_a]
                else:
                    self.PC += 2

            elif cmd == CMP:
                self.alu(cmd, operand_a, operand_b)
                self.PC +=3       

            elif cmd == "AND":
                self.alu("AND", operand_a, operand_b)
                self.PC += 3  

            elif cmd == "OR":
                self.alu("OR", operand_a, operand_b)
                self.PC += 3 

            elif cmd == "XOR":
                self.alu("XOR", operand_a, operand_b)
                self.PC += 3 

            elif cmd == "NOT":
                self.alu("NOT", operand_a, operand_b)
                self.PC += 2
            
            elif cmd == "SHL":
                self.alu("SHL", operand_a, operand_b)
                self.PC += 3

            elif cmd == "SHR":
                self.alu("SHR", operand_a, operand_b)
                self.pc += 3
            
            elif cmd == "MOD":
                self.alu("MOD", operand_a, operand_b)
                self.PC += 3                            
            else:  
                print(f'unknown cmd: {cmd}')
                running = False
