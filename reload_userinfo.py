import Db_Util
from skimage import io
import os
import get_face_feature
import pandas as pd
import csv
conn = Db_Util.DBUtil(password="123456",databasename="face_info")
#用户信息读入数据库
#图片的整体存取
#存入不同的数据库
#csv文件逐行存入数据库
#图片加载到数据库中
def pic_to_mysql(user_id,user_name):
    fp = open("images/"+user_name+".png", 'rb')
    img = fp.read()
    fp.close()
    conn.insetOne("INSERT INTO pic_face (pic_id,pic_name,pic_face) VALUES  (%s,%s,%s)",(user_id,user_name,img))
    print("用户信息备份完成")
#用户信息获取
#用户图片获取
def get_pic_face():
    res = conn.Listall("pic_face")
    for i in res:
        f = open("images\\"+i[1]+"1.png","wb")
        f.write(i[2])
        f.close()
    print("用户信息获取完成")
#用户信息重写
def reload_pic_to_csv():
    path = "images"
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    for i in imagePaths:
        get_face_feature.write_csv(i,"data.csv")
    print("数据重载完成")
#从数据库中取出数据写入到csv当中
def reload_mysql_to_csv():
    flag = 0
    res = conn.Listall("pic_face")
    for i in res:
        f = open("images\\" + i[1] + "1.png", "wb")
        f.write(i[2])
        f.close()
        get_face_feature.write_csv_1("images\\" + i[1] + "1.png","data.csv")
        flag+=1
        print("用户信息重重载完成"+str(flag)+"条")
#将csv文件中的数据加载到数据库
def load_csvfile_to_mysql():
    conn.cursor.execute("delete from csv_data")
    with open("data.csv") as f:
        for line in f:
            conn.insetOne("insert into csv_data values(%s)",line)
            print("插入完成")
        conn.db.commit()
def load_mysql_to_csv():
    res = conn.Listall("csv_data")
    with open("data.csv","w") as f:
        f.truncate()
        writer = csv.writer(f)
        for i in res:
            f.write(i[0])
        f.close()
    print("数据重载完成")
if __name__ == '__main__':
    admin_name = input("admin name:")
    admin_pwd = input("admin pwd:")
    while True:
        conn.cursor.execute("select * from admin where username='%s' and userpassword='%s'" % (admin_name, admin_pwd))
        res = conn.cursor.fetchall()
        if len(res) > 0:
            while True:
                print("""欢迎进入用户信息重载系统===============""")
                print("=====1.备份csv文件到数据库===============")
                print("=====2.数据库信息储存到csv===============")
                print("=====3.用户照片信息下载从数据库下载到本地=")
                print("=====4.用户图片从本地上传到数据库=========")
                key_operate = input("您的指令：")
                if key_operate == "1":
                    load_csvfile_to_mysql()
                elif key_operate == "2":
                    load_mysql_to_csv()
                elif key_operate == "3":
                    get_pic_face()
                elif key_operate == "4":
                    user_id = input("your user id")
                    user_name = input("your user name")
                    pic_to_mysql(user_id, user_name)
                else:
                    exit("指令错误系统关闭")
        elif len(res)==0:
            print("用户名或密码输入错误")
            admin_name = input("admin name:")
            admin_pwd = input("admin pwd:")
        else:
            exit("未知错误，系统关闭")

