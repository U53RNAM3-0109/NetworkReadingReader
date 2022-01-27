from matplotlib import pyplot as plt
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import csv

def getcsv(file):
    #Turns the csv into a very big dictionary
    try:
        with open(file,'r') as csv_file:
            reader = csv.reader(csv_file)
            head=True
            data = []
            for row in reader:
                if head:
                    headers = tuple(row)
                    head = False
                packet = {}
                for i in range(len(headers)):
                    packet[headers[i]] = row[i]
                data.append(packet)
            data = tuple(data)
        return data
    except:
        mb.showerror("File error",f"Cannot locate file \"{file}\"")
        return None

def makedict(data):
    if data:
        #Counts each type and places the results into a dictionary
        protocol_freq = {}
        protocols = {}
        for packet in data:
            if packet['Protocol'] not in protocols.keys():
                protocols[packet['Protocol']] = 1
            else:
                protocols[packet['Protocol']] += 1
        return protocols
    else:
        return None

def sortaslist(protocols):
    if protocols:
        #sorts the dictionary into a list
        protlist = []
        for item in protocols.items():
            protlist.append(item)

        notDone=True
        while notDone:
            notDone=False
            for i in range(len(protlist)):
                try:
                    if protlist[i][1] > protlist[i+1][1]:
                        temp = protlist[i]
                        protlist[i] = protlist[i+1]
                        protlist[i+1] = temp
                        notDone=True
                except IndexError:
                    pass
        
        return protlist
    else:
        return None
    
def getnum(inp,numofprots,showErrors):
    # Returns the contents of the text box,
    # raising an error if it isn't an integer
    # (returned as a negative number, to allow
    # for list slicing later)
    while True:
        inp 
        try:
            num = 0-(int(inp))
            if num<-numofprots:
                if showErrors:
                    mb.showinfo("Graph Info",f"Only {numofprots} protocols to show.")
            return num
        except:
            raise ValueError('Not the right thingy')
            

def remakedict(protlist,numentry,showErrors):
    if protlist:
        #rebuilds the dict from the list
        #shows a message if the text input isn't a number
        protocols = {}
        protlist=protlist[1::]
        try:
            protlist = protlist[getnum(numentry,len(protlist),showErrors)::]
        except:
            if not showErrors:
                mb.showerror("Graph Error","Please enter a number.")
            return None
        for item in protlist:
            protocols[item[0]] = item[1]
        return protocols
    else:
        return None

def showgraph():
    plt.clf() #clears current graph

    #attempts to show the graph
    file = fileentry.get()
    protocols=remakedict(sortaslist(makedict(getcsv(file))),numentry.get(),True)
    if protocols:
        plt.xlabel('Protocol')
        plt.ylabel('Frequency')
        plt.title('Protocol Frequency')
        vals = tuple(list(protocols.values()))
        keys = tuple(list(protocols.keys()))
        plt.bar(keys,vals)
        plt.show()

def showstats():
    plt.clf() #clears current graph

    #create new window
    window2 = tk.Toplevel(window)
    window2.title("Statistics")

    #create empty treeview widget
    statdisplay = ttk.Treeview(window2,columns=('Frequency')).pack()

    #get csv data for display
    file = fileentry.get()
    data = remakedict(sortaslist(makedict(getcsv(file))),80,False)
    if not data:
        window2.destroy()
    print(data)

window = tk.Tk()
window.title("Menu")

#entry boxes
numentry = tk.Entry(window,width=18)
numentry.insert(0,'Protocols to plot')
numentry.pack()
fileentry = tk.Entry(window,width=18)
fileentry.insert(0,'Filename.csv')
fileentry.pack()

#buttons
graphbutton = tk.Button(window,text='Show Graph',command=showgraph).pack()
statbutton = tk.Button(window,text='Show Statistics',command=showstats).pack()


def on_closing():
    if mb.askokcancel("Quit", "Quit?"):
        window.destroy()
        plt.close()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()