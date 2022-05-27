states = []
start_state = []
acceptance_state = []
reject_state = []
input_alph = []
tape_alph = []
transitions = {}
errors = []

def addError(error):
    errors.append(error)

def validateTransition(state,line):
    transition = [i[1:-1].split(",") for i in state.split("->")]
    # get every element of the transition
    letter = transition[0][1]
    changed_state = transition[1][0]
    changed_letter = transition[1][1]
    direction = transition[1][2]

    if direction != "L" and direction != "R":
        addError("Line " + str(line) + ": " + "The directions of the turing machine should be L(left ) or R( right)")

    if transition[0][0] not in transitions:
        transitions[transition[0][0]] = [letter, (changed_state, changed_letter, direction)]
    else:
        transitions[transition[0][0]].append(letter)
        transitions[transition[0][0]].append((changed_state, changed_letter, direction))

def validateState(state, line):
    # first we check if it is a special state
    if state[-7:] == ", start":
        state = state[:-7]
        start_state.append(state)
    elif state[-8:] == ", accept":
        state = state[:-8]
        acceptance_state.append(state)
    elif state[-8:] == ", reject":
        state = state[:-8]
        reject_state.append(state)

    # if the string is not already a state, we make it one
    # otherwise, we add the error below
    if state not in states:
        states.append(state)
    else:
        addError("Line " + str(line) + ": " + state + " is already a state.")

def validateInputAlph(state,line):
    if state not in input_alph:
        input_alph.append(state)
    else:
        addError("Line " + str(line) + ": " + state + " is already in the input's alphabet.")

def validateTapeAlph(state,line):
    if state not in tape_alph:
        if(state == ""):
            state = " "
        tape_alph.append(state)
    else:
        addError("Line " + str(line) + ": " + state + " is already in the tape's alphabet.")

def readFileTM(file_name):
    f = open(file_name)
    s = [linie.strip("\n") for linie in f]
    line_cnt = 0
    while line_cnt < len(s):
        # read the states
        if s[line_cnt] == "States:":
            line_cnt += 1
            while s[line_cnt] != "--end":
                # validate each state
                validateState(s[line_cnt], line_cnt)
                line_cnt += 1
            line_cnt += 1

        elif s[line_cnt] == "Input alphabet:":
            line_cnt += 1
            while s[line_cnt] != "--end":
                # validate each input alphabet
                validateInputAlph(s[line_cnt],line_cnt)
                line_cnt += 1
            line_cnt += 1

        elif s[line_cnt] == "Tape alphabet:":
            line_cnt += 1
            while s[line_cnt] != "--end":
                # validate each input alphabet
                validateTapeAlph(s[line_cnt],line_cnt)
                line_cnt += 1
            line_cnt += 1

        else:
            line_cnt += 1
            while s[line_cnt] != "--end":
                validateTransition(s[line_cnt], line_cnt)
                line_cnt += 1
            line_cnt += 1

readFileTM("tm_config_file")

# you cannot have more than one starting state
def validateStateLength(state,state_name):
    if len(state) > 1:
        error = "You cannot have more than one " + state_name + ".( "
        for i in range(len(state)):
            error = error + state[i] + " "
        error += ")"
        errors.append(error)

def validateInputInTape():
    # verify if tape alphabet contains " " delimitator
    if " " not in tape_alph:
        addError("The ' ' is needed in the tape's alphabet to mark the end of the input.")

    # verify if the input alphabet is included inside the tape alphabet
    missing_letters = list(set(input_alph) - set(tape_alph))
    if len(missing_letters) > 0:
        error = "The input's alphabet should be included in the tape's alphabet. The tape's alphabet is missing: "
        for i in range(len(missing_letters)-1):
            error = error + missing_letters[i] + " "
        error += "."
        errors.append(error)

def validateTransitions():
    # first try to find the start, reject & acceptance state
    oks = False
    okr = False
    oka = False
    for item in transitions:
        if item not in states:
            addError(item + " is included inside a transition, as a state, but it is not a state.")
        if item in start_state: oks = True
        # we get each state transitions as a list
        let_list = transitions[item]
        # we verify if the transition letter is inside the tape's alphabet
        for i in range(0,len(let_list),2):
            if let_list[i] not in tape_alph:
                addError("State " + item + " cannot be transited using a letter that is not in the tape's alphabet.( " + let_list[i] + ")")
        # we verify the first two variables of the tuples inside each transition
        for i in range(1, len(let_list), 2):
            # verify if the first item in the tuple is a valid state
            if let_list[i][0] not in states:
                addError("State " + item + " cannot be transited into a state that does not exist.( " + let_list[i][0] + ")")
            else:
                # if its a valid state, we verify if it is a special one
                if let_list[i][0] in reject_state: okr = True
                if let_list[i][0] in acceptance_state: oka = True

            if let_list[i][1] not in tape_alph:
                addError("State " + item + " cannot be overwritten using a letter that is not in the tape's alphabet.( " + let_list[i][1] + ")")

    if oks == False:
        addError("There is no transition starting from the starting state.")
    if okr == False:
        addError("There is no transition going into the rejecting state.")
    if oka == False:
        addError("There is no transition going into the acceptance state.")

# for each type of state we check if it is valid
validateStateLength(start_state, "starting state")
validateStateLength(acceptance_state, "accepting state")
validateStateLength(reject_state, "rejecting state")
validateInputInTape()
validateTransitions()
if len(errors) == 0:
    print("Your turing machine is valid!")
else:
    for i in range(len(errors)):
        print(errors[i])
    print("So... your turing machine is invalid.")

