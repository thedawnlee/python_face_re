import cv2

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