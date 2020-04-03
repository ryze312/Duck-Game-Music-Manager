# Ryze © 2020
# Duck Game Music Manager
import os
import shutil
import shelve

# Entry variable for menu
entry = ""
# List of packs
packs = []
# Path to Duck Game
db = shelve.open('DGMM.db')

def firstRun():
    print("|         Welcome to Duck Game Music Manager          |")
    print('| Error occured while trying to read database         |')
    print('| Looks like it is your first time opening the manager|')
    print('| Or you deleted DGMM.db                              |')
    db['DGPath'] = input('Enter path to Duck Game: ')
    db['FirstRun'] = True
    os.system('cls')


try:
    firstRun = db['FirstRun']
    DGPath = db['DGPath']
except KeyError:
    firstRun()
    firstRun = db['FirstRun']
    DGPath = db['DGPath']
finally:
    DGPath = os.path.join(DGPath, 'Content\\Audio')
    

# Custom copytree function with handling directory existence at destination
def copytree(src, dst):
    # Destination must be with name of new directory

    # Checking if path exists
    if not os.path.exists(dst):
        # If not exists create it
        os.mkdir(dst)
    
    # Walking item by item in dir
    for item in os.listdir(src):
        
        # Choosing item
        # Foo/bar + eggs.txt
        # Foo/bar/eggs.txt
        src_item = os.path.join(src,item)
        
        # Choosing item destination
        dst_item = os.path.join(dst, item)
        
        # if dir do recursivly call copytree 
        if os.path.isdir(src_item):
            copytree(src_item, dst_item)
        else:
            shutil.copy(src_item, dst_item)
            

# Function for installing pack
# Argument pack must be a string with name of pack
def installPack(pack):
    print('| Installing', pack, '|')
    os.chdir("Music Packs\\")
    #pdb.set_trace()
    
    # If installing custom pack install DG original firstly
    if pack != 'DG Original':
        copytree('DG Original\\Audio', DGPath)
    
    # Then install custom pack
    copytree(pack + '\\Audio', DGPath)
    
    # Go to root path
    os.chdir('../')
    
    
            


def displayPacks():
    # Local entry
    # entry == -1 to enter loop
    entry = -1
    
    # Show packs
    for i, pack in enumerate(packs):
        print(str(i+1)+'.', pack)
    
    # Checking if input is in range of packs
    while (entry < 0 or entry > len(packs)):
        try:
            entry = int(input('| Choose entry: '))
        # If input is empty continue
        except ValueError:
            continue   
    os.system('cls')
    
    installPack(packs[entry-1])

# Function for scanning packs
def scan():
    os.chdir('Music Packs')
    dir = os.listdir('./')
    
    for pack in dir:
        # If item is file skip it
        if os.path.isfile(pack):
            continue
        try:
            packs.index(pack)
        # If new pack found
        except ValueError:
            packs.append(pack)
            print("| Found", pack, '|')
    os.chdir('../')

# Function for printing manager
def manager():
    while 1:
        entry = ""
        print("|               Manager               |")
        print("| 1. Packs                            |")
        print('| 2. Rescan                           |')
        print('| 3. Exit to menu                     |')
        
        while (entry != '1' and entry != '2' and entry != '3'):
            entry = input('| Choose entry: ')
        
        if (entry == '1'):
            displayPacks()
        elif (entry == '2'):
            scan()      
        else:
            break
        os.system('pause')
        os.system('cls')

def menu():
    global entry
    entry = ""
    
    print("\n| Welcome to Duck Game Music Manager |")
    print("| 1. Manage                          |")
    print("| 2. About                           |")
    print("| 3. Exit                            |")
    
    while (entry != '1' and entry != '2' and entry != '3'):
        entry = input('| Choose entry: ')
    
    if (entry == '3'):
        exit()




print('| Scanning.. |')
scan()

# Check if original pack exist
try:
    packs.index('DG Original')
except ValueError:
    print('Not found original pack')
    print('Copying original sounds..')
    os.mkdir('Music Packs\\DG Original')
    copytree(DGPath, 'Music Packs\\DG Original\\Audio')
    
    
    
        
while 1:
    menu()
    os.system("cls")
    
    if (entry == '1'):
        manager()

    else:
        print('\n|      Duck Game Music Manager       |')
        print('| Version: 0.5 Alpha               |')
        print('| Created by Ryze 2020               |')
        os.system('pause')  
    os.system("cls")
    

