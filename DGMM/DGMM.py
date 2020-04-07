# Ryze © 2020
# Duck Game Music Manager
import os
import shutil
import shelve
import gettext
from sys import exit

# Entry variable for menu
entry = ""
lang = ""
langs = ['en','ru_RU']
_ = None
# List of packs
packs = []
# Path to Duck Game
db = shelve.open('DGMM')
DGPath = ''

def firstRun():
    entry = -1
    global _

    print('|         Welcome to Duck Game Music Manager          |')
    print('| 1. English                                          |')
    print('| 2. Русский                                          |')
    
    while (entry < 1 or entry > 2):
        entry = int(input('| Language/Язык: '))
    
    db['Lang'] = langs[entry-1]
    
    text = gettext.translation('base', 'locales', languages=[langs[entry-1]])
    text.install()
    _ = text.gettext
    os.system('cls')

    print(_("|         Welcome to Duck Game Music Manager          |"))
    print(_('| Error occured while trying to read database         |'))
    print(_('| Looks like it is your first time opening the manager|'))
    print(_('| Or you deleted DGMM.dir                             |'))
    db['DGPath'] = input(_('| Enter path to Duck Game: '))
    
    os.system('cls')


try:
    DGPath = db['DGPath']
    lang = db['Lang']
    
    text = gettext.translation('base', 'locales', languages=[lang])
    text.install()
    _ = text.gettext

except KeyError:
    firstRun()
    DGPath = db['DGPath']
    lang = db['Lang']
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
def enablePack(pack, keepOriginalMusic):
    print('| Installing', pack, '|')
    
    #Go to Audio section of pack
    print(os.getcwd())
    os.chdir("Music Packs\\" + pack + '\\Audio')

    # Unlink all previous packs
    for path, _, files in os.walk(DGPath):
        for file in files:
            os.unlink(path + '\\' + file)
    
    # Link pack files  
    for path, _, files in os.walk('.\\'):
        for file in files:
            
            link = DGPath + path[1:] + '\\' + file
            src = os.path.abspath(path + '\\' + file)
            
            os.symlink(src,link)

    # Go to Audio section of original pack
    os.chdir('..\\..\\DG Original\\Audio') 
    
    # Link Original files
    for path, _, files in os.walk('.\\'):
        # Continue if user doesn't want to keep original music
        if path == '.\\Music\\InGame' and not keepOriginalMusic:
            continue

        for file in files:
            link = DGPath + path[1:] + '\\' + file
            src = os.path.abspath(path + '\\' + file)
            
            # If link exists. It means that file already overrided by pack
            # So continue
            if os.path.isfile(link):
                continue  
            
            os.symlink(src,link)
            
    # Go to Root path
    os.chdir('../../../')


def displayPacks():
    # Local entry
    # entry == -1 to enter loop
    entry = -1
    keepOriginalMusic = False
    
    # Show packs
    for i, pack in enumerate(packs):
        print(str(i+1)+'.', pack)
    
    # Checking if input is in range of packs
    while (entry < 0 or entry > len(packs)):
        try:
            entry = int(input(_('| Choose entry: ')))
        # If input is empty continue
        except ValueError:
            continue

    keepOriginal = input(_('| Keep original music (Y/N): '))
    
    if lang == 'ru_RU':
        yes = 'Д'
        no = 'Н'
    else:
        yes = 'Y'
        no = 'N'
    
    while keepOriginal.upper() != yes and keepOriginal.upper() != no:
        keepOriginal = input(_('| Keep original music (Y/N): '))
    
    if keepOriginal == 'Y':
        keepOriginalMusic == True
    
    os.system('cls')
    
    enablePack(packs[entry-1], keepOriginalMusic)


# Function for scanning packs
def scan():
    if not os.path.isdir('Music Packs'):
        os.mkdir('Music Packs')

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
            print(_("| Found "), pack)
    os.chdir('../')


# Function for printing manager
def manager():
    while 1:
        entry = ""
        print(_("|               Manager               |"))
        print(_("| 1. Packs                            |"))
        print(_('| 2. Rescan                           |'))
        print(_('| 3. Exit to menu                     |'))
        
        while (entry != '1' and entry != '2' and entry != '3'):
            entry = input(_('| Choose entry: '))
        
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
    
    print(_("\n| Welcome to Duck Game Music Manager |"))
    print(_("| 1. Manage                          |"))
    print(_("| 2. About                           |"))
    print(_("| 3. Exit                            |"))
    
    while (entry != '1' and entry != '2' and entry != '3'):
        entry = input(_('| Choose entry: '))
    
    if (entry == '3'):
        db.close()
        exit()


print(_('| Scanning...'))
scan()

# Check if original pack exist
try:
    packs.index('DG Original')
except ValueError:
    print(_('| NTF original pack'))
    print(_('| Copying original sounds...'))
    
    os.mkdir('Music Packs\\DG Original')
    copytree(DGPath, 'Music Packs\\DG Original\\Audio')
    
    packs.append('DG Original')
    
    # Delete original Audio Tree
    shutil.rmtree(DGPath)
    
    # Recreate it without files
    os.mkdir(DGPath)
    os.mkdir(DGPath+'\\Music')
    os.mkdir(DGPath+'\\Music\\InGame')
    os.mkdir(DGPath+'\\SFX')
    os.mkdir(DGPath+'\\SFX\\Voice')
    os.mkdir(DGPath+'\\SFX\\Voice\\Mallard')
    os.mkdir(DGPath+'\\SFX\\Voice\\Mallard2')
    os.mkdir(DGPath+'\\SFX\\Voice\\Vincent')

        
while 1:
    menu()
    os.system("cls")
    
    if (entry == '1'):
        manager()

    else:
        print(_('\n|      Duck Game Music Manager       |'))
        print(_('| Version: 0.6 Alpha                 |'))
        print(_('| Created by Ryze 2020               |'))
        os.system('pause')  
    os.system("cls")