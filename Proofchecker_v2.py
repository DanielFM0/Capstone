import re

def infix_to_prefix(wff: str) -> list:
    # Split the string on whitespaces and brackets, reverse the string and remove empty and whitespace strings from the list
    operators = ["and", "or", "impl", "not"]
    revwff = [x for x in re.split(r'(\s|\(|\))', wff)[::-1] if x not in (' ', '')]
    operator_stack = []
    output_stack = []
    for char in revwff:
        if char in operators:
            while len(operator_stack) > 0 and operator_stack[-1] != ')':
                if char == 'not':
                    break
                output_stack.append(operator_stack.pop())
            operator_stack.append(char)
        elif char == ')':
            operator_stack.append(char)
        elif char == '(':
            try:
                while operator_stack[-1] != ')':
                    output_stack.append(operator_stack.pop())
                # Get rid of the closing bracket
                operator_stack.pop()
            except:
                print("There were mismatched brackets, please check the following formula:", wff)
        else:
            output_stack.append(char)
    
    # Push all remaining operators onto the queue
    while len(operator_stack) != 0 and operator_stack[0] != ')':
        output_stack.append(operator_stack.pop())
    return output_stack[::-1]

def split_operator(prefix_wff: str):
    prefix_wff = prefix_wff[::-1]
    operators = ["and", "or", "impl"]
    # Convert it back to infix, but remove the first operator
    output_stack = []

    # In the case that the operator is "not"
    if prefix_wff[-1] == "not":
        return prefix_wff[:-1][::-1]

    for i, char in enumerate(prefix_wff):
        # Ignore first operator
        if i == len(prefix_wff) - 1:
            break
        elif char in operators:
            lchar = output_stack.pop()
            rchar = output_stack.pop()
            new_formula = "(" + lchar + " " + char + " " + rchar + ')'
            output_stack.append(new_formula)
        elif char == "not":
            neg_char = output_stack.pop()
            output_stack.append("(not " + neg_char + ")")
        else:
            output_stack.append(char)

    return infix_to_prefix(output_stack[1]), infix_to_prefix(output_stack[0])


def read_proof(filename: str) -> dict:
    proof = {}
    with open(filename, 'r') as proof_lines:
        for i, line in enumerate(proof_lines.readlines()):
            if i == 0:
                proof['prem'] = infix_to_prefix(line[:-1])
                continue
            if i == 1:
                proof['goal'] = infix_to_prefix(line[:-1])
                continue
            line = line.split(". ")
            proof[line[0]] = [infix_to_prefix(line[1]), line[2][:-1]] # [:-1] to get rid of newline character
    
    return proof

#def is_well_formed(wff):
    

##############################################################################################

# Introduction Rules

def Iconj(wff: list, proof: dict, lines: tuple) -> bool:
    if not (wff[0] == 'and'):
        print("You used the rule Introduction of Conjunction, but you introduced the", wff[0], "connective.")
        return False
    a, b = split_operator(wff)

    if not (a == (proof[lines[0]][0])):
        print("The formulas you introduced the conjunction to are not on the lines you specified. You said", a, 
        "could be found on line", lines[0], "but that is wrong.")
        return False
    elif not (b == (proof[lines[1]][0])):
        print("The formulas you introduced the conjunction to are not on the lines you specified. You said",
        b, "could be found on line", lines[1], "but that is wrong.")
        return False
    else:
        return True

def Idisj(wff: list, proof: dict, lines: tuple) -> bool:
    if not (wff[0] == "or"):
        print("You used the rule Introduction of Disjunction, but you introduced the", wff[0], "connective.")
        return False
    
    a, b = split_operator(wff)
    if not ((a == (proof[lines[0]][0])) or (b == (proof[lines[0]][0]))):
        print("The formula you introduced the disjunction to are not on the lines you specified. You said", a, "or",
        b, "could be found on line", lines[0], "but that is wrong")
        return False
    
    else:
        return True

def Iimpl(wff: list, proof: dict, lines: tuple) -> bool:
    if not (wff[0] == "impl"):
        print("You used the rule Introduction of Implication but you introduced the", wff[0], "connective.")
        return False

    a, b = split_operator(wff)
    if not (a == (proof[lines[0]][0])):
        print("The formulas you introduced the implication to are not on the lines you specified. You said that the antecedent",
        a, "could be found at", lines[0], "but that is wrong")
        return False
    
    elif not (b == (proof[lines[1]][0])):
        print("The formulas you introduced the implication to are not on the lines you specified. You said that the the consequent",
        b, "could be found at", lines[1], "but that is wrong.")
        return False

    else:
        return True

def Ineg(wff: list, proof: dict, lines: tuple) -> bool:
    if not (wff[0] == "not"):
        print("You used the rule Introduction of Negation but you introduced the", wff[0], "connective.")
        return False

    a = split_operator(wff)
    cont_1, cont_2 = split_operator(proof[lines[1]][0])
    if not (a == proof[lines[0]][0]):
        print("You said you negated the formula in line", lines[0], "but that is wrong.")
        return False
    
    elif not ((cont_1 == (["not"] + cont_2)) or ((["not"] + cont_1) == cont_2)):
        print("You said there was a contradiction at line", lines[1], "but that is wrong.")
        return False
    
    else:
        return True
    
    
# Elimination rules:
def Econj(wff: list, proof: dict, lines: tuple) -> bool:
    if not (proof[lines[0]][0][0] == "and"):
        print("You said you eliminated a conjunction in line", lines[0], "but that formula is not a conjunction.")
        return False
    
    a, b = split_operator(proof[lines[0]][0])
    if not (wff == a or wff == b):
        print("The formula you acquired is neither of the conjuncts of", proof[lines[0]])
        return False
    
    else:
        return True

def Edisj(wff: list, proof: dict, lines: tuple) -> bool:
    if not (proof[lines[0]][0][0] == "or"):
        print("You said you eliminated a disjunction in line", lines[0], "but that formula is not a disjunction.")
        return False
       
    a, b = split_operator(proof[lines[0]][0])
    if not (a == proof[lines[1]][0]):
        print("Your first assumption", a, "is not the first disjunct of the disjunction.")
        return False
    elif not (wff == proof[lines[2]][0]):
        print("You said you derived your final formula in line", lines[2], "but that is wrong.")
        return False

    if not (a == proof[lines[3]][0]):
        print("Your second assumption", b, "is not the second disjunct of the disjunction.")
        return False
    elif not (wff == proof[lines[4]][0]):
        print("You said you derived your final formula in line", lines[4], "but that is wrong.")
        return False

    else:
        return True


def Eimpl(wff: list, proof: dict, lines: tuple) -> bool:
    if not (proof[lines[0]][0][0] == "impl"):
        print("You said you eliminated an implication on line", lines[0], "but that formula is not an implication.")
        return False
    
    a, b = split_operator(proof[lines[0]][0])

    if not (a == proof[lines[1]][0]):
        print("You said the antecedent of the implication could be found at line", lines[1], "but that is wrong.")
        return False
    elif not (b == wff):
        print("You acquired", wff, "but that is not the consequent of the implication at line", lines[0])
        return False
    
    else:
        return True

    

def DNE(wff: list, proof: dict, lines: tuple) -> bool:
    if not (proof[lines[0]][0][:2] == ["not", "not"]):
        print("You said the formula in line", lines[0], "had a double negation, but that is wrong.") 
        return False
    
    if not ((["not", "not"] + wff) == proof[lines[0]][0]):
        print("You said your acquired formula is the result of applying DNE to line", lines[0], "but that is wrong.")
        return False
    
    else:
        return True

# Miscellaneous rules

def Rep(wff: list, proof: dict, lines: tuple) -> bool:
    if not (wff == proof[lines[0][0]]):
        print("You didn't repeat the formula from line", lines[0])
        return False
    else:
        return True

def check_proof(filename: str) -> bool:
    proof = read_proof(filename)
    correctness = True
    actives = ""
    for i in range(1, len(proof) - 1):
        # Stop if a mistake is found
        if not correctness:
            return False
        i  = str(i)

        # Split into wff and justification
        wff, unsplit_just = proof[i][0], proof[i][1].split(', ')
        # Clean justification lines
        just = []
        for x in unsplit_just:
            spl = x.split('-')
            just += spl
        proof_lines = tuple([x for x in just if x.isdigit()])

        # Get the rule
        rule = just[0]
        if rule == 'prem':
            proof[i].append(actives)
            if wff != proof['prem']:
                print("You said a formula was a premise but it is not in line", i)
                return False
            continue

        if rule.startswith('ass'):
            active = rule.split('(')[1].split(')')[0]
            actives += active
            proof[i].append(actives)
            continue
        elif just[-1].startswith('endass'):
            proof[i].append(actives)
            actives = actives[:-1]
        else:
            proof[i].append(actives)

        if rule == "Iconj":
            if not (len(proof_lines) == 2):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if (proof[proof_lines[0]][-1] not in proof[i][-1]) or (proof[proof_lines[0]][-1] not in proof[i][-1]):
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Iconj(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "Idisj":
            if not (len(proof_lines) == 1):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if proof[proof_lines[0]][-1] not in proof[i][-1]:
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Idisj(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "Iimpl":
            if not (len(proof_lines) == 2):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if (proof[proof_lines[0]][-1] != proof[proof_lines[1]][-1]) or (proof[i][-1] != proof[proof_lines[1]][-1][:-1]):
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Iimpl(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "Ineg":
            if not (len(proof_lines) == 2):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if (proof[proof_lines[0]][-1] != proof[proof_lines[1]][-1]) or (proof[i][-1] != proof[proof_lines[1]][-1][:-1]):
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Ineg(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "Econj":
            if not (len(proof_lines) == 1):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if proof[proof_lines[0]][-1] not in proof[i][-1]:
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Econj(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "Edisj":
            if not (len(proof_lines) == 5):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if (proof[proof_lines[0]][-1] not in proof[i][-1]) or (proof[proof_lines[1]][-1] != proof[proof_lines[2]][-1]) or\
                (proof[proof_lines[3]][-1] != proof[proof_lines[4]][-1]) or (proof[i][-1] != proof[proof_lines[2]][-1][:-1]) or\
                    (proof[i][-1] != proof[proof_lines[4]][-1][:-1]):
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Edisj(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "Eimpl":
            if not (len(proof_lines) == 2):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if (proof[proof_lines[0]][-1] not in proof[i][-1]) or (proof[proof_lines[1]][-1] not in proof[i][-1]):
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Eimpl(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)

        elif rule == "DNE":
            if not (len(proof_lines) == 1):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if proof[proof_lines[0]][-1] not in proof[i][-1]:
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = DNE(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)
        
        elif rule == "rep":
            if not (len(proof_lines) == 1):
                print("You have used the wrong number of proof lines in line", i)
                correctness = False
                break
            if proof[proof_lines[0]][-1] not in proof[i][-1]:
                print("You have used an inactive line in the justification of line", i)
                correctness = False
                break
            correctness = Rep(wff, proof, proof_lines)
            if not correctness:
                print("You made a mistake at line", i)
    
    if proof[str(len(proof)-2)][0] != proof['goal']:
        print("You didn't prove the formula you wanted to prove")
        return False
    if correctness:
        print('Done! Your proof is correct.')


check_proof("Proofs/DeMorgan.txt")
check_proof("Proofs/DeMorganWrong.txt")
check_proof("Proofs/DeMorganWrong2.txt")
check_proof("Proofs/DeMorganWrong3.txt")
check_proof("Proofs/DeMorganWrong4.txt")