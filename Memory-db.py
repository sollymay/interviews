database = {} #this is the global database
snapshots =[] #snapshots of the database Before each transaction_block

def main():
    ## program starts here and runs to the programLogic with flag as "f". This denotes that the program is not currently in a Begin state and storing the events
    programLogic("f","")

def record(state): #Core logic for the COMMIT/ROLLBACK/BEGIN
    while state:
        global database
        n= raw_input()
        command=n.split(" ")

        if command[0]== 'COMMIT' or command[0]== 'commit': #If a commit was invoked AFTER any amount of BEGINS, then the programLogic flag goes to True and we stop the iteration
            del snapshots[:] #REMOVING ALL THE SNAPSHOTS SINCE IT IS ALREADY COMMITED
            programLogic("f","")
        elif command[0]=='END' or command[0]== 'end':
            state=False
            exit()

        elif command[0]=='BEGIN' or command[0]== 'begin': #If a begin command was already set up, then this will give us the last begin (we entered here through the FIRST begin)
            if not database: #empty dict will return False, so if database is empty, append an empty dict
                snapshots.append({})
            else: #else store a copy of the database in order to be able to rollback to this point
                snapshots.append(database.copy())
        elif command[0]=='ROLLBACK' or command[0]== 'rollback': #If a rollback is called, then we delete the last snapshots and update the database
            if not snapshots:
                database ={}
            else:
                database = snapshots[-1]
                snapshots.pop()
        else:
            programLogic("t",' '.join(command))


def setFunction(command): #Function used to set values.
    try:
        global database
        database[command[1]]=command[2]
    except Exception as e:
        print "Usage for SET command: SET name value"
    else:
        pass


def getFunction(command): #Function used to get the value for a specific name store on the database. If no name is found, it returns None (the equivalent of null)
    try:
        print database[command[1]]
    except Exception as e:
        print None
    else:
        pass

def unsetFunction(command): #Function used to unset a value. If used, the currently stored key[value] pair will be deleted from the DB
    try:
        if database[command[1]] != None:
            del(database[command[1]])
        else:
            pass
    except Exception as e:
        print "No name set as " + command[1]
    else:
        pass
def numEqualToFunction(command): #Function used to count the amount of occurences for a specific value. Loops through the array and gets the values
    temp_dict = {}
    for key in database:
        if database[key] in temp_dict:
            temp_dict[database[key]] = temp_dict[database[key]] + 1
        else:
            temp_dict[database[key]] = 1
    try:
        print temp_dict[command[1]]
    except Exception as e:
        print "0"
    else:
        pass

def programLogic(flag, f):
    #The programLogic state depends on wether or not a commit is being called. if
    state = True
    while state:
        if flag == "t":
            command=f.split(" ")
            options(command)
            flag = "f"
            state = False
        elif flag == "f":
            n= raw_input()
            command=n.split(" ")
            options(command)

def options(command): #All possible options default values (since commit and rollback depend on BEGIN, they are defaulted to NO TRANSACTION)
    if command[0]=='SET' or command[0]=='set':
        setFunction(command)
    elif command[0]=="GET" or command[0]=='get':
        getFunction(command)
    elif command[0]=="UNSET" or command[0]=="unset":
        unsetFunction(command)
    elif command[0]=="NUMEQUALTO" or command[0]=="numequalto":
        numEqualToFunction(command)
    elif command[0] == 'BEGIN' or command[0]=='begin':
        if not database: #empty dict will return False, so if database is empty, append an empty dict
            snapshots.append({})
        else: #else store a copy of the database in order to be able to rollback to this point
            snapshots.append(database.copy())
        record(True)
    elif command[0] == 'COMMIT' or command[0]=='commit':
        print "NO TRANSACTION"
    elif command[0]== 'ROLLBACK' or command[0]== 'rollback':
        print "NO TRANSACTION"
    elif command[0]=='END' or command[0]=='end':
        exit()
    else:
        print "Please enter a valid command"

if __name__ == "__main__":
    main()
