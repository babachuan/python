#!/usr/bin/evn python
#-*-coding:utf-8-*-
import queue
import threading
import tkinter.messagebox
from tkinter import *
import hashlib
import time
from tkinter import filedialog
import os
import shutil
from tkinter import *
from tkinter import ttk



# box中rawdata完成后的目录：/rawdata/180419/HKVL7BGX5/output/HKVL7BGX5_L004/180419_NS500823_HKVL7BGX5_L004_HUMCNGQZHPEI-1130-v109
# /mnt/NL200_1/archive/2017/12/13/HYFMFBGX3_L003/171213_TPNB500129_HYFMFBGX3_L003_HUMCNFWYKPEI-281-v109
class make_data(object):
    def __init__(self, sourthpath, tarpath, rawdatapath):  #
        self.sourthpath = sourthpath + '\\'  # 数据原目录
        self.tarpath = tarpath + '\\'  # 数据需要拷贝整理的目的目录
        self.path = os.getcwd() + '\\'  # 获取当前脚本存放目录
        self.rawdatapath = rawdatapath

    # 获取数据的全路径，并存储到文件中：/mnt/ONCOBOX/geneplus/test_data/180013773/180702_NS500823_HKVWHBGX5_L004_HUMCNHFYLPEI-1535-v109
    # /mnt/ONCOBOX/geneplus/test_data/这部分为sourcepath，后半部分为真正的数据
    def get_fullnamelist(self):
        if os.path.exists(self.path + "namelist.txt"):
            os.remove(self.path + "namelist.txt")
        with open(self.path + "namelist.txt", "a") as file:
            for item in os.listdir(self.sourthpath):
                for pathname in os.listdir(self.sourthpath + item):
                    file.write(self.sourthpath + item + '\\' + pathname + "\n")
                    # 将遍历到的文件写入namelist.txt,
                    # 注意遍历的原始数据目录格式应该是：样本编号/lane对应的文件夹
                    # 格式：目录/170016744/171218_NB501132_HYFKNBGX3_L001_HUMCNFYFVPEI-237-v109
                    # print(self.sourthpath + item + '\\' + pathname)

    # 对于namelist的路径进行拆分，生成上机所需字段
    def saveSqueceData(self):
        with open(self.path + "namelist.txt", "r") as ssf:
            with open(self.path + "squence_list.txt", "w",encoding='utf-8') as slf:
                slf.write("Run号" + "\t" + "上机时间" + "\t" + "测序平台" + "\t" + "机器号" + "\t" + "样本编号" + "\t" + "样本文库号" + "\t" + "index号" + "\t" + "lane号" + "\t" + "芯片号" + "\t" + "样本类型" + "\n")
                for line in ssf.readlines():
                    datetime, machinenum, runnum, lane, libnum1 = (line.split('\\')[-1]).split('_')
                    libnum2 = libnum1.replace('\n', '')
                    yangbenbianhao = line.split('\\')[-2].strip('\n')
                    xinpianhao = libnum2.split('-')[-1]
                    time_str = "20" + datetime
                    shangjishijian = time_str[:4] + '\\' + time_str[4:6] + '\\' + time_str[6:8]
                    indexnum = libnum2.split('-')[1]
                    slf.write(runnum + "\t" + shangjishijian + "\t" + "Illumina" + "\t" + machinenum + "\t" + yangbenbianhao + "\t" + libnum2 + "\t" + indexnum + "\t" + lane + "\t" + xinpianhao + "\t" + "样本类型" + "\n")

    # 公用方法，判断并生成路径
    def check_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    # 该方法用于生成数据拆分后的log成功标识文件
    def makelogpath(self, datetiem, runnum):
        logpath = self.tarpath + datetiem + '\\' + runnum + '\\' + "log"
        self.check_path(logpath)
        file = open(logpath + '\\' + 'SUCCESS', 'w')
        file.close()

    # 生成数据拆分后的QC文件
    def makeqcfile(self, datetime, runnum):
        qcfilgpath = self.tarpath + datetime + '\\' + runnum + '\\' + "output/"
        self.check_path(qcfilgpath)

        laneqc = qcfilgpath + runnum + '_lanes_qc.csv'
        laneqc_s = "Run20180301_lanes_qc.csv"
        shutil.copy(laneqc_s, laneqc)

        libqc = qcfilgpath + runnum + '_libs_qc.csv'
        libqc_s = "Run20180301_libs_qc.csv"
        shutil.copy(libqc_s, libqc)

        reportqc = qcfilgpath + runnum + '_sequencing_report.csv'
        reportqc_s = "Run20180301_sequencing_report.csv"
        shutil.copy(reportqc_s, reportqc)
        # laneqc=open(qcfilgpath+runnum+'_lanes_qc.csv','w')
        # libqc=open(qcfilgpath+runnum+'_libs_qc.csv','w')
        # reportqc=open(qcfilgpath+runnum+'_sequencing_report.csv','w')
        waringqc = open(qcfilgpath + runnum + '_warning_lanes.txt', 'w')
        waringqc.close()
        # reportqc.close()
        # libqc.close()
        # laneqc.close()

    # 该方法用于拷贝数据到拆分结果目录
    def copydata(self):
        with open(self.path + "namelist.txt") as file:  # 读取的文件为get_fullnamelist生成的namelist.txt
            for item in file:
                datapath = item.strip('\n')
                datetime, machinenum, runnum, lane, libnum = (datapath.split('\\')[-1]).split('_')
                tarpath = self.tarpath + datetime + '\\' + runnum + '\\' + "output" + '\\' + runnum + "_" + lane + '\\' + (
                datapath.split('\\')[-1]) + '\\'
                self.check_path(tarpath)
                self.makelogpath(datetime, runnum)
                self.makeqcfile(datetime, runnum)
                try:
                    for item in os.listdir(datapath):
                        shutil.copy(os.path.join(datapath,item),os.path.join(tarpath,item))
                    # os.system('copy ' + datapath + '\\'+'* ' + tarpath)
                    # print(datapath, 'copy over.................')
                except:
                    errorfile = open(self.tarpath + 'errorlist.txt', 'a')
                    errorfile.write(datapath + '\t' + tarpath + '\n')
                    errorfile.close()
                    # print('There is an error occur!!!!!!!!==========')

    # 在北京box上进行该目录生成,生成的目录是拆分前的目录
    def makrawdatapath(self):
        # basepath='/mnt/ONCOBOX/geneplus/rawdata/' 现在直接拷贝到rawdata目录
        with open(self.path + "namelist.txt") as file:
            for item in file:
                datapath = item.strip('\n')
                datetime, machinenum, runnum, lane, libnum = (datapath.split('\\')[-1]).split('_')
                rawdatapath = self.rawdatapath + '\\' + datetime + "_" + machinenum + "_" + "1234" + "_A" + runnum + '\\'
                self.check_path(rawdatapath)
                shutil.copy(self.path + 'RunInfo.xml',rawdatapath)
                # os.system('copy ' + self.path + 'RunInfo.xml ' + rawdatapath)
                file = open(rawdatapath + 'RTAComplete.txt', 'w')
                file.close()
                # print
                # rawdatapath

    # 获取录入数据的方法：180013773/180702_NS500823_HKVWHBGX5_L004_HUMCNHFYLPEI-1535-v109
    def get_dampleinfo(self):
        result = open(self.path + "sampleinfo.csv", "w")
        with open(self.path + "namelist.txt") as file:
            for line in file:
                datapath = line.strip('\n')
                samplenum = datapath.split('\\')[-2]
                datetime, machinenum, runnum, lane, libnum = (datapath.split('\\')[-1]).split('_')
                result.write(
                    samplenum + "\t" + libnum + "\t" + lane + "\t" + runnum + "\t" + machinenum + "\t" + datetime + "\n")
        result.close()

#
# if __name__ == '__main__':
#     sourcepath = "/mnt/ONCOBOX/geneplus/20180905/test_data"  # 原始数据目录，下一层目录是样本编号
#     tarpath = "/mnt/ONCOBOX/geneplus/20180905/workspace/rowdata"  # 目标数据目录，数据拆分后要存放到哪里，fq文件
#     rawdatapath = "/mnt/ONCOBOX/geneplus/20180905/rawdata"  # 数据拆分前的目录，模拟原始数据用
#     data = make_data(sourcepath, tarpath, rawdatapath)
#     data.get_fullnamelist()
#     data.copydata()
#     data.makrawdatapath()
#     data.saveSqueceData()
#     data.get_dampleinfo()
#
#     print
#     'over!!!'

# 进度条类
class GressBar():

	def start(self):
		top = Toplevel()
		self.master = top
		top.overrideredirect(True)
		top.title("进度条")
		Label(top, text="任务正在运行中,请稍等……", fg="green").pack(pady=2)
		prog = ttk.Progressbar(top, mode='indeterminate', length=200)
		prog.pack(pady=10, padx=35)
		prog.start()

		top.resizable(False, False)
		top.update()
		curWidth = top.winfo_width()
		curHeight = top.winfo_height()
		scnWidth, scnHeight = top.maxsize()
		tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
		top.geometry(tmpcnf)
		top.mainloop()

	def quit(self):
		if self.master:
			self.master.destroy()


LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.notify_queue = queue.Queue()
        self.gress_bar=GressBar()

    # 数据目录调用目录
    def get_init_data_dialog_text(self):
        self.init_data_Text.delete(1.0, END)
        init_data_dilog = filedialog.askdirectory()
        self.init_data_Text.insert(1.0,init_data_dilog)
    # 拆分前目录调用目录
    def get_before_rawdata_data_dialog_text(self):
        self.before_rawdata_data_Text.delete(1.0, END)
        before_rawdata_data_dilog = filedialog.askdirectory()
        self.before_rawdata_data_Text.insert(1.0,before_rawdata_data_dilog)
    # 拆分后目录调用目录
    def get_after_rawdata_data_dialog_text(self):
        self.after_rawdata_data_Text.delete(1.0, END)
        after_rawdata_data_dilog = filedialog.askdirectory()
        self.after_rawdata_data_Text.insert(1.0,after_rawdata_data_dilog)

    # #执行拷贝的整体命令
    # def execute(self):
    #     self.gress_bar.start()

    # 执行命令,在异步线程里执行
    def execute_copy(self):
        sourcepath = self.init_data_Text.get('0.0',END).strip().replace('/','\\').strip('\n') # 原始数据目录，下一层目录是样本编号
        tarpath = self.after_rawdata_data_Text.get('0.0',END).strip().replace('/','\\').strip('\n') #"/mnt/ONCOBOX/geneplus/20180905/workspace/rowdata"  # 目标数据目录，数据拆分后要存放到哪里，fq文件
        rawdatapath = self.before_rawdata_data_Text.get('0.0',END).strip().replace('/','\\').strip('\n')#"/mnt/ONCOBOX/geneplus/20180905/rawdata"  # 数据拆分前的目录，模拟原始数据用
        data = make_data(sourcepath, tarpath, rawdatapath)
        data.get_fullnamelist()
        data.copydata()
        # time.sleep(10)
        data.makrawdatapath()
        data.saveSqueceData()
        data.get_dampleinfo()
        tkinter.messagebox.showinfo('处理结果','已经成功处理完成')
        self.gress_bar.quit()

    #处理进度条
    # def process_msg(self):
    #     self.init_window_name.after(400, self.process_msg)  #随主窗口一起启动
    #     while not self.notify_queue.empty():
    #         try:
    #             msg = self.notify_queue.get()
    #             if msg[0] == 1:
    #                 self.gress_bar.quit()
    #
    #         except queue.Empty:
    #             pass


    #进度条相关
    def execute(self):
        # # 定义一个scan函数，放入线程中去执行耗时扫描
        def scan(_queue):
            self.execute_copy()
            _queue.put((1,))

        # th = threading.Thread(target=self.execute_copy(), args=(self.notify_queue,))
        th = threading.Thread(target=scan,args=(self.notify_queue,))
        th.setDaemon(True)
        th.start()
        self.gress_bar.start()




    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("BOX数据处理工具    吉因加科技")           #窗口名
        #self.init_window_name.geometry('320x160+50+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('560x225+350+250')
        self.init_window_name["bg"] = "#005b6f"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #数据目录标签
        self.init_data_label = Label(self.init_window_name, text="原数据目录",width=10,height=1,background="#005b6f",foreground="white")
        self.init_data_label.grid(row=1, column=2,pady=10,padx=40)
        #数据目录文本框
        self.init_data_Text =Text(self.init_window_name, width=40, height=1) #Entry(self.init_window_name,width=40, height=1) #Text(self.init_window_name, width=40, height=1)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=4, rowspan=2, columnspan=2)
        #数据目录打开按钮
        self.init_data_open_button = Button(self.init_window_name, text="打开", bg="lightblue", width=6,height=1,command=self.get_init_data_dialog_text)  # 调用内部方法  加()为直接调用
        self.init_data_open_button.grid(row=1, column=15,padx=10)

        #拆分前目录标签
        self.before_rawdata_data_label = Label(self.init_window_name, text="拆分前目录",width=10,height=1,background="#005b6f",foreground="white")
        self.before_rawdata_data_label.grid(row=3, column=2,pady=10,padx=40)
        #拆分前目录文本框
        self.before_rawdata_data_Text = Text(self.init_window_name, width=40,height=1)  # Entry(self.init_window_name,width=40, height=1) #Text(self.init_window_name, width=40, height=1)  #原始数据录入框
        self.before_rawdata_data_Text.grid(row=3, column=4, rowspan=2, columnspan=2)
        #拆分前目录打开按钮
        self.before_rawdata_data_open_button = Button(self.init_window_name, text="打开", bg="lightblue", width=6,height=1,command=self.get_before_rawdata_data_dialog_text)  # 调用内部方法  加()为直接调用
        self.before_rawdata_data_open_button.grid(row=3, column=15,padx=10)



        #拆分后目录标签
        self.after_rawdata_data_label = Label(self.init_window_name, text="拆分后目录",width=10,height=1,background="#005b6f",foreground="white")
        self.after_rawdata_data_label.grid(row=5, column=2,pady=10,padx=40)
        # 拆分后目录文本框
        self.after_rawdata_data_Text = Text(self.init_window_name, width=40,height=1)  # Entry(self.init_window_name,width=40, height=1) #Text(self.init_window_name, width=40, height=1)  #原始数据录入框
        self.after_rawdata_data_Text.grid(row=5, column=4, rowspan=2, columnspan=2)
        # 拆分后目录打开按钮
        self.after_rawdata_data_open_button = Button(self.init_window_name, text="打开", bg="lightblue", width=6,height=1,command=self.get_after_rawdata_data_dialog_text)  # 调用内部方法  加()为直接调用
        self.after_rawdata_data_open_button.grid(row=5, column=15,padx=10)


        #执行按钮
        self.execute_button = Button(self.init_window_name, text="执行", bg="lightblue", width=6,height=1,command=self.execute)  # 调用内部方法  加()为直接调用
        self.execute_button.grid(row=7, column=2,padx=10)
        # self.init_data_Text = Text(self.init_window_name, width=30, height=10)  #原始数据录入框
        # self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        # self.result_data_Text = Text(self.init_window_name, width=40, height=22)  #处理结果展示
        # self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        # self.log_data_Text = Text(self.init_window_name, width=30, height=10)  # 日志框
        # self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # #按钮
        # self.str_trans_to_md5_button = Button(self.init_window_name, text="MD5加密", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        # self.str_trans_to_md5_button.grid(row=1, column=11)

    #
    # #功能函数
    # def str_trans_to_md5(self):
    #     src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
    #     #print("src =",src)
    #     if src:
    #         try:
    #             myMd5 = hashlib.md5()
    #             myMd5.update(src)
    #             myMd5_Digest = myMd5.hexdigest()
    #             #print(myMd5_Digest)
    #             #输出到界面
    #             self.result_data_Text.delete(1.0,END)
    #             self.result_data_Text.insert(1.0,myMd5_Digest)
    #             self.write_log_to_Text("INFO:str_trans_to_md5 success")
    #         except:
    #             self.result_data_Text.delete(1.0,END)
    #             self.result_data_Text.insert(1.0,"字符串转MD5失败")
    #     else:
    #         self.write_log_to_Text("ERROR:str_trans_to_md5 failed")
    #
    #
    # #获取当前时间
    # def get_current_time(self):
    #     current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #     return current_time
    #
    #
    # #日志动态打印
    # def write_log_to_Text(self,logmsg):
    #     global LOG_LINE_NUM
    #     current_time = self.get_current_time()
    #     logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
    #     if LOG_LINE_NUM <= 7:
    #         self.log_data_Text.insert(END, logmsg_in)
    #         LOG_LINE_NUM = LOG_LINE_NUM + 1
    #     else:
    #         self.log_data_Text.delete(1.0,2.0)
    #         self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
