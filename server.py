import socket, time
from threading import Thread
import os
import getpass
from rich.console import Console
from pathlib import Path
import time
global op
nameipdic = {}
ipnamedic = {}
global hosttmp
global porttmp
fileidx = 1
oppassword = 123456
version = "2.2.2" # 版本号

def resetdata(data): # 重新设置信息
    try:
        if len(data) > 1024:
            return "发送了长度超过系统限制的信息"
        tmp = ""
        cnt = 0
        try:
            for i in data:
                if i == "\n":
                    cnt += 1
                if i == "\r":
                    tmp = tmp + "\\r"
                else:
                    tmp = tmp + i
            if cnt >= 300:
                return "发送了行数超过系统限制的信息"
        except:
            return data
        return tmp
    except:
        return ""

class Manager:
    def __init__(self,socket,addr,username):
        self.ip = addr[0]
        self.port = addr[1]
        self.username = username
        self.socket=socket
        self.lastsendtime = 0
        self.last_kick = 10
        self.version = ""
    def sendMsg(self,msg,username):
        try:
            self.socket.send(("%s %s: %s" %(self.getTime(), username, msg)).encode("utf-8"))
            return True
        except:
            return False
    def set_LastSendTime(self):
        self.lastsendtime = time.time()
    def recv(self,mtu=102400):
        try:
            data = self.socket.recv(mtu).decode("utf-8")
            if data == "quit" or not data:
                return False
            return data
        except:
            return False
        
    def close(self):
        try:
            self.socket.close()
            return True
        except:
            return False
    def kick(self):
        try:
            self.socket.send("!!!kick".encode("utf-8"))
            time.sleep(1)
            self.close()
            return True
        except:
            return False
    def banned(self):
        try:
            self.socket.send("!!!ban".encode("utf-8"))
            time.sleep(1)
            self.close()
            return True
        except:
            return False
    def kick2(self):
        try:
            time.sleep(1)
            self.close()
            return True
        except:
            return False
    def getId(self):
        return "%s-%s" % (self.ip,self.port)
    def getTime(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S"))

    def new_client(c):
        try:
            print("%s[%s] 尝试连接" %(c.ip,c.port))
            data = c.recv()
            if not data:
                return
            bannedlist = open("banlist.txt", "r")
            banlist = bannedlist.readlines()
            bannedlist.close()
            for lines in banlist:
                if c.ip in lines:
                    c.banned()
                    time.sleep(1)
                    return
            c.username = data.split(" ")[0]
            c.version = data.split(" ")[1]
            sleeptime = 2
            if c.username == op:
                time.sleep(2)
                c.socket.send("!!!password".encode("utf-8"))
                password = c.recv()
                if password != oppassword:
                    c.socket.send("密码错误！".encode("utf-8"))
                    c.socket.close()
                    return
                sleeptime = 0.5
            try:
                if c.version.split(".")[0] != version.split(".")[0] or c.version.split(".")[1] != version.split(".")[1]:
                    s.print("用户 " + c.username + " " + c.ip + "[" + str(c.port) + "] 因为版本号相差过大而无法连接。", style="bold yellow")
                    c.socket.send("!!!warning 版本号相差过大，无法连接。".encode("utf-8"))
                    time.sleep(10)
                    c.kick2()
                    try:
                        del nameipdic[c.username]
                        del ipnamedic[("%s-%s" % (c.ip, c.port))]
                        clients.pop(c.getId())
                    except:
                        pass
                    return
            except:
                s.print("用户 " + c.username + " " + c.ip + "[" + str(c.port) + "] 因为版本号相差过大而无法连接。", style="bold yellow")
                c.socket.send("!!!warning 版本号相差过大，无法连接。".encode("utf-8"))
                time.sleep(10)
                c.kick2()
                try:
                    del nameipdic[c.username]
                    del ipnamedic[("%s-%s" % (c.ip, c.port))]
                    clients.pop(c.getId())
                except:
                    pass
                return
            s.print("用户 %s %s[%s] 已连接" %(c.username,c.ip,c.port), style = "bold yellow")
            nameipdic[c.username] = "%s-%s" % (c.ip, c.port)
            ipnamedic[("%s-%s" % (c.ip, c.port))] = c.username
            usercnt = len(nameipdic)
            iports[c.username] = f'{c.ip}-{c.port}'
            time.sleep(sleeptime)
            c.socket.send(("欢迎来到 OIChat !\n当前在线用户 " + str(usercnt) + " 人。\n输入 '/help' 获取帮助 。\n").encode("utf-8"))
            time.sleep(0.5)
            Manager.broadcast("用户 " + c.username + " 加入了聊天室，当前在线 " + str(usercnt) + " 人。", "系统消息")
            if c.version != version: # 版本号校验
                data = "!!!warning 警告：您的版本为 " + c.version + ", 而服务端的版本为 " + version + ", 可能出现问题。"
                c.socket.send(data.encode("utf-8"))
            while True:
                data = c.recv()
                data = resetdata(data)
                if not data:
                    break
                elif data[0:3] == "!!!":
                    global fileidx
                    tmp = data[3:].split(" ")
                    if tmp[0] == "file":
                        filename = data[7:]
                        tmpfilename = ""
                        for char in filename:
                            if char == " ":
                                continue
                            tmpfilename += char
                        filename = tmpfilename
                        if not os.path.exists("file"):
                            os.makedirs("file")
                        oldfilename = filename
                        filename = str(fileidx) + " " + str(time.strftime("%Y.%m.%d.%H.%M.%S")) + " " + c.username + " " + filename
                        fileidx = fileidx + 1
                        fileaddr = os.path.join("file", filename)
                        file = open(fileaddr, "wb")
                        filedata = b""
                        while True:
                            filedata = c.socket.recv(100)
                            if filedata == b"!!!endfile":
                                break
                            file.write(filedata)
                        file.close()
                        s.print("用户 " + c.username + " 发送了文件：" + oldfilename)
                        c.socket.send("发送文件成功！".encode("utf-8"))
                        time.sleep(0.1)
                        Manager.broadcast("用户 " + c.username + " 发送了文件：" + oldfilename + "，输入 '/files download " + str(fileidx - 1) + "' 下载。", "系统消息")
                        continue
                elif data[0:1] == "/":
                    tmp = data[1:].split(" ")
                    if tmp[0] == "help":
                        c.sendMsg("\n指令列表：\n\n1. /files\n\n2. /kick\n\n3. /ban\n\n4. /banip\n\n5. /important", "系统消息")
                        continue
                    elif tmp[0] == "files":
                        cnt = len(tmp)
                        if cnt == 1:
                            c.sendMsg("缺少参数，输入 '/files ?' 获取帮助", "系统消息")
                        elif cnt == 2:
                            if tmp[1] == "?":
                                c.sendMsg("\n1. query (/files query) ，查询所有文件 。\n\n2. download [id] (/files downloads [id]) ，使用文件编号替代 [id] ，下载编号为 [id] 的文件 。", "系统消息")
                            if tmp[1] == "query":
                                path = Path("./file")
                                try:
                                    files = [file.name for file in path.rglob("*.*")]
                                except:
                                    c.sendMsg("暂无文件。", "系统消息")
                                    continue
                                message = "\n编号 | 文件名 | 时间 | 用户\n"
                                le = len(files)
                                if le == 0:
                                    c.sendMsg("暂无文件。", "系统消息")
                                    continue
                                for file in files:
                                    fi = file.split(" ")
                                    message = " " + message + fi[0] + " | "
                                    message = message + fi[3] + " | "
                                    message = message + fi[1].split('.')[1] + "." + fi[1].split('.')[2] +  " " + fi[1].split('.')[3] + ":" + fi[1].split('.')[4] + ":" + fi[1].split('.')[5] + " | "
                                    message = message + fi[2] + "\n"
                                c.sendMsg(message, "系统消息")
                            if tmp[1] == "download":
                                c.sendMsg("缺少参数。", "系统消息")
                        elif cnt == 3:
                            if tmp[1] == "download":
                                path = Path("./file")
                                try:
                                    files = [file.name for file in path.rglob("*.*")]
                                except:
                                    c.sendMsg("暂无文件。", "系统消息")
                                flag = 1
                                for file in files:
                                    if file.split(" ")[0] == tmp[2]:
                                        c.socket.send("正在下载文件..在此期间请勿发送任何消息，否则可能造成文件损坏！！！".encode("utf-8"))
                                        c.socket.send(("!!!file " + file.split(" ")[3]).encode("utf-8"))
                                        time.sleep(3)
                                        filename = os.path.basename(file)
                                        fileaddr = os.path.join("file", filename)
                                        sendfile = open(fileaddr, "rb")
                                        c.socket.sendall(sendfile.read())
                                        sendfile.close()
                                        time.sleep(5)
                                        c.socket.send(b"!!!endfile")
                                        s.print("用户 " + c.username + " 下载文件：" + file.split(" ")[3])
                                        time.sleep(1)
                                        c.socket.send("下载文件成功！".encode("utf-8"))
                                        flag = 0
                                        break
                                if flag == 1:
                                    c.sendMsg("没有编号为 " + str(tmp[2]) + " 的文件。", "系统消息")
                        else:
                            c.sendMsg("参数过多", "系统消息")
                        continue
                    elif (tmp[0] == "important"):
                        cnt = len(tmp)
                        if (cnt == 1):
                            c.sendMsg("缺少参数，输入 /important ? 获取帮助。", "系统消息")
                        elif (cnt == 2):
                            if (tmp[1] == "?"):
                                c.sendMsg("用法：/important <User> <Msg>", "系统消息")
                            else:
                                c.sendMsg("输入 /important ? 获取帮助。", "系统消息")
                        elif (cnt >= 3):
                            User_Name = tmp[1]
                            message_len = 12 + len(User_Name)
                            Send_Msg = data[message_len:]
                            try:
                                User_Id = nameipdic[User_Name]
                            except:
                                c.sendMsg("没有 " + User_Name + " 用户", "系统消息")
                            clients[iports[User_Name]].socket.send(("!!!important " + c.username + " " + Send_Msg).encode("utf-8"))
                            c.sendMsg("你向 " + User_Name + " 发送了重要消息：" + Send_Msg, "系统消息")
                    elif clients[c.getId()].username != op:
                        c.sendMsg("你没有权限使用指令", "系统消息")
                        continue
                    elif (tmp[0] == "kick"):
                        cnt = len(tmp)
                        if cnt == 1:
                            c.sendMsg("缺少参数，输入 '/kick ?' 获取帮助", "系统消息")
                        elif cnt == 2:
                            if tmp[1] == "?":
                                c.sendMsg("\n/kick username\n把 username 踢出服务器", "系统消息")
                            else:
                                user = ""
                                try:
                                    user = nameipdic[tmp[1]]
                                except:
                                    user = "-"
                                if user == "-":
                                    c.sendMsg("没有找到 " + tmp[1] + " 用户。", "系统消息")
                                else:
                                    clients[user].kick()
                        else:
                            c.sendMsg("参数过多", "系统消息")
                    elif (tmp[0] == "ban"):
                        cnt = len(tmp)
                        if cnt == 1:
                            c.sendMsg("缺少参数，输入 '/ban ?' 获取帮助", "系统消息")
                        elif cnt == 2:
                            if tmp[1] == "?":
                                c.sendMsg("\n/ban <User>\n把 <User> 所在的 IP 加入黑名单并且把 <User> 踢出服务器", "系统消息")
                            else:
                                user = ""
                                try:
                                    user = nameipdic[tmp[1]]
                                except:
                                    user = "-"
                                if user == "-":
                                    c.sendMsg("没有找到 " + tmp[1] + " 用户。", "系统消息")
                                else:
                                    banlist = open("banlist.txt", "a")
                                    banlist.write(user + "\n")
                                    banlist.close()
                                    clients[user].banned()
                        else:
                            c.sendMsg("参数过多", "系统消息")
                        continue
                    elif (tmp[0] == "banip"):
                        cnt = len(tmp)
                        if cnt == 1:
                            c.sendMsg("缺少参数，输入 '/banip ?' 获取帮助", "系统消息")
                        elif cnt == 2:
                            if tmp[1] == "?":
                                c.sendMsg("\n/banip ip\n把 ip 加入黑名单。", "系统消息")
                            else:
                                fi = open("banlist.txt", "a")
                                fi.write("\n" + tmp[1])
                                fi.close()
                        else:
                            c.sendMsg("参数过多", "系统消息")
                    continue
                elif data[0:1] == "@":
                    try:
                        c.sendMsg(data,c.username)
                        clients[iports[data[1:].split(' ')[0]]].sendMsg(data,c.username)
                    except:
                        c.sendMsg("没有找到 " + data[1:].split(' ')[0] + " 用户。", "系统消息")
                else:
                    if c.last_kick <= 0:
                        c.sendMsg("由于你的发送速度太快，你将被系统踢出了服务器。", "系统消息")
                        time.sleep(1)
                        c.kick()
                    if (time.time() - c.lastsendtime <= 2):
                        c.sendMsg("请稍后发送。", "系统消息")
                        c.last_kick -= 1
                        continue
                    c.set_LastSendTime()
                    if c.username == op:
                        c.lastsendtime = 0
                    s.print("用户 %s %s[%s] 发送了: " % (c.username, c.ip, c.port), end = "")
                    print(data)
                    Manager.broadcast(data, c.username)

        except socket.errno as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            s.print("%s[%s] 断开连接" % (c.ip, c.port), style = "bold yellow")
            try:
                del nameipdic[c.username]
                del ipnamedic[("%s-%s" % (c.ip, c.port))]
                clients.pop(c.getId())
            except:
                pass
            usercnt = len(nameipdic)
            Manager.broadcast("用户 " + c.username + " 离开了聊天室，当前在线 " + str(usercnt) + " 人。", "系统消息")
            c.close()

    def broadcast(msg,username):
        for c in clients.values():
            c.sendMsg(msg,username)

def main(host, port, flag):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((host, port))
    server.listen(10)
    s.print("欢迎使用 OIChat " + version + " ！", justify="center", end="\n\n")
    s.print("服务器已成功在 %s 端口开启！" % (port), style = "bold green")
    s.print("管理员账户：[ " + op + " ]", style = "bold blue")
    s.print("管理员密码：请查看 `config.txt` 内的密码。", style = "bold blue")
    if flag == 1:
        s.print("是否打开 GitHub 仓库（Y / N）：", end = "")
        tmpp = input()
        if tmpp == "y" or tmpp == "Y":
            os.system("start https://github.com/yuhaodi22222/OIChat")
    else:
        s.print("GitHub 仓库地址：https://github.com/yuhaodi22222/OIChat")
    while True:
        conn, addr = server.accept()
        c = Manager(conn,addr,"")
        clients[c.getId()] = c
        t = Thread(target=Manager.new_client, args=(c,))
        t.start()

if __name__ == "__main__":
    s = Console()
    banlist = open("banlist.txt", "a")
    banlist.close()
    clients = {}
    iports = {}
    fileidx = 0
    flag = 0
    try:
        path = Path("./file")
        files = [file.name for file in path.rglob("*.*")]
        for file in files:
            fileidx = max(fileidx, int(file.split(" ")[0]))
        fileidx = fileidx + 1
    except:
        fileidx = 1
    try:
        config = open("config.txt", "r")
        lines = config.readlines()
        porttmp = int(lines[0])
        optmp = lines[1]
        op = ""
        for i in optmp:
            if i == "\n" or i == "\r":
                break
            op = op + i
        oppasswordtmp = lines[2]
        oppa = ""
        for i in oppasswordtmp:
            if i == "\n" or i == "\r":
                break
            oppa = oppa + i
        oppassword = oppa
        hosttmp = "0.0.0.0"
    except:
        hosttmp = "0.0.0.0"
        porttmp = int(input("请输入开服端口："))
        op = input("设置管理员账号名称：")
        oppassword = ""
        oppassword1 = "1"
        oppassword = getpass.getpass("设置管理员账号密码（输入内容不会显示）：")
        oppassword1 = getpass.getpass("再次输入密码确认：")
        while oppassword != oppassword1:
            print("两次密码不匹配，请重新输入！")
            oppassword = getpass.getpass("设置管理员账号密码：")
            oppassword1 = getpass.getpass("再次输入密码确认：")
        config = open("config.txt", "w")
        config.write(str(porttmp) + "\n")
        config.write(op + "\n")
        config.write(oppassword)
        config.close()
        flag = 1
    finally:
        os.system("cls")
        main(hosttmp, porttmp, flag)
