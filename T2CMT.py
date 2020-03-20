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
    if Path('T2CMT Data\skater_profile_s.txt').is_file():
        global skp1
        f=open("T2CMT Data\skater_profile_s.txt", "r")
        if f.mode == 'r':
           skp1 =f.read()
    else:
        return False
    if Path('T2CMT Data\skater_profile_e.txt').is_file():
        global skp2
        f=open("T2CMT Data\skater_profile_e.txt", "r")
        if f.mode == 'r':
           skp2 =f.read()
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

def getValidInt(displaymes, minval, maxval):
    #region
    error = "Error: Invalid Integer - Please try again!"
    while True:
        string = input(displaymes)
        if string.strip():
            if string.isdigit():
                if int(string) >= minval and int(string) <= maxval:
                    break
                else: 
                    print(error)   
            else: 
                print(error)   
        else:
            print(error)       
    return string
    #endregion

def saveChrAttribute(text, info, fname, isint=0, minval=0, maxval=255):
    #region
    if len(info) > 0:
        info = "("+info+") "
    if isint == 1:
        value = int(getValidInt("Enter \""+text+"\" "+info+"for \""+fname+"\": ",minval, maxval))
    else:
        value = getValidString("Enter \""+text+"\" "+info+"for \""+fname+"\": ")
    return value
    #endregion

def createChrData(fname, data, outfile):
    #region
    #--display_name$ = %s(4,"NAME")
    #--first_name$ = %s(1,"A")
    #--last_name$ = %s(1,"B")
    #--voice$ = $female2$
    #--stance$ = $regular$
    #--pushstyle$ = $never_mongo$ // always_mongo // mongo_when_switch
    #--trickstyle$ = $street$
    #--is_male$ = %i(0,00000000)
    #--air$ = %i(10,0000000a)
    #--run$ = %i(10,0000000a)
    #--ollie$ = %i(10,0000000a)
    #--speed$ = %i(10,0000000a)
    #--spin$ = %i(10,0000000a)
    #--switch$ = %i(10,0000000a)
    #--flip_speed$ = %i(10,0000000a)
    #--rail_balance$ = %i(10,0000000a)
    #--lip_balance$ = %i(10,0000000a)
    #--manual_balance$ = %i(10,0000000a)    

    class Attribute:
        def __init__(self, name, text, info, isint, minval, maxval):
            self.name = name
            self.text = text
            self.info = info
            self.isint = isint
            self.minval = minval
            self.maxval = maxval
    
    catts = [
        Attribute("display_name","Display Name","",0,0,0),
        Attribute("first_name","First Name","",0,0,0),
        Attribute("last_name","Last Name","",0,0,0),
        Attribute("is_male","Gender","Male = 1, Female = 2",1,1,2),
        Attribute("voice","Voice","Male 1-4 = 1-4, Female 1-2 = 5-6",1,1,6),   
        Attribute("stance","Stance","Regular = 1, Goofy = 2",1,1,2),
        Attribute("pushstyle","Push Style","Never Mongo = 1, Mongo Switch = 2, Always Mongo = 3",1,1,3),        
        Attribute("trickstyle","Trick Style","Street = 1, Vert = 2",1,1,2)
    ]

    cstats = [
        Attribute("air","Air Stat Value","1-10",1,1,10),
        Attribute("run","Run Stat Value","1-10",1,1,10),
        Attribute("ollie","Ollie Stat Value","1-10",1,1,10),
        Attribute("speed","Speed Stat Value","1-10",1,1,10),
        Attribute("spin","Spin Stat Value","1-10",1,1,10),
        Attribute("switch","Switch Stat Value","1-10",1,1,10),
        Attribute("flip_speed","Flip Speed Stat Value","1-10",1,1,10),
        Attribute("rail_balance","Rail Balance Stat Value","1-10",1,1,10),
        Attribute("lip_balance","Lip Balance Stat Value","1-10",1,1,10),
        Attribute("manual_balance","Manual Balance Stat Value","1-10",1,1,10),
    ]

    for c in catts:
        if data.get(c.name):
            print(fname + " "+c.text+": " +str(data[c.name]))
        else:
            data[c.name] = saveChrAttribute(c.text, c.info, fname, c.isint, c.minval, c.maxval)
    
    if not data.get("all_stats"):
        data["all_stats"] = saveChrAttribute("Global Stats Value", "1-10 - Enter 0 to edit individual stats", fname, 1, 0, 10)
        if data["all_stats"] == 0:
            data["all_stats"] = "-"

    if data["all_stats"] != "-":
        print(fname + " Global Stats Value: " +str(data["all_stats"]))
    else:
        for s in cstats:
            if data.get(s.name):
                print(fname + " "+s.text+": " +str(data[s.name]))
            else:
                data[s.name] = saveChrAttribute(s.text, s.info, fname, s.isint, s.minval, s.maxval) 

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
    global skp1
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

                    pft =       "\n:i :s{\n:i $display_name$ = %s("+str(len(chrdata['display_name']))+",\""+chrdata['display_name']+"\")\n"
                    pft = pft + ":i $first_name$ = %s("+str(len(chrdata['first_name']))+",\""+chrdata['first_name']+"\")\n"
                    pft = pft + ":i $last_name$ = %s("+str(len(chrdata['last_name']))+",\""+chrdata['last_name']+"\")\n"
                    pft = pft + ":i $default_appearance$ = $appearance_MOD_"+str(i)+"$\n"
                    pft = pft + ":i $name$ = $MOD_"+str(i)+"$\n"


                    if chrdata["stance"] == 1:
                        stance = "regular"
                    else:
                        stance = "goofy"

                    pft = pft + ":i $stance$ = $"+stance+"$\n"

                    if chrdata["pushstyle"] == 1:
                        pushstyle = "never_mongo"
                    elif chrdata["stance"] == 2:
                        pushstyle = "mongo_when_switch"
                    else:
                        pushstyle = "always_mongo"

                    pft = pft + ":i $pushstyle$ = $"+pushstyle+"$\n"

                    if chrdata["trickstyle"] == 1:
                        trickstyle = "street"
                    else:
                        trickstyle = "vert"

                    pft = pft + ":i $trickstyle$ = $"+trickstyle+"$\n"


                    pft = pft + ":i $tag_texture$ = %s(12,\"tags\cas_01\")\n"
                    pft = pft + ":i $skater_family$ = $family_custom$\n"
                    pft = pft + ":i $is_pro$ = %i(0,00000000)\n"
                    pft = pft + ":i $is_head_locked$ = %i(0,00000000)\n"
                    pft = pft + ":i $is_locked$ = %i(0,00000000)\n"
                    pft = pft + ":i $is_hidden$ = %i(0,00000000)\n"

                    if chrdata["is_male"] == 2:
                        is_m =  0
                    else:
                        is_m = 1
                    tohex = "{0:0{1}x}".format(is_m,8)
                    pft = pft + ":i $is_male$ = %i("+str(is_m)+","+str(tohex)+")\n"

                    pft = pft + ":i $points_available$ = %i(0,00000000)\n"

                    if chrdata["all_stats"] == "-":
                        tohex = "{0:0{1}x}".format(chrdata["air"],8) 
                        pft = pft + ":i $air$ = %i("+str(chrdata["air"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["run"],8) 
                        pft = pft + ":i $run$ = %i("+str(chrdata["run"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["ollie"],8) 
                        pft = pft + ":i $ollie$ = %i("+str(chrdata["ollie"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["speed"],8) 
                        pft = pft + ":i $speed$ = %i("+str(chrdata["speed"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["spin"],8) 
                        pft = pft + ":i $spin$ = %i("+str(chrdata["spin"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["switch"],8) 
                        pft = pft + ":i $switch$ = %i("+str(chrdata["switch"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["flip_speed"],8) 
                        pft = pft + ":i $flip_speed$ = %i("+str(chrdata["flip_speed"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["rail_balance"],8) 
                        pft = pft + ":i $rail_balance$ = %i("+str(chrdata["rail_balance"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["lip_balance"],8) 
                        pft = pft + ":i $lip_balance$ = %i("+str(chrdata["lip_balance"])+","+str(tohex)+")\n"
                        tohex = "{0:0{1}x}".format(chrdata["manual_balance"],8) 
                        pft = pft + ":i $manual_balance$ = %i("+str(chrdata["manual_balance"])+","+str(tohex)+")\n"
                    else:
                        tohex = "{0:0{1}x}".format(chrdata["all_stats"],8) 
                        pft = pft + ":i $air$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $run$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $ollie$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $speed$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $spin$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $switch$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $flip_speed$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $rail_balance$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $lip_balance$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"
                        pft = pft + ":i $manual_balance$ = %i("+str(chrdata["all_stats"])+","+str(tohex)+")\n"

                    pft = pft + ":i $sponsors$ = :a{:a}\n"
                    pft = pft + ":i $trick_mapping$ = :s{:s}\n"
                    pft = pft + ":i $default_trick_mapping$ = $CustomTricks$\n"
                    pft = pft + ":i $max_specials$ = %i(12,0000000c)\n"
                    pft = pft + ":i $specials$ = :s{\n"
                    pft = pft + ":i :a{\n"
                    pft = pft + ":i :s{$trickslot$ = $SpAir_R_D_Circle$$trickname$ = $Trick_McTwist$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $SpAir_U_R_Square$$trickname$ = $Trick_KickFlipUnderFlip$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $SpGrind_R_D_Triangle$$trickname$ = $Trick_tailblockslide$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $SpMan_D_U_Triangle$$trickname$ = $Trick_OneFootOneWheel$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :s{$trickslot$ = $Unassigned$$trickname$ = $Unassigned$:s}\n"
                    pft = pft + ":i :a}\n"
                    pft = pft + ":i :s}\n"

                    if chrdata["voice"] >= 5:
                        voice = "female" + str(chrdata["voice"]-4)
                    else:
                        voice = "male" + str(chrdata["voice"])
                    
                    pft = pft + ":i $voice$ = $"+voice+"$\n"

                    pft = pft + ":i :s}"
                    skp1 = skp1 + pft
                    i = i + 1
                else:
                    return False
            else:
                print("Error: No tex file found for '"+fname+"' - skipping file...")
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
        
        global skp
        skp = skp1 + "\n" + skp2
        f= open("T2CMT Data\skater_profile","w+")
        f.write(skp)
        f.close()
        p = Popen(["T2CMT Data\\roq.exe", "-c","T2CMT Data\skater_profile"])
        p.wait()
        
        print("Compiling complete!\n")

        print("Copying files... ", end='')
        if Path('T2CMT Data\skater_profile.qb').is_file():
            shutil.copy2(Path('T2CMT Data\skater_profile.qb'), Path('Data\scripts\game\skater\skater_profile.qb'))
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
skp   = ""
skp1  = ""
skp2  = ""
check = checkFiles()
if check == False:
    print ("Welcome to the THUG2 Character Mod Tool\n\nPlease copy the contents of the T2CMT folder to your THUG2 directory then restart the program.\n")
    print("Press any key to exit...")
    msvcrt.getch()
else:
    MainCode()