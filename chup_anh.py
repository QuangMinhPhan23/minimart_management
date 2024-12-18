import cv2
import os
import shutil
def take_photo(a):
	#Khởi tạo camera
	cap=cv2.VideoCapture(0)

	#Đợi cho camera khởi động
	cv2.waitKey(1000)

	#Chụp ảnh
	ret, frame=cap.read()

	#Lưu ảnh vào file
	cv2.imwrite('captured_image.jpg',frame)
	#Đóng camera
	cap.release()
	#Đóng tất cả các cửa sổ hiển thị
	cv2.destroyAllWindows()
	#Đường dẫn tới tập tin cần đổi tên
	old_file_name='captured_image.jpg'
	#Đường đãn và tên mới cho tập tin cần đổi tên
	new_file_name=a+'_image.jpg'
	#Sử dụng hàm rename() của module os để đổi tên tập tin
	os.rename(old_file_name,new_file_name)
	
	work_directory=os.getcwd()
	destination_folder=os.path.join(work_directory,"images3")
	a=os.path.join(destination_folder,new_file_name)
	os.rename(new_file_name,a)
	return new_file_name

