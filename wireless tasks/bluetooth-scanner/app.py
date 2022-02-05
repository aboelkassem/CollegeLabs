import bluetooth
from tkinter import *
from tkinter import filedialog as fd
import tkinter.ttk as ttk
import threading
import tkinter.messagebox as messages
from PyOBEX.client import Client
import os
import time

devices = []
tk = Tk()
devicesVar = StringVar(tk, value = devices)
deviceName = StringVar(tk, value = "Device name: None")
deviceMAC = StringVar(tk, value = "Device MAC Address: None")
deviceClass = StringVar(tk, value = "Device Class: None")
sendInput = StringVar(tk)
isConnected = BooleanVar(tk)

btSocket = None
btClient = None
rate = "Data transfer rate:"

messageQueue = []

def scan():
    print("Scanning for bluetooth devices")
    scanButton.state(['disabled'])
    btScanThread = threading.Thread(target = scanSubprocess, name = "btscanthread", daemon = True)
    connectLoader.grid(column=0, row=16, pady=[5,0])
    btScanThread.start()
    while btScanThread.is_alive():
        tk.update()
        tk.update_idletasks()
    print("scan finished")
    scanButton.state(['!disabled'])
    connectLoader.grid_forget()

def recieveListener():
    global messageQueue, isConnected
    while isConnected.get():
        try:
            data = btSocket.recv(1024)
            if len(data) != 0:
                messageQueue.append(data)
        except bluetooth.btcommon.BluetoothError as err:
             messages.showerror(title="Connection Error", message="Connection terminated. \nError: " + str(err) + "\nPlease restart the program.")
        #print("Recieved message")

def connectToDevice(selection):
    global btSocket, btClient
    device = devices[selection[0]]
    addr = device[0]
    btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    service_matches = bluetooth.find_service(name=b'OBEX Object Push\x00', address=addr)
    if len(service_matches) == 0:
        print("Couldn't find bluetooth services.")
        sys.exit(0)
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]
    btClient = Client(addr, port)
    print("Connecting to \"{}\" on {}".format(name, host))
    try:
        print("Paring...")
        btSocket.connect((addr,3))
        print("Connecting....")
        btClient.connect()
        print("Connected successfully")
        deviceName.set("Device name: " + device[1])
        deviceMAC.set("Device MAC Address: " + device[0])
        deviceClass.set("Device class: " + str(device[2]))
        isConnected.set(True)
        recieveThread.start()
        sendButton.state(['!disabled'])
        disconnectButton.state(["!disabled"])
    except bluetooth.btcommon.BluetoothError as err:
        messages.showerror(title="Connection Error", message="Failed to establish RFCOMM socket. \nInfo: " + str(err))

def updateLog():
    for item in messageQueue:
        writeToDataLog("Recieved message > " + item.hex())
        print("Recieved message > " + item.hex())
        messageQueue.remove(item)
    tk.after(1000, updateLog)

def scanSubprocess():
    global devices
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True,
                                            flush_cache=True, duration=5)
    devicesList = []
    for name in devices:
        devicesList.append(name[1])
    devicesVar.set(devicesList)
    print(devicesVar.get())

def disconnectFromDevice(ask = True):
    if ask:
        if messages.askyesno(title='Disconnect???', message="Do you really want to disconnect??? Just want to be sure."):
            isConnected.set(False)
            sendButton.state(['disabled'])
            disconnectButton.state(["disabled"])
            btSocket.close()
            btClient.disconnect()
            deviceName.set("Device name: None")
            deviceMAC.set("Device MAC Address: None")
            deviceClass.set("Device class: None")
    else:
        isConnected.set(False)
        sendButton.state(['disabled'])
        disconnectButton.state(["disabled"])
        btSocket.close()
        deviceName.set("Device name: None")
        deviceMAC.set("Device MAC Address: None")
        deviceClass.set("Device class: None")

def writeToDataLog(msg):
    numlines = int(dataLog.index('end - 1 line').split('.')[0])
    dataLog['state'] = 'normal'
    if numlines==24:
        dataLog.delete(1.0, 2.0)
    if dataLog.index('end-1c')!='1.0':
        dataLog.insert('end', '\n')
    dataLog.insert('end', msg)
    dataLog['state'] = 'disabled'

def selectFile():
    global rate
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filepath = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    with open(filepath, 'rb') as f:
        contents = f.read()
    filename = os.path.basename(filepath)
    filesizeKb = os.path.getsize(filepath) / 1024   # getsize return in bytes
    ts = time.time()
    btClient.put(filename, contents)
    te = time.time()
    rate += " {:.2f} kbps".format(filesizeKb / (te - ts)) # data transfer rate
    rateLabel.config(text=rate)
    print(rate)
    writeToDataLog("Sent file > " + filename)


recieveThread = threading.Thread(target = recieveListener, name = "recievelistenerthread", daemon = True)

tk.geometry("550x500")
tk.title("Bluetooth file transfer")
tk.resizable(0, 0)
tabControl = ttk.Notebook(tk)
connectionTab = ttk.Frame(tabControl)
sendRecieveTab = ttk.Frame(tabControl)
tabControl.add(connectionTab, text='Connection')
tabControl.add(sendRecieveTab, text='Send/Recieve')
tabControl.pack(expand=1, fill="both")

devicesLabel = Label(connectionTab, text="Device info")
devicesLabel.grid(column=1, row=0)

nameLabel = Label(connectionTab, textvariable = deviceName)
nameLabel.grid(column = 1, row = 1, sticky="W", padx = [5,0])
macLabel = Label(connectionTab, textvariable = deviceMAC)
macLabel.grid(column = 1, row = 2, sticky="W", padx = [5,0])
classLabel = Label(connectionTab, textvariable = deviceClass)
classLabel.grid(column = 1, row = 3, sticky="W", padx = [5,0])

scanButton = ttk.Button(connectionTab, text='Scan', command=scan)
scanButton.grid(column=0, row=17, pady=[5,0])

devicesFrame = ttk.Labelframe(connectionTab, text='Devices')
devicesFrame.grid(column=0, row=0, rowspan=10, padx = [5,0], pady = [5,0])
devicesFrame['padding'] = (5, 0, 5, 5)
devicesFrame['relief'] = 'ridge'
devicesListbox = Listbox(devicesFrame, height = 10, listvariable=devicesVar)
devicesListbox.grid(column=0, row=1, rowspan=10)
devicesListbox.bind("<Double-1>", lambda e: connectToDevice(devicesListbox.curselection()))

connectLoader = ttk.Progressbar(connectionTab, orient= "horizontal", length = 200, mode = "indeterminate")
connectLoader.start(4)

rateLabel = Label(sendRecieveTab, text=rate)
rateLabel.grid(column=0, row=0, pady=[5,0], columnspan=2)

dataLog = Text(sendRecieveTab, state='disabled', width=70, height=24, wrap='none')
dataLog.grid(column=0, row=1, pady=[5,0], columnspan=2)

sendButton = ttk.Button(sendRecieveTab, text='Send File', command=selectFile, state = "disabled")
sendButton.grid(column=1, row=2, sticky="W", pady=[5,0])

disconnectButton = ttk.Button(connectionTab, text='Disconnect', command=disconnectFromDevice, state = "disabled")
disconnectButton.grid(column=1, row=4)

writeToDataLog("Messages recieved from a connected device will appear here.\n")
tk.after(1000, updateLog)
tk.mainloop()