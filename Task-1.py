R_type_funct_codes = {
    'add' : '100000',
    'sub' : '100010',
    'and' : '100100',
    'or' : '100101',
    'slt' : '101010'
}

I_type_op_codes = {
    'lw' : '100011',
    'beq' : '000100',
    'addi' : '001000'
}

J_type_op_codes = {
    'j': '000010'
}

Register_codes = {
    '$zero': '00000', '$t0': '01000', '$t1': '01001', '$t2': '01010', 
    '$t3': '01011', '$t4': '01100', '$t5': '01101', '$t6': '01110', 
    '$t7': '01111', '$s0': '10000', '$s1': '10001'
}

def compile(assembly):
    binary_code = []
    data_section = False
    text_section = False

    for line in assembly:
        line = line.strip()

        if line == '.data':
            data_section = True
            text_section = False
        elif line == '.text':
            data_section = False
            text_section = True
        elif text_section == True:
            instruction = convert(line)
            binary_code.append(instruction)

    return binary_code


def convert(line):
    # parts = line.split()
    parts = [part.strip(',') for part in line.split()]

    if parts[0] in R_type_funct_codes:
        instruction = parse_R_type(parts)
    elif parts[0] in I_type_op_codes:
        instruction = parse_I_type(parts)
    elif parts[0] in J_type_op_codes:
        instruction = parse_J_type(parts)

    return instruction


def parse_R_type(parts):
    op_code = '000000'
    shamt = '00000'
    funct = R_type_funct_codes[parts[0]]

    rd = Register_codes[parts[1]]
    rs = Register_codes[parts[2]]
    rt = Register_codes[parts[3]]

    return op_code + " " + rs + " " + rt + " " + rd + " " + shamt + " " + funct


def parse_I_type(parts):
    instruction = parts[0]
    op_code = I_type_op_codes[instruction]
    
    if instruction == 'lw':
        rt = Register_codes[parts[1]]

        offset, base = parts[2].split('(')
        offset = format(int(offset), '016b')
        rs = Register_codes[base[:-1]]

        return op_code + " " + rs + " " + rt + " " + offset
    elif instruction == 'beq':
        rs = Register_codes[parts[1]]
        rt = Register_codes[parts[2]]

        offset = format(int(parts[3]), '016b')

        return op_code + " " + rs + " " + rt + " " + offset
    elif instruction == 'addi':
        rs = Register_codes[parts[2]]
        rt = Register_codes[parts[1]]

        immediate = format(int(parts[3]), '016b')

        return op_code + " " + rs + " " + rt + " " + immediate
    

def parse_J_type(parts):
    instruction = parts[0]
    op_code = J_type_op_codes[instruction]

    address = format(int(parts[1]), '026b')

    return op_code + " " + address


