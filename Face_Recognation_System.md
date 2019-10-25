#基于opencv+Dlib的人脸识别系统
##核心思路
        
        1.获取照片。
        2.保存照片。
        3.导入人脸检测器、人脸预测器、人脸识别模型。
        4.特征提取。
        5.写入csv。
        6.保存用户信息，存入数据库，实现信息持久化。
        7.人脸识别，读取CSV，检测符合度，设置参数，给出判定。
        
        
##核心模块
        
        get_face_infp.py
        get_face_feature.py
        face_predict.py
##模块关键代码
###获取人脸信息模块get_face_info.py
        
    def get_photo(face_name):
        camera = cv2.VideoCapture(0)#打开笔记本自带摄像头
    
        while True:
            ret, frame = camera.read()
    
            cv2.imshow('', frame)
    
            # 按q键拍照保存图片并退出
            if cv2.waitKey(1) == ord('q'):
                cv2.imwrite(face_name+".png", frame)
                break
    
             # 释放摄像头资源
            camera.release()
            cv2.destroyAllWindows()

###读取图片，提取特征写入csv文件模块get_face_feature.py
    
    #数据事先训练好的。
    #创建Dlib人脸检测器对象
    detector = dlib.get_frontal_face_detector()
    
    # 创建Dlib人脸预测器对象
    predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
    
    # 读入Dlib人脸识别模型
    facerec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')
        
    # 返回单张图像的特征函数
    def feature(img):
        #转换为灰度图片，将三维问题转换为二维问题。
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #检测人脸
        faces = detector(img_gray, 1)
        if len(faces) != 0:
            #如果人脸存在绘制形状，作为参数传入人脸人脸预测器对象，返回描述信息。
            shape = predictor(img_gray, faces[0])
            descriptor = facerec.compute_face_descriptor(img_gray, shape)
        else:
            descriptor = 0
        return descriptor   
     # 将照片特征提取出来, 写入 CSV
    def write_csv(face_path, csv_path,user_name):
        #I\O流读取图片，调用feature函数获得图片特征，写入csv。
        image = io.imread(face_path)
        face_feature = feature(image)
        with open('data.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(face_feature)
###读取csv特征文件，进行人脸预测识别face_predict.py
####关键模块Dlib
        
        
        识别原理：
             
             调用人脸检测器，生成128维向量。
             计算摄像头读取的图片的欧式距离，与保存在data.csv中的信息进行比对，判断拟合度。
             给出识别结果
             

####代码实现
    #引入数据库模块，实现用户信息持久化。
    conn = db.DBUtil(username='root',password='12345',databasename='face_recoginition')

    # Dlib 正向人脸检测器
    detector = dlib.get_frontal_face_detector()
    
    # Dlib 人脸预测器
    predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
    
    # Dlib 人脸识别模型
    facerec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')
    #计算欧式距离函数，将一维数据作为参数，生成array数组，求两个向量的差的范数。
    def distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.linalg.norm(feature_1 - feature_2)
        #若欧式距离之差小于0.4则认为是目标人脸存在于识别库中
        if dist > 0.4:
            return False
        else:
            return True

     def face_predict():
        # 处理存放所有人脸特征的 csv
        #采用pandas处理结构化的特征
        #读入csv文件
        csv_rd = pd.read_csv('data.csv', header=None)
        # 用来存放所有录入人脸特征的数组，默认初始值为空
        known_arr = []
        # 读取已知人脸数据
        for i in range(csv_rd.shape[0]):
            someone_arr = []
            #ix：通过行标签进行索引
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
                        # 遍历已知库的人脸特征
                        for i in range(len(known_arr)):
                            # 将得到的人脸信息人脸与已知库人脸数据进行比对
                            compare = distance(feature_arr[k], known_arr[i])
                            # 发现与已知库特征信息匹配的人脸
                            #查询数据库，查询用户姓名
                            if compare == True:
                                user_info = conn.findById("face_name", "id", i + 1)
    
                                namelist[k] = str(user_info[0][0])
                                # if i == 0:
                                #     namelist[k] = 'bisiyun'
                                # elif i==1:
                                #     namelist[k] = 'lst'
                                # elif i==2:
                                #     namelist[k] = 'pig'
                        # 根据目标人脸大小绘制矩形框标注人脸识别出来的区域
                        for kk, d in enumerate(faces):
                            cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
                    # 标注目标人脸信息
                    for i in range(len(faces)):
                        cv2.putText(frame, namelist[i], (faces[i].left(), faces[i].top()), 0, 1.5, (0, 255, 0), 2)
            cv2.imshow('', frame)
        # 释放摄像头
        camera.release()
        # 删除建立的窗口
        cv2.destroyAllWindows()  