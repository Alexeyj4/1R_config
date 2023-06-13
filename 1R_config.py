title="1Р конфигуратор v1.0"

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import serial
import configparser
import time

com_port_opened = 0 #com port opened flag

config = configparser.ConfigParser()  # создаём объекта парсера
try:
    config.read("settings.ini")  # читаем конфиг    
    port=config["settings"]["port"]
    rx_freq=float(config["settings"]["rx_freq"])
    tx_freq=float(config["settings"]["tx_freq"])
    squelch=int(config["settings"]["squelch"])    
    volume=int(config["settings"]["volume"])    
except:
    messagebox.showerror("Ошибка","Ошибка в файле settings.ini")

def write_settings():
    config.set("settings","port",ent_com_port.get())
    config.set("settings","rx_freq",ent_rx_freq.get())
    config.set("settings","tx_freq",ent_tx_freq.get())
    config.set("settings","squelch",ent_squelch.get())    
    config.set("settings","volume",ent_volume.get())
    with open("settings.ini", "w") as config_file:
        config.write(config_file)

def open_com_port():
    global com_port_opened    
    if(com_port_opened==0):
        try:
            global ser
            ser = serial.Serial(ent_com_port.get(),9600)
            com_port_opened=1
        except:
            messagebox.showerror("Ошибка!","Не удалось открыть COM-порт "+ent_com_port.get())
            com_port_opened=0

def writeln(s):
    ser.write(s.encode('ascii'))
    ser.write('\r'.encode('ascii')) #cr
    ser.write('\n'.encode('ascii')) #lf    
    stx_monitor.insert(INSERT,s+'\r'+'\n')

def write(s):
    ser.write(s.encode('ascii'))   
    stx_monitor.insert(INSERT,s)

def handshake():
    open_com_port()
    write_settings()
    writeln("AT+DMOCONNECT")
    
def write_rx(): #AT+DMOSETGROUP=0,134.0000,171.8500,0000,1,0000
    open_com_port()
    write_settings()
    rx_freq=float(ent_rx_freq.get())
    volume=int(ent_volume.get())
    squelch=int(ent_squelch.get())
    write("AT+DMOSETGROUP=0,134.0000,")    
    write(str('%.4f' % rx_freq))
    write(",0000,")
    write(str(squelch))
    writeln(",0000")    
    time.sleep(0.5)
    write("AT+DMOSETVOLUME=")
    writeln(str(volume))

def write_tx():
    open_com_port()
    write_settings()
    tx_freq=float(ent_tx_freq.get())
    write("AT+DMOSETGROUP=0,")    
    write(str('%.4f' % tx_freq))
    writeln(",174.0000,0000,0,0000")

window = Tk()
window.title(title)

window.title(title+" - "+port)

frm_handshake=Frame(window)
btn_handshake=Button(frm_handshake,text="Проверка программатора (подключите разъём). Должен быть ответ[+DMOCONNECT:0]",command=handshake)
btn_handshake.pack()
frm_handshake.pack()

lbl_com_port=Label(frm_handshake,text="COM-порт (см.в диспетчере устройств):")
ent_com_port=Entry(frm_handshake)                  
ent_com_port.insert(0,port)
lbl_com_port.pack()
ent_com_port.pack()


frm_rx=Frame(window)
lbl_rx_freq=Label(frm_rx,text="Частота приёма ретранслятора:")
ent_rx_freq=Entry(frm_rx)                  
ent_rx_freq.insert(0,rx_freq)
btn_write_rx=Button(frm_rx,text="Запись настроек приёма (подключите разъём)",command=write_rx)
lbl_rx_freq.pack()
ent_rx_freq.pack()
lbl_volume=Label(frm_rx,text="Уровень модуляции ретранслятора (0-8):")
lbl_volume.pack()
ent_volume=Entry(frm_rx)                  
ent_volume.insert(0,volume)
ent_volume.pack()
lbl_squelch=Label(frm_rx,text="Чувствительность приёма ретранслятора (0-8):")
lbl_squelch.pack()
ent_squelch=Entry(frm_rx)                  
ent_squelch.insert(0,squelch)
ent_squelch.pack()
btn_write_rx.pack()
frm_rx.pack()

frm_tx=Frame(window)
lbl_tx_freq=Label(frm_tx,text="Частота передачи ретранслятора:")
ent_tx_freq=Entry(frm_tx)                  
ent_tx_freq.insert(0,tx_freq)
btn_write_tx=Button(frm_tx,text="Запись настроек передачи (подключите разъём)",command=write_tx)
lbl_tx_freq.pack()
ent_tx_freq.pack()
btn_write_tx.pack()
frm_tx.pack()

frm_monitor=Frame(window)
stx_monitor=scrolledtext.ScrolledText(frm_monitor,width = 50,height = 30)
lbl_monitor=Label(frm_monitor,text="Монитор. [+DMOSETGROUP:0] - значит настройка прошла успешно")
lbl_monitor.pack()
stx_monitor.pack()
frm_monitor.pack()



def loop1():
    global com_port_opened
    if(com_port_opened==1):
        while(ser.inWaiting()>0):
            stx_monitor.insert(INSERT,ser.read())

    window.after(100, loop1)
    
loop1()

window.mainloop()
