# -*- coding:utf8 -*-
import tkinter as tk
import datetime as dt
import subWindow as sw
import jsonIO

#[button] -> window -> I/O
def saveTask(bL,win):
    #dict tsk
    tsk = {"title":bL["title"].get(),
            "priority":bL["priority"].get(),
           "date":bL["date"].get(),
           "kind":bL["kind"].get(),
           "favorit":0,
           "comment":bL["comment"].get()}
    gTaskList.append(tsk)
    jsonIO.saveJson(tsk)
    renewTsk(gTaskList)
    win.destroy()

#event -> void
def addTskWin(event):
    global subW
    if subW is None or not subW.winfo_exists(): 
        subW = tk.Toplevel()
        subW.title("タスクを追加")
        aW = sw.InputWindow(subW,dt.datetime.today())
        aW.packWidget()
        aW.tEntry.focus_set()

#event -> int -> void
def pushed(i):
    def x():
        global subW
        if subW is None or not subW.winfo_exists():
            subW = tk.Toplevel()
            subW.title("タスクを編集")
            eW = sw.InputWindow(subW,dt.datetime.today(),btnTaskList[i])#ボタンに対応するタスクの情報を取りたい
            eW.packWidget()
            eW.tEntry.focus_set()
    

#[task] -> [button]
#ボタンの生成&初期設定を行う
def btnLGen(tskL,i=0):
    if len(tskL) != 0:
        btnText = tskL[0]["title"] + "\n" + "date:" + tskL[0]["date"]
        btn = tk.Button(tskFrame,text=btnText)#,command=pushed(i))
        #print(btngTaskList)
        btnTaskList.append(tskL[0])
        return [btn] + btnLGen(tskL[1:],i+1)
    else:
        print("btnLGen END")
        return []
    
#buttn -> int -> void
def cmdSet(btnL,i=0):
    if len(btnL) != 0:
        #eWGen = lambda i:pushed(i)
        btnL[0].bind("<1>",lambda i:pushed(i))
        cmdSet(btnL[1:],i+1)
    else:
        pass
    
#[button] -> [task] -> void
#ボタンを出現させる
def btnGen(btnL,tskL):
    if len(btnL) != 0:
        btnL[0].pack(fill="both")
        if tskL[0]["favorit"] == 1:
            lbl = tk.Label(btnL[0],text="★")
        else:
            lbl = tk.Label(btnL[0],text="☆")
        lbl.pack(side="right")
        btnGen(btnL[1:],tskL[1:])
    else:
        pass

        
# frame -> I/O
def frameClear(frm):
    widL = frm.pack_slaves()
    #print(widL)
    for l in widL:
        l.destroy()
    
# void -> I/O
def tskSort(self):
    if svSortV == menuBar.sortV:
        pass
    elif menuBar.sortV.get() == "優先度":
        btnTaskList.sort(key= lambda x:x["priority"])
        btnTaskList.reverse()
    else:
        btnTaskList.sort(key= lambda x:x["date"])
    renewTsk(btnTaskList)

# void -> I/O
def tskFilt(self):
    if menuBar.filtV.get() == "すべて":
        btnTaskList = gTaskList
    else:
        btnTaskList = [k for k in gTaskList if k["kind"] == menuBar.filtV.get()]
    renewTsk(btnTaskList)
    pass

# [task] -> I/O
def renewTsk(tskL):
    global btnTaskList
    frameClear(tskFrame)
    print("btnTaskList:",btnTaskList)
    btnTaskList = []
    btnList = btnLGen(tskL)
    print("btnList:",btnList)
    cmdSet(btnList)
    btnGen(btnList,tskL)

#---------------------------------------------
gTaskList = jsonIO.inportJson()
subW = None
svSortV = None
btnTaskList = []
sw.saveTask = saveTask

#-------メインウィンドウ----------
root = tk.Tk()
root.title(u"Tasksack")
root.geometry("300x400")

#--------メニューバー-------------
menuBar = sw.MnBar(root)
menuBar.sortBtn.focus_set() #ウィンドウ生成時sortボタンにフォーカス
#-------------------------------

#--------上部メニュー&ボタン生成----------------
spFrame = tk.Frame(root,bd=0,relief="ridge")
sortBtn = tk.Button(spFrame,text="to sort")
sortBtn.bind("<1>",tskSort)
filtBtn = tk.Button(spFrame,text="to filter")
filtBtn.bind("<1>",tskFilt)
addBtn = tk.Button(spFrame,text="+")
addBtn.bind("<1>",addTskWin)

spFrame.pack(fill="x")
sortBtn.pack(side="left")
filtBtn.pack(side="left")
addBtn.pack(side="right")
#----------------------------

#---------タスクリスト-----------
tskFrame = tk.Frame(root,bd=2,relief="ridge")
tskFrame.pack(fill="both")

renewTsk(gTaskList)
#----------------------------



root.mainloop()
#---------------------------