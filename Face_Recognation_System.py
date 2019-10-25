#Dlib是一个包含机器学习算法的python开源工具包。
import dlib
import Db_Util as db
import cv2
import csv
from skimage import io
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import *
# from tkinter import Entry
import tkinter.messagebox
from PIL import Image, ImageTk

conn = db.DBUtil(username='root',password='123456',databasename='face_info')

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

# Dlib 人脸识别模型
facerec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')
# 处理存放所有人脸特征的 csv
# # 用来存放所有录入人脸特征的数组
# # 读取已知人脸数据
root = tk.Tk()
def  face_index():

    # 设置窗口主题
    root.title('欢迎进入人脸识别系统')
    root.geometry('500x300')
    #透明主题
    # root.attributes('-alpha', 0.4)
    # 创建画布
    canvas = tk.Canvas(root,
                       width=500,  # 指定Canvas组件的宽度
                       height=300,  # 指定Canvas组件的高度
                       bg='white')  # 指定Canvas组件的背景色
    # im = Tkinter.PhotoImage(file='img.gif')     # 使用PhotoImage打开图片
    image = Image.open("images/face.jpg")
    im = ImageTk.PhotoImage(image)

    canvas.create_image(300, 100, image=im)  # 使用create_image将图片添加到Canvas组件中
    # 添加按钮
    # img=tk.PhotoImage(file="images/pig.png")
    bt1 = tk.Button(root, text='1.采集数据',bg='white',font=('Arial', 12),relief='ridge', width=10, height=1,command=face_register)
    bt2 = tk.Button(root, text='2.人脸识别',bg='white', font=('Arial', 12),relief='ridge', width=10, height=1,command=face_detect)
    bt3 = tk.Button(root, text='3.退出系统',bg='white',font=('Arial', 12),relief='ridge', width=10, height=1,command=exit)

    canvas.create_window(250, 50, width=200, height=50, window=bt1)
    canvas.create_window(250, 150, width=200, height=50, window=bt2)
    canvas.create_window(250, 250, width=200, height=50, window=bt3)
    canvas.pack()  # 将Canvas添加到主窗口
    root.mainloop()
def face_register():
    # root.destroy()
    root1=Tk()
    # 设置窗口主题
    root1.title('欢迎进入人脸识别系统')
    root1.geometry('500x300')  # 这里的乘是小x
    la1 = tk.Label(root1, text='Id：',  font=('Arial', 12), width=10, height=1).place(x=10,y=20)
    la2 = tk.Label(root1, text='用户名：', font=('Arial', 12), width=10, height=1).place(x=10, y=60)
    var1=tk.StringVar()
    var1.set('')
    var2=tk.StringVar()
    var2.set('')
    e1 = tk.Entry(root1,textvariable=var1)
    e1.place(x=120,y=20)
    e2 = tk.Entry(root1, textvariable=var2)
    e2.place(x=120,y=60)
    def judge():
        # tkinter.messagebox.showwarning(title="温馨提示",message='你好')

        user_id =e1.get()
        user_name = e2.get()
        flag = conn.findById('face_info', 'id', user_id)
        if len(flag) == 0:
            root1.destroy()
            tkinter.messagebox.showinfo(title="温馨提示", message='正在收集，请等待。。。')
            get_photo(user_name)
            tkinter.messagebox.showinfo(title="温馨提示", message='按q键保存并退出')
            try:
                fp = open("images/" + user_name + ".png", 'rb')
                img = fp.read()
                fp.close()
                conn.cursor.execute("insert into face_info values(%s,%s)", (user_name, user_id))
                conn.insetOne("INSERT INTO pic_face (pic_id,pic_name,pic_face) VALUES  (%s,%s,%s)",
                              (user_id, user_name, img))
                conn.db.commit()
            except Exception as e:
                print(e)
                tkinter.messagebox.showwarning(title="温馨提示", message='插入失败')
            try:
                write_csv("images/" + user_name + ".png", "data.csv")
            except Exception as ret:
                print(ret)
                tkinter.messagebox.showwarning(title="温馨提示", message='写入失败')
        else:
            tkinter.messagebox.showwarning(title="温馨提示", message='输入的id已存在，请重新输入')
    bt=tk.Button(root1, text='开始采集',bg='white',font=('Arial', 12),relief='ridge', width=10, height=1,command=judge).place(x=200,y=100)
    root1.mainloop()

def feature(img):
    #转换为灰度图片
    #将三维图片转换为二维进行处理
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #将图片采用人脸检测器检测人脸
    faces = detector(img_gray, 1)
    #检测到人脸，进行人脸预测，返回参数
    #将shape结果作为参数放到人脸识别模型中去识别人脸
    #人脸识别模型返回一个特征
    #并且return结果特征
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        descriptor = facerec.compute_face_descriptor(img_gray, shape)
    else:
        descriptor = 0
    return descriptor

# 将照片特征提取出来, 写入 CSV
def write_csv(face_path, csv_path):
    image = io.imread(face_path)
    #得到人脸特征
    feature_128d = feature(image)
    #打开IO流写入特征到csv文件当中，采用a参数作为追加保证数据持久化
    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(feature_128d)

def get_photo(face_name):
    # 打开摄像头，0代表内置摄像头，1代表外置摄像头
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        cv2.imshow('', frame)
        # 按q键拍照保存图片并退出
        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite("images/"+face_name+".png", frame)
            break
    # 释放摄像头资源
    camera.release()
    cv2.destroyAllWindows()

def distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.linalg.norm(feature_1 - feature_2)
    # 若欧式距离之差小于0.4则认为是目标人脸存在于识别库中
    if dist > 0.4:
        return False
    else:
        return True

def face_detect():
    csv_rd = pd.read_csv('data.csv', header=None)
    # 用来存放所有录入人脸特征的数组，默认初始值为空
    known_arr = []
    # 读取已知人脸数据
    for i in range(csv_rd.shape[0]):
        someone_arr = []
        for j in range(0, len(csv_rd.ix[i, :])):
            someone_arr.append(csv_rd.ix[i, :][j])
        known_arr.append(someone_arr)

    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()

        # 取灰度
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 人脸数 faces
        faces = detector(img_gray, 0)
        # 存储当前摄像头中捕获到的所有人脸的名字
        namelist = []

        # 按下 q 键退出
        if cv2.waitKey(1) == ord('q'):
            break
        else:
            # 检测到人脸
            if len(faces) != 0:
                feature_arr = []
                # 获取当前捕获到的图像的所有人脸的特征，存储到 feature_arr
                for i in range(len(faces)):
                    shape = predictor(img_gray, faces[i])
                    feature_arr.append(facerec.compute_face_descriptor(img_gray, shape))
                # 遍历捕获到的图像中所有的人脸
                for k in range(len(faces)):
                    # 先默认所有人不认识，是 unknown
                    namelist.append('unknown')
                    # 对于某张人脸，遍历所有存储的人脸特征
                    for i in range(len(known_arr)):
                        # 将某张人脸与存储的所有人脸数据进行比对
                        compare = distance(feature_arr[k], known_arr[i])
                        # 找到了相似脸
                        if compare == True:
                            user_info = conn.findById("face_info", "id", i + 1)

                            namelist[k] = str(user_info[0][0])
                     # 绘制矩形框
                    for kk, d in enumerate(faces):
                        cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
                # 在人脸框下面写人脸名字
                for i in range(len(faces)):
                    cv2.putText(frame, namelist[i], (faces[i].left(), faces[i].top()), 0, 1.5, (0, 255, 0), 2)
        cv2.imshow('', frame)
    # 释放摄像头
    camera.release()
    # 删除建立的窗口
    cv2.destroyAllWindows()
# 处理存放所有人脸特征的 csv
#采用pandas处理结构化的特征
#读入csv文件
# # 用来存放所有录入人脸特征的数组，默认初始值为空\

def pic_to_mysql(user_id,user_name):
    fp = open("images/"+user_name+".png", 'rb')

    img = fp.read()

    fp.close()

    conn.insetOne("INSERT INTO pic_face (pic_id,pic_name,pic_face) VALUES  (%s,%s,%s)",(user_id,user_name,"images/"+user_name+".png"))
    print("用户信息备份完成")

if __name__ == '__main__':
    face_index()
    #添加新数据选项
    # while True:
    #     print("===================================")
    #     print("=======1.新建样本==================")
    #     print("=======2.人脸识别==================")
    #     print("=======3.退出系统==================")
    #     print("===================================")
    #     key =input("请输入查询指令：")
    #     if key=='1':
    #         user_id = input("Please input your user_id:")
    #         user_name = input("Please input your username:")
    #         flag=conn.findById('face_info','id',user_id)
    #         if len(flag)==0 :
    #             print("=======欢迎进入人脸识别系统=======")
    #             print("=======正在收集您的信息，请等待=======")
    #             get_photo(user_name)
    #             print("=======收集成功，请按Q键保存并退出=======")
    #             try:
    #                 fp = open("images/" + user_name + ".png", 'rb')
    #                 img = fp.read()
    #                 fp.close()
    #                 conn.cursor.execute("insert into face_info values(%s,%s)",(user_name,user_id))
    #                 conn.insetOne("INSERT INTO pic_face (pic_id,pic_name,pic_face) VALUES  (%s,%s,%s)",(user_id, user_name,img))
    #                 conn.db.commit()
    #             except Exception as e:
    #                 print(e)
    #                 print("插入数据失败")
    #             try:
    #                 write_csv("images/"+user_name+".png","data.csv")
    #             except Exception as ret:
    #                 print(ret)
    #                 print("写入失败")
    #             continue
    #         else:
    #             print("输入的id已存在，请重新选择指令！")
    #             continue
    #     elif key=='2':
    #         print("=======识别系统初始化中=======")
    #         face_detect()
    #         continue
    #     elif key=='3':
    #         exit("=======成功退出系统========")
    #     else:
    #         print("输入的指令有误，请重新输入！")
    #执行识别