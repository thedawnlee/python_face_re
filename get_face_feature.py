import csv
import dlib
from skimage import io
import cv2

#Dlib 正向人脸检测器,人脸特征提取器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器，训练好的数据
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

# Dlib 人脸识别模型，ResNet残差神经网络：允许原始输入信息直接传到后面的层保护信息的完整性，
# 整个网络只需要学习输入、输出差别的那一部分，简化学习目标和难度
facerec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')


# 返回单张图像的 128D 特征
def feature(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        descriptor = facerec.compute_face_descriptor(img_gray, shape)
    else:
        descriptor = 0
    return descriptor


# 将照片特征提取出来, 写入 CSV
def write_csv(face_path, csv_path):
    image = io.imread(face_path)
    feature_128d = feature(image)
    with open('data.csv', 'a',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(feature_128d)


if __name__ == '__main__':
    write_csv('images/bsy.png', 'data.csv')