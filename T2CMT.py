import os
import json
import shutil
import msvcrt
import subprocess
from subprocess import Popen
from pathlib import Path

def checkFiles():
    #region
    if Path('THUG2.exe').is_file():
        pass
    else:
        return False
    if Path('T2CMT Data').exists():
        pass
    else:
        return False
    if Path('T2CMT Data\\00.cas.xbx').is_file():
        pass
    else:
        return False
    if Path('T2CMT Data\\00.col.xbx').is_file():
        pass
    else:
        return False
    if Path('T2CMT Data\\00.usg.xbx').is_file():
        pass
    else:
        return False
    if Path('T2CMT Data\cas_skater_f_s.txt').is_file():
        global casf1
        f=open("T2CMT Data\cas_skater_f_s.txt", "r")
        if f.mode == 'r':
           casf1 =f.read()
    else:
        return False
    if Path('T2CMT Data\cas_skater_f_e.txt').is_file():
        global casf2
        f=open("T2CMT Data\cas_skater_f_e.txt", "r")
        if f.mode == 'r':
           casf2 =f.read()
    else:
        return False
    if Path('T2CMT Data\cas_skater_m_s.txt').is_file():
        global casm0
        f=open("T2CMT Data\cas_skater_m_s.txt", "r")
        if f.mode == 'r':
           casm0 =f.read()
    else:
        return False
    if Path('T2CMT Data\cas_skater_m_m.txt').is_file():
        global casm2
        f=open("T2CMT Data\cas_skater_m_m.txt", "r")
        if f.mode == 'r':
           casm2 =f.read()
    else:
        return False
    if Path('T2CMT Data\cas_skater_m_e.txt').is_file():
        global casm3
        f=open("T2CMT Data\cas_skater_m_e.txt", "r")
        if f.mode == 'r':
           casm3 =f.read()
    else:
        return False
    if Path('T2CMT Data\mainmenu_Scripts_s.txt').is_file():
        global mme1
        f=open("T2CMT Data\mainmenu_Scripts_s.txt", "r")
        if f.mode == 'r':
           mme1 =f.read()
    else:
        return False
    if Path('T2CMT Data\mainmenu_Scripts_e.txt').is_file():
        global mme2
        f=open("T2CMT Data\mainmenu_Scripts_e.txt", "r")
        if f.mode == 'r':
           mme2 =f.read()
    else:
        return False
    #endregion

def getValidString(displaymes):
    #region
    error = "Error: Invalid String - Please try again!"
    while True:
        string = input(displaymes)
        if string.strip():
            break
        else: 
            print(error) 
    return string
    #endregion

def createChrData(fname, data, outfile):
    #region
    
    if data.get("display_name"):
        print(fname + " Display Name: " +str(data["display_name"]))
    else:
        data["display_name"] = getValidString("Enter \"Display Name\" for \""+fname+"\": ")

    outfile.seek(0)
    outfile.truncate(0)
    json.dump(data, outfile, indent=2)
    return data
    #endregion

def processChrs(fpath,fname):
    #region
    cfiles = [
        ".cas.xbx",
        ".col.xbx",
        ".usg.xbx"
    ]

    for f in cfiles:
        if Path(os.path.join(fpath, fname + f)).is_file():
            print("File Found: "+os.path.join(fpath, fname + f))
        else:  
            print("No "+f+" file found for '"+fname+"' - Copying dummy file... ", end='')
            if Path('T2CMT Data\\00'+f).is_file():
                shutil.copy2(Path('T2CMT Data\\00'+f), os.path.join(fpath, fname + f))
                print("Complete")
            else:
                return False
                
    fdat = fname + ".json"
    if Path(os.path.join(fpath, fdat)).is_file():
        print("File Found: "+os.path.join(fpath, fdat))
    else:
        print("No json file found for '"+fname+"' - Creating new file... ", end='')
        data = {}
        with open(os.path.join(fpath, fdat), 'w') as outfile:
            json.dump(data, outfile)
            print("Complete")
   
    with open(os.path.join(fpath, fdat), "r+") as json_file:
        data = json.load(json_file)
        data = createChrData(fname, data, json_file)
    
    return data 
    #endregion


def getAllChrs():
    #region
    global casm0
    global casm1
    global casm2
    global casf1
    global mme1

    ddlcstr =           "\n:i :s{$struct$ = $MOD_DDLC_Monika$$name$ = %s(6,\"Monika\")$female$ = %i(1,00000001)$voice$ = $female2$:s}"
    ddlcstr = ddlcstr + "\n:i :s{$struct$ = $MOD_DDLC_Natsuki$$name$ = %s(7,\"Natsuki\")$female$ = %i(1,00000001)$voice$ = $female2$:s}"
    ddlcstr = ddlcstr + "\n:i :s{$struct$ = $MOD_DDLC_Sayori$$name$ = %s(6,\"Sayori\")$female$ = %i(1,00000001)$voice$ = $female2$:s}"
    ddlcstr = ddlcstr + "\n:i :s{$struct$ = $MOD_DDLC_Yuri$$name$ = %s(4,\"Yuri\")$female$ = %i(1,00000001)$voice$ = $female2$:s}\n"

    casm0 = casm0.replace("$$$DDLC$$$", ddlcstr)

    i = 0
    #checks for all skin files
    fpath = Path('Data\models\\ab_mod\mods')
    for file in os.listdir(fpath):
        if file.endswith("skin.xbx"):
            print("File Found: "+os.path.join(fpath, file))
            fname = file[:-9]
            ftex = fname+'.tex.xbx'
            if Path(os.path.join(fpath, ftex)).is_file():
                print("File Found: "+os.path.join(fpath, ftex))
                chrdata = processChrs(fpath,fname)
                if chrdata:
                    print("Character \""+fname+"\" loaded successfully!\n")

                    apMod = "\n:i $appearance_MOD_"+str(i)+"$ = :s{\n:i $body$ = :s{$desc_id$ = $MOD_"+str(i)+"$:s}\n:i $board$ = :s{$desc_id$ = $default$:s}\n:i :s}"
                    casm0 = casm0 + apMod

                    modpath = "models/ab_mod/mods/"+fname+".skin"
                    modtext = "\n:i :s{\n:i $desc_id$ = $MOD_"+str(i)+"$\n:i $frontend_desc$ = %sc("+str(len(chrdata['display_name']))+",\""+chrdata['display_name']+"\")\n:i $mesh$ = %s("+str(len(modpath))+",\""+modpath+"\")\n:i :s}"
                    casm1 = casm1 + modtext
                    casm2 = casm2 + modtext
                    casf1  = casf1  + modtext

                    mme1 = mme1 + "\n:i :s{\n:i $display_name$ = %s("+str(len(chrdata['display_name']))+",\""+chrdata['display_name']+"\")\n:i $ped_appearance_structure$ = $appearance_MOD_"+str(i)+"$\n:i $ped_group_flag$ = $LEVEL_UNLOCKED_BO$\n:i $tag_texture$ = %s(11,\"tags\cas_01\")\n:i :s}"
                    
                    i = i + 1
                else:
                    return False
            else:
                print("Error: No tex file found for '"+fname+"' - skipping file...")

    mme1 = mme1 + "\n:i :s{\n:i $display_name$ = %s(6,\"Monika\")\n:i $ped_appearance_structure$ = $MOD_DDLC_Monika$\n:i $ped_group_flag$ = $LEVEL_UNLOCKED_BO$\n:i $tag_texture$ = %s(11,\"tags\cas_01\")\n:i :s}"
    mme1 = mme1 + "\n:i :s{\n:i $display_name$ = %s(7,\"Natsuki\")\n:i $ped_appearance_structure$ = $MOD_DDLC_Natsuki$\n:i $ped_group_flag$ = $LEVEL_UNLOCKED_BO$\n:i $tag_texture$ = %s(11,\"tags\cas_01\")\n:i :s}"
    mme1 = mme1 + "\n:i :s{\n:i $display_name$ = %s(6,\"Sayori\")\n:i $ped_appearance_structure$ = $MOD_DDLC_Sayori$\n:i $ped_group_flag$ = $LEVEL_UNLOCKED_BO$\n:i $tag_texture$ = %s(11,\"tags\cas_01\")\n:i :s}"
    mme1 = mme1 + "\n:i :s{\n:i $display_name$ = %s(4,\"Yuri\")\n:i $ped_appearance_structure$ = $MOD_DDLC_Yuri$\n:i $ped_group_flag$ = $LEVEL_UNLOCKED_BO$\n:i $tag_texture$ = %s(11,\"tags\cas_01\")\n:i :s}"

    print("All characters loaded successfully!\n")
    return True
    #endregion

def startGetFiles():
    #region
    if getAllChrs():

        global casm
        casm = casm0 + "\n" + casm1 + "\n" + casm2 + "\n" + casm3
        f= open("T2CMT Data\cas_skater_m","w+")
        f.write(casm)
        f.close()
        p = Popen(["T2CMT Data\\roq.exe", "-c","T2CMT Data\cas_skater_m"])
        p.wait()

        global casf
        casf = casf1 + "\n" + casf2
        f= open("T2CMT Data\cas_skater_f","w+")
        f.write(casf)
        f.close()
        p = Popen(["T2CMT Data\\roq.exe", "-c","T2CMT Data\cas_skater_f"])
        p.wait()
        
        global mme
        mme = mme1 + "\n" + mme2
        f= open("T2CMT Data\mainmenu_Scripts","w+")
        f.write(mme)
        f.close()
        p = Popen(["T2CMT Data\\roq.exe", "-c","T2CMT Data\mainmenu_Scripts"])
        p.wait()
        
        print("Compiling complete!\n")

        print("Copying files... ", end='')
        if Path('T2CMT Data\mainmenu_Scripts.qb').is_file():
            shutil.copy2(Path('T2CMT Data\mainmenu_Scripts.qb'), Path('Data\levels\mainmenu\mainmenu_Scripts.qb'))
        if Path('T2CMT Data\cas_skater_f.qb').is_file():
            shutil.copy2(Path('T2CMT Data\cas_skater_f.qb'), Path('Data\scripts\game\cas_skater_f.qb'))
        if Path('T2CMT Data\cas_skater_m.qb').is_file():
            shutil.copy2(Path('T2CMT Data\cas_skater_m.qb'), Path('Data\scripts\game\cas_skater_m.qb'))
        print("Complete\n")
        print("All characters installed successfully!\n")
        print("Press any key to exit...")
        msvcrt.getch()
    else:
        print("ERROR - Please try again")  
    #endregion

def MainCode():
    #region
    print ("Welcome to the THUG2 Character Mod Tool\n\nPlease make sure character files have been copied to: '"+os.getcwd()+"\Data\models\\ab_mod\mods'\n")
    print("Press F to open the folder or press any other key to continue...")
    folder = msvcrt.getch().decode('ASCII').upper()
    if folder != "F":
        startGetFiles()
    else:
        os.startfile(os.getcwd()+"\Data\models\\ab_mod\mods")
        print("\nWhen you are ready press any key to continue...")
        msvcrt.getch()  
        startGetFiles()
    #endregion

#start
casm  = ""
casm0 = ""
casm1 = ":i $body$ = :a{"
casm2 = ""
casm3 = ""
casf  = ""
casf1 = ""
casf2 = ""
mme   = ""
mme1  = ""
mme2  = ""
check = checkFiles()
if check == False:
    print ("Welcome to the THUG2 Character Mod Tool\n\nPlease copy the contents of the T2CMT folder to your THUG2 directory then restart the program.\n")
    print("Press any key to exit...")
    msvcrt.getch()
else:
    MainCode()