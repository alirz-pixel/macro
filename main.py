import keyboard
import tkinter as tk

key = ""
selected = -1
special_keys={}
str_Option = 0
cup = "" 

#키보드 추가 함수
def Add_Key(fun,caller):# caller= 부르는 곳으로 설정 ex)ListBox, Option
    global key,str_Option
    
    if key != "":
        key = ""

    def Change_Str():
        global str_Option
        if str_Option == 0:
            str_Option = 1
        else:
            str_Option = 0

        win_AddKey.destroy()
        Add_Keyboard()

    def key_down(e):
        global str_Option

        if str_Option == 0:
            global key

            if key != e.keysym:
                key = e.keysym
                AddKey_Text["text"] = key
                print("키 입력 : " + str(key))

    def CompleteGetKey():
        global cup
        try:
            if en_AddStr.get()!="":
                listBox.insert(tk.END, " str : " + en_AddStr.get())
        except:
            fun()

        win_AddKey.destroy()
        
    win_AddKey = tk.Tk()
    win_AddKey.title("키보드 설정")
    win_AddKey.geometry("200x160")
    win_AddKey.lift() #창을 맨 위로 올리는 설정입니다.
    win_AddKey.attributes("-topmost", True) #창을 맨 위로 올리는 설정입니다.
    win_AddKey.attributes('-toolwindow', True)
    win_AddKey.bind("<KeyPress>", key_down) #키보드 입력 받기

    AddKey_Label = tk.Label(master=win_AddKey, text='추가할 키를 입력해 주세요.')
    AddKey_Label.place(x=23, y=10)

    if caller=="ListBox":
        bu_Change = tk.Checkbutton(master=win_AddKey, text='키 입력', command=Change_Str)
        bu_Change.place(x=52, y=68)
    elif "Option" in caller:
        str_Option=0

    if str_Option == 0:
        AddKey_Text = tk.Label(master=win_AddKey, text=' ', font=("System", 5), relief='sunken')
        AddKey_Text.config(bg='LightGray')
        AddKey_Text.place(x=25, y=33, width=150, height=32)

    else:
        en_AddStr = tk.Entry(master=win_AddKey, font=("System", 5), relief='sunken', justify='center')
        en_AddStr.config(bg='LightGray')
        en_AddStr.place(x=25, y=33, width=150, height=32)    


    Add_Btn = tk.Button(master=win_AddKey, text="완료", command=CompleteGetKey)

    Add_Btn.place(x=70, y=120, width=60, height=25)

    win_AddKey.mainloop()

def Add_Keyboard():
    def Add_KeyboardMain():
        global key
        listBox.insert(tk.END, " key : " + key)
    Add_Key(Add_KeyboardMain,caller="ListBox")

#ListBox 내용 삭제 함수
def Delete_ListBox():
    global selected

    if selected >= 0:  # Check this still isn't -1
        listBox.delete(selected)
        selected = -1
    else:
        print("Error", "Can't delete the selected item if you haven't selected anything!")

#ListBox seleted 함수
def list_clicked(e):
    print(e)
    global selected
    selected = int(listBox.curselection()[0])  # item number selected in list
    item = listBox.get(selected)  # text of selected item
    print(f"You have clicked item {selected} which is {item} | type is {type(item)}")

#특정 키를 눌렀을 때, 매크로 시작하기
def Macro_Start():
    win.after(100, Macro_Start)

    if keyboard.is_pressed(special_keys['start']):
        print("ha!")
        for i in range(listBox.size()):
            item_Formet = listBox.get(i).split()[0]  #키 입력 또는 문자열 출력 등을 구분하는 변수
            item_Content = listBox.get(i).split()[2] #리스트 박스에 들어있는 내용을 담는 변수
            print(f'now i is {i} | and | item is {item_Formet}')

            if item_Formet == 'str':
                keyboard.write(item_Content)
            elif item_Formet == 'key':
                keyboard.press_and_release(item_Content)

#옵션가져오기 
def Get_Option():
    global special_keys
    try:
        f=open("option.txt",'r')
        cup=list(f.readline().strip('\n').split())
        while cup!=list(''):
            special_keys[cup[0]]=cup[2]
            cup=list(f.readline().strip('\n').split())
        f.close()
        #옵션에서 조정 가능한 키 출력. 
        print("매크로 시작 키:"+special_keys['start']+" 매크로 중지 키 :"+special_keys['stop'])

    except: #첫 실행시 또는 옵션txt파일에 문제 있을 시 초기화후 실행
        f=open("option.txt",'w')
        f.write('start = F3\n')
        f.write('stop = F2\n')
        f.close()
        f=open("option.txt",'r')
        cup=list(f.readline().strip('\n').split())
        while cup!=list(''):
            special_keys[cup[0]]=cup[2]
            cup=list(f.readline().strip('\n').split())
        f.close()
        print("매크로 시작 키:"+special_keys['start']+" 매크로 중지 키 :"+special_keys['stop'])

def Open_option():
    start=special_keys['start']
    stop=special_keys['stop']
    def GetKeyStart():
        global key
        def GetKeyStartMain():
            global start
            start=key
            la_bstart.configure(text="start = "+key)
        Add_Key(GetKeyStartMain,caller="OptionStart")
    def GetKeyStop():
        global key
        def GetKeyStopMain():
            global stop
            stop=key
            la_bstop.configure(text="stop = "+key)
        Add_Key(GetKeyStopMain,caller="OptionStop")
                               
    def Save_option():
        global special_keys, start, stop
        special_keys['start']=start
        special_keys['stop']=stop
        f=open("option.txt",'w')
        f.write("start = "+special_keys['start']+"\n")
        f.write("stop = "+special_keys['stop']+"\n")
        f.close()
        la_bstart.configure(text="start = "+special_keys['start'])
        la_bstop.configure(text="start = "+special_keys['stop'])
        print("옵션 저장 완료")
        win_option.destroy()
        
    win_option = tk.Tk()
    win_option.title("옵션")
    win_option.geometry("200x120")
    win_option.attributes('-toolwindow', True)

    la_bstart=tk.Label(win_option,text="start = "+special_keys['start'])
    bu_astart=tk.Button(win_option,text="변경",relief='sunken',command=GetKeyStart)
    la_bstop=tk.Label(win_option,text="stop = "+special_keys['stop'])
    bu_astop=tk.Button(win_option,text="변경",relief='sunken',command=GetKeyStop)
    bu_save=tk.Button(win_option,text="완료",command=Save_option)
    la_bstart.place(x=13, y= 17)
    bu_astart.place(x=120,y=17)
    la_bstop.place(x=13, y= 40)
    bu_astop.place(x=120,y=40)
    bu_save.place(x=40, y=80, width=130, height=20)

    win_option.mainloop()
#tk 기본 설정
win = tk.Tk()
win.title("Py Macro")
win.geometry("250x190")

#옵션 가져오기
Get_Option()

#메뉴생성
menu=tk.Menu(win)
menu_list=tk.Menu(menu,tearoff=0)
menu_list.add_command(label='옵션',command=Open_option)
menu_list.add_separator()
menu_list.add_command(label='저장')
menu_list.add_command(label='불러오기')

menu.add_cascade(label="파일 및 옵션",menu=menu_list)

win.config(menu=menu)
#listbox 생성
listBox = tk.Listbox(win, borderwidth=3)
listBox.place(x=13, y=17, width=130, height=140)

#selected is ListBox element
listBox.bind('<<ListboxSelect>>', list_clicked)

#키보드 추가 박스 생성
Key_Box = tk.Button(win, text="키보드", borderwidth=2, command=Add_Keyboard)
Key_Box.place(x=155, y=17, width=70, height=30)

#마우스 추가 박스 생성
Mouse_Box = tk.Button(win, text="마우스", borderwidth=2)
Mouse_Box.place(x=155, y=52, width=70, height=30)

#시간 추가 박스 생성
Mouse_Box = tk.Button(win, text="시간", borderwidth=2)
Mouse_Box.place(x=155, y=87, width=70, height=30)

#지우기 박스 생성
Mouse_Box = tk.Button(win, text="지우기", borderwidth=2, command=Delete_ListBox)
Mouse_Box.place(x=155, y=122, width=70, height=30)

#매크로 실행
Macro_Start()

tk.mainloop()
