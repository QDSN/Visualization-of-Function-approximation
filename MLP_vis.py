# -*- coding: utf-8 -*-
import tkinter
import numpy as np
"""
多層パーセプトロン
"""
#隠れ層の数
Unit_hidden=5
#学習率
eta=0.2
#重み行列
W1=2*np.random.rand(2,Unit_hidden+1)-1
W2=2*np.random.rand(Unit_hidden+1,1)-1
#テストデータ
test=np.arange(1,800)/400-1
#出力関数
def output(x):
    #xはデータ
    temp=np.dot(np.array([[1],[x]]).T,W1)
    t=np.dot(np.tanh(temp),W2)
    return(t[0][0])

def deltak(x,y):
    #x,yは単一のデータ
    return(output(x)-y)
def z_hidj(x,j):
    temp=np.dot(np.array([[1],[x]]).T,W1)
    return(np.tanh(temp)[0][j])
def deltaj(x,y,j):
    return((1-z_hidj(x,j)**2)*W2[j][0]*deltak(x,y))

#重みの更新
def update(x,y):
    global W1
    global W2
    for j in range(Unit_hidden):
        W1[0][j]=W1[0][j]-eta*deltaj(x,y,j)
        W1[1][j]=W1[1][j]-eta*deltaj(x,y,j)*x
        W2[j][0]=W2[j][0]-eta*deltak(x,y)*z_hidj(x,j)

"""

"""
mode=0#1が点を打つ、0が線を引く
points=[]
temp_x=0
temp_y=0
root = tkinter.Tk()
c = tkinter.Canvas(root, width = 800, height = 450)
c.pack()
c.create_rectangle(10, 10, 790, 440,fill="#ffffff")
for i in range(0,10):
    c.create_line(0,45*i,800,45*i,fill = '#87cefa')
    c.create_line(80*i,0,80*i,450,fill='#87cefa')
    c.create_line(400,450,400,0,fill='#4169e1',arrow=tkinter.LAST,width=2)
    c.create_line(0,225,800,225,fill='#4169e1',arrow=tkinter.LAST,width=2)

#関数定義
def getp(event):
    global temp_x,temp_y
    temp_x=event.x
    temp_y=event.y
def create_point(event):
        x=event.x
        y=event.y
        id=c.create_oval(x-3,y-3,x+3,y+3,fill = '#fa3253',tags='draw')
        c.tag_bind(id, '<Button1-Motion>',move_oval)
        points.append([x,y])
def write(event):

    if mode==1:
        create_point(event)
    elif mode==0:
        getp(event)

def move_oval(event):
    x = event.x
    y = event.y
    c.coords("current", x - 3, y - 3, x + 3, y + 3)
def Draw_line(event):
    if mode==0:
        global temp_x,temp_y
        x=event.x
        y=event.y
        c.create_line(temp_x,temp_y,x,y,tags='draw',fill = '#000000')
        getp(event)
def Spinter():
    c.create_line(points, smooth = 1,tags='draw',fill = '#5998ff')
def MLP():
    for k in range(100):
        c.delete('MLP')
        test_list=[]
        x=np.array(points)[:,0]/400-1
        y=np.array(points)[:,1]/225-1
        for j in np.random.permutation(len(x)):
            update(x[j],y[j])
        for i in range(799):
            temp=output(test[i])
            test_list.append([(test[i]+1)*400,(temp+1)*225])
        c.create_line(test_list,tags=('MLP','draw'),fill = '#f78e80',smooth=1)
        c.update()
def eta_change(n):
    global eta
    eta=scale1.get()/100
def Unit_hidden_change(n):
    global Unit_hidden
    Unit_hidden=scale2.get()
    global W1
    global W2
    W1=np.random.rand(2,Unit_hidden+1)
    W2=np.random.rand(Unit_hidden+1,1)
def mode_change(n):
    global mode
    mode=scale3.get()
def delete():
    c.delete('draw')
    global points
    points=[]

c.bind( '<Button-1>', write) #move_ovalの引数は自動的に決まる 多くの引数を渡したいときはλ関数で与える
c.bind( '<Button1-Motion>', Draw_line)
c.bind( '<Button3-Motion>', move_oval)
button1 = tkinter.Button(root, text='Bezier interpolation', command=Spinter,bg='#5998ff')
button1.pack(side=tkinter.LEFT)
button2 = tkinter.Button(root, text='Multilayer Perceptron', command=MLP,bg='#f78e80')
button2.pack(side=tkinter.LEFT)
button_del=tkinter.Button(root, text='delete', command=delete)
button_del.pack(side=tkinter.RIGHT)
scale1 = tkinter.Scale(root, label='learning rate', orient='h', from_=0.01, to=1,resolution=0.01, command=eta_change)
scale1.pack()
scale2 = tkinter.Scale(root, label='hidden layer', orient='h', from_=1, to=100, command=Unit_hidden_change)
scale2.pack()
scale3 = tkinter.Scale(root, label='Mode', orient='h', from_=0, to=1, command=mode_change)
scale3.pack()
root.mainloop()
