import cv2
import dlib
import pandas as pd
import numpy as np
import pymysql
import Db_Util as db

conn = db.DBUtil(username='root',password='123456',databasename='face_info')

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

# Dlib 人脸识别模型
facerec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')


# 计算两个128D向量间的欧式距离,将一维数据作为参数，生成array数组，求两个向量的差的范数
# (欧几里得距离)衡量的是多维空间中各个点之间的绝对距离
def distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.linalg.norm(feature_1 - feature_2)
    # 若欧式距离之差小于0.4则认为是目标人脸存在于识别库中
    if dist > 0.4:
        return False
    else:
        return True


# 处理存放所有人脸特征的 csv
#采用pandas处理结构化的特征
#读入csv文件
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
                        user_info = conn.findById("face_info", "id", i+1)

                        namelist[k] = str(user_info[0][0])
                        # if i == 0:
                        #     namelist[k] = 'bisiyun'
                        # elif i==1:
                        #     namelist[k] = 'lst'
                        # elif i==2:
                        #     namelist[k] = 'pig'
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