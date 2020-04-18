# Ryze © 2020
# Duck Game Music Manager
import os
import shutil
import shelve
import gettext
from sys import exit
from sys import _MEIPASS

# Entry variable for menu
entry = ""

# Current lang
lang = ""
# Available langs
langs = ['en','ru_RU']
# Variable for GetText
_ = None
# List of packs
packs = {}
filesState = {}
# Path to Duck Game
DGPath = ''
# Database file
db = shelve.open('DGMM')
print(_MEIPASS)

def firstRun():
    entry = -1
    global _

    print('|         Welcome to Duck Game Music Manager          |')
    print('| 1. English                                          |')
    print('| 2. Русский                                          |')
    while (entry < 1 or entry > 2):
        try:
            entry = int(input('| Language/Язык: '))
        except ValueError:
            continue
    
    db['Lang'] = langs[entry-1]
    
    # Install Translation
    text = gettext.translation('base', _MEIPASS+'\\locales', languages=[langs[entry-1]])
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
    
    # Install Translation
    text = gettext.translation('base', _MEIPASS+'\\locales', languages=[lang])
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
def enablePack(keepOriginalMusic):
    #print('| Installing', pack, '|')
    # Unlink all previous packs
    for path, _, files in os.walk(DGPath):
        for file in files:
            os.unlink(path + '\\' + file)
    os.chdir("Music Packs\\")
    for pack in packs:      
        print(pack)
        #Go to Audio section of pack
        os.chdir(pack + '\\Audio')
        
        # Link pack files  
        for path, _, files in os.walk('.\\'):
        
            for file in files:
                print(file)
                if not filesState[pack][packs[pack].index(file)]:
                    continue
            
                link = DGPath + path[1:] + '\\' + file
                src = os.path.abspath(path + '\\' + file)
                
                os.symlink(src,link)
        os.chdir('../../')
    os.chdir('../')
    # Go to Audio section of original pack
    #os.chdir('..\\..\\DG Original\\Audio') 
    
    # Link Original files
    #for path, _, files in os.walk('.\\'):
        # Continue if user doesn't want to keep original music
     #   if path == '.\\Music\\InGame' and not keepOriginalMusic:
          #  continue
#
     #   for file in files:
      #      link = DGPath + path[1:] + '\\' + file
      #      src = os.path.abspath(path + '\\' + file)
            
            # If link exists. It means that file already overrided by pack
      #      # So continue
       #     if os.path.isfile(link):
        #        continue  
            
        #    os.symlink(src,link)
            
    # Go to Root path
    os.chdir('../../../')
    
def drawPacksProp(pack):
    print(_("|               Manager               |"))
    for i, file in enumerate(packs[pack]):
        print(str(i+1) + '.' + file, filesState[pack][i])
    print(str( len(packs[pack]) + 1)  + '.' +' Exit')

def packProperties(pack):
    entry = -1
    
    drawPacksProp(pack)
    
    while entry != str(len(packs[pack]) + 1):
        try:
            entry = int(input('File: '))    
        except ValueError:
            continue
        
        if entry == len(packs[pack]) + 1 :
            break
        
        filesState[pack][entry-1] = not filesState[pack][entry-1]
        drawPacksProp(pack)
        


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
    
    if keepOriginal.upper() == yes:
        keepOriginalMusic == True
    
    os.system('cls')
    
    
    packProperties(list(packs.keys())[entry-1])


# Function for scanning packs
def scan():
    global packs
    # Delete previous packs
    packs = {}

    if not os.path.isdir('Music Packs'):
        os.mkdir('Music Packs')

    os.chdir('Music Packs')
    dir = os.listdir('./')
    
    for pack in dir:
        # If item is file skip it
        if os.path.isfile(pack):
            continue
        
        # Find all files in pack
        packs[pack] = []
        filesState[pack] = []
        for _,_,files in os.walk(pack + '\\Audio'):
            for file in files:
                packs[pack].append(file)
                filesState[pack].append(True)
 
        print("| Found " +  pack)
    
    # Go to Root
    os.chdir('../')


# Function for printing manager
def manager():
    while 1:
        entry = ""
        print(_("|                     Manager                     |"))
        print(_("| 1. Install all Packs                            |"))
        print(_("| 2. Packs                                        |"))
        print(_('| 3. Rescan                                       |'))
        print(_('| 4. Exit to menu                                 |'))
        
        while (entry != '1' and entry != '2' and entry != '3' and entry != '4'):
            entry = input(_('| Choose entry: '))
        
        if entry == '1':
            enablePack(False)
        
        elif (entry == '2'):
            displayPacks()
        elif (entry == '3'):
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

if not 'DG Original' in packs:
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