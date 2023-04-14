title="1Р конфигуратор v1.0"

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import serial
import configparser
import time

config = configparser.ConfigParser()  # создаём объекта парсера
try:
    config.read("settings.ini")  # читаем конфиг    
    port=config["settings"]["port"]
    rx_freq=float(config["settings"]["rx_freq"])
    tx_freq=float(config["settings"]["tx_freq"])
    volume=int(config["settings"]["volume"])    
except:
    messagebox.showerror("Ошибка","Ошибка в ini-файле")

try:
    ser = serial.Serial(port,9600)
except:
    messagebox.showerror("Ошибка!","Не удалось открыть COM-порт "+port)
    

def writeln(s):
    ser.write(s.encode('ascii'))
    ser.write('\r'.encode('ascii')) #cr
    ser.write('\n'.encode('ascii')) #lf    
    stx_monitor.insert(INSERT,s+'\r'+'\n')

def write(s):
    ser.write(s.encode('ascii'))   
    stx_monitor.insert(INSERT,s)

def handshake():
    writeln("AT+DMOCONNECT")
    
def write_rx(): #AT+DMOSETGROUP=0,134.0000,171.8500,0000,1,0000
    write("AT+DMOSETGROUP=0,134.0000,")    
    write(str('%.4f' % rx_freq))
    writeln(",0000,0,0000")
    time.sleep(0.5)
    write("AT+DMOSETVOLUME=")
    writeln(str(volume))

def write_tx():        
    write("AT+DMOSETGROUP=0,")    
    write(str('%.4f' % tx_freq))
    writeln(",174.0000,0000,0,0000")

window = Tk()
window.title(title)

window.title(title+" - "+port)

frm_handshake=Frame(window)
btn_handshake=Button(frm_handshake,text="Handshake",command=handshake)
btn_handshake.pack()
frm_handshake.pack()

frm_rx=Frame(window)
lbl_rx_freq=Label(frm_rx,text="RX freq:")
ent_rx_freq=Entry(frm_rx)                  
ent_rx_freq.insert(0,rx_freq)
btn_write_rx=Button(frm_rx,text="Записать RX",command=write_rx)
lbl_rx_freq.pack()
ent_rx_freq.pack()
lbl_volume=Label(frm_rx,text="Volume:")
lbl_volume.pack()
ent_volume=Entry(frm_rx)                  
ent_volume.insert(0,volume)
ent_volume.pack()
btn_write_rx.pack()
frm_rx.pack()

frm_tx=Frame(window)
lbl_tx_freq=Label(frm_tx,text="TX freq:")
ent_tx_freq=Entry(frm_tx)                  
ent_tx_freq.insert(0,tx_freq)
btn_write_tx=Button(frm_tx,text="Записать TX",command=write_tx)
lbl_tx_freq.pack()
ent_tx_freq.pack()
btn_write_tx.pack()
frm_tx.pack()

frm_monitor=Frame(window)
stx_monitor=scrolledtext.ScrolledText(frm_monitor,width = 50,height = 30)
lbl_monitor=Label(frm_monitor,text="Монитор:")
lbl_monitor.pack()
stx_monitor.pack()
frm_monitor.pack()






def loop1():
    if ser.inWaiting()>0:
        stx_monitor.insert(INSERT,ser.readline())                               
              

    
    

    window.after(100, loop1)
    
loop1()

window.mainloop()
