from tkinter import filedialog  # 導入文件對話框
from PIL import Image, ImageTk, ImageEnhance  # 導入PIL庫中的Image, ImageTk, ImageEnhance
import cv2  # 導入OpenCV
import numpy as np  # 導入NumPy

class ImageProcessor:
    def __init__(self, canvas, left_frame, width_entry, height_entry, blur_type_var):
        """
        初始化ImageProcessor類別

        參數:
        canvas (tk.Canvas): 用於顯示圖片的畫布。
        left_frame (tk.Frame): 包含畫布的框架，用於計算畫布的大小。
        width_entry (tk.Entry): 輸入框，用於輸入新寬度。
        height_entry (tk.Entry): 輸入框，用於輸入新高度。
        blur_type_var (tk.StringVar): 單選框變數，用於選擇模糊類型。
        """
        self.canvas = canvas  # 設置畫布
        self.left_frame = left_frame  # 設置左側框架
        self.width_entry = width_entry  # 設置寬度輸入框
        self.height_entry = height_entry  # 設置高度輸入框
        self.blur_type_var = blur_type_var  # 設置模糊類型變數
        self.scale_factor = 1.0  # 初始縮放比例為1.0
        self.img = None  # 當前顯示的圖片
        self.img_tk = None  # 用於在Tkinter中顯示的圖片
        self.original_img = None  # 用於儲存上傳時的圖片
        self.current_angle = 0  # 當前旋轉角度為0
        self.current_img = None  # 用於儲存當前狀態的圖片
        self.sharpen_factor = 1.0  # 初始銳化比例為1.0
        self.blur_factor = 0.0  # 初始模糊比例為0.0
        self.brightness_factor = 1.0  # 初始亮度比例為1.0
        self.contrast_factor = 1.0  # 初始對比度比例為1.0
        self.saturation_factor = 1.0  # 初始飽和度比例為1.0
        self.is_flipped_horizontally = False  # 水平翻轉狀態
        self.is_flipped_vertically = False  # 垂直翻轉狀態
        self.resized_width = None  # 調整大小後的寬度
        self.resized_height = None  # 調整大小後的高度

    def upload_image(self):
        """
        開啟文件對話框讓使用者選擇圖片並上傳。
        選擇圖片後，重置縮放比例並更新畫布顯示圖片。
        """
        file_path = filedialog.askopenfilename()  # 開啟文件選擇對話框
        if file_path:  # 如果選擇了文件
            self.img = Image.open(file_path)  # 開啟圖片
            self.original_img = self.img.copy()  # 儲存原始圖片
            self.scale_factor = 1.0  # 重置縮放比例
            self.current_angle = 0  # 重置旋轉角度
            self.current_img = self.img.copy()  # 儲存當前狀態
            self.is_flipped_horizontally = False  # 重置水平翻轉狀態
            self.is_flipped_vertically = False  # 重置垂直翻轉狀態
            self.resized_width = None  # 重置調整大小寬度
            self.resized_height = None  # 重置調整大小高度
            self.apply_all_filters()  # 應用所有濾鏡
            self.update_image()  # 更新畫布顯示圖片
            print(f"Image loaded: {file_path}")  # 打印除錯訊息

    def update_image(self):
        """
        根據當前的縮放比例更新畫布顯示的圖片。
        """
        if self.current_img:  # 如果圖片已經載入
            max_width, max_height = self.left_frame.winfo_width(), self.left_frame.winfo_height()  # 獲取畫布的最大寬度和高度
            display_img = self.current_img.copy()  # 複製圖片
            display_img.thumbnail((max_width * self.scale_factor, max_height * self.scale_factor), Image.LANCZOS)  # 按縮放比例調整大小
            self.img_tk = ImageTk.PhotoImage(display_img)  # 將調整後的圖片轉換為Tkinter顯示格式
            self.canvas.delete("all")  # 清除之前的圖片
            
            def update_canvas():
                canvas_width = self.canvas.winfo_width()  # 獲取畫布寬度
                canvas_height = self.canvas.winfo_height()  # 獲取畫布高度
                self.canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=self.img_tk)  # 在畫布中央顯示圖片
                self.canvas.image = self.img_tk  # 保持引用，避免圖片被垃圾回收
                print("Image updated on canvas")  # 打印除錯訊息
            
            self.canvas.after(100, update_canvas)  # 延遲執行，確保畫布已經更新尺寸

    def zoom(self, event):
        """
        根據滾輪事件縮放圖片。
        
        參數:
        event (tk.Event): 滾輪事件對象，包含滾輪滾動的方向。
        """
        if event.delta > 0:  # 滾輪向上滾動
            self.scale_factor *= 1.1  # 放大圖片
        else:  # 滾輪向下滾動
            self.scale_factor /= 1.1  # 縮小圖片
        self.update_image()  # 更新畫布顯示圖片
        print(f"Zoom event: scale_factor = {self.scale_factor}")   # 打印除錯訊息

    def resize_image(self, width, height):
        """
        根據給定的寬度和高度調整圖片大小。
        
        參數:
        width (int): 新的寬度。
        height (int): 新的高度。
        """
        if self.current_img:  # 如果圖片已經載入
            self.resized_width = width  # 儲存調整大小後的寬度
            self.resized_height = height  # 儲存調整大小後的高度
            self.apply_all_filters()  # 應用所有濾鏡
            print(f"Image resized to: {width}x{height}")  # 打印除錯訊息

    def resize_command(self):
        """
        從輸入框獲取寬度和高度值，並調整圖片大小。
        """
        try:
            width_str = self.width_entry.get()  # 獲取寬度輸入框的值
            height_str = self.height_entry.get()  # 獲取高度輸入框的值
            print(f"Width entry value: '{width_str}'")  # 打印除錯訊息
            print(f"Height entry value: '{height_str}'")  # 打印除錯訊息
            
            width = int(width_str)  # 將寬度值轉換為整數
            height = int(height_str)  # 將高度值轉換為整數
            
            print(f"Resizing to width: {width}, height: {height}")   # 打印除錯訊息
            self.resize_image(width, height)  # 調整圖片大小
        except ValueError:
            print("請輸入有效的寬度和高度。")  # 打印錯誤訊息

    def rotate_command(self, angle):
        """
        根據給定的角度旋轉圖片。

        參數:
        angle (int): 旋轉角度。
        """
        if self.original_img:  # 如果圖片已經載入
            self.current_angle = angle  # 設定旋轉角度
            self.apply_all_filters()  # 應用所有濾鏡
            print(f"Image rotated to {angle} degrees")  # 打印除錯訊息

    def flip_vertical(self):
        """
        垂直翻轉圖片。
        """
        if self.current_img:  # 如果圖片已經載入
            self.is_flipped_vertically = not self.is_flipped_vertically  # 切換垂直翻轉狀態
            self.apply_all_filters()  # 應用所有濾鏡
            print("Image flipped vertically")  # 打印除錯訊息

    def flip_horizontal(self):
        """
        水平翻轉圖片。
        """
        if self.current_img:  # 如果圖片已經載入
            self.is_flipped_horizontally = not self.is_flipped_horizontally  # 切換水平翻轉狀態
            self.apply_all_filters()  # 應用所有濾鏡
            print("Image flipped horizontally")  # 打印除錯訊息

    def adjust_brightness(self, brightness_factor):
        """
        調整圖片的亮度。

        參數:
        brightness_factor (float): 亮度調整的比例因子。1.0表示原始亮度，>1.0表示更亮，<1.0表示更暗。
        """
        self.brightness_factor = brightness_factor  # 設定亮度比例
        self.apply_all_filters()  # 應用所有濾鏡
        print(f"Brightness adjusted by factor: {brightness_factor}")  # 打印除錯訊息

    def adjust_contrast(self, contrast_factor):
        """
        調整圖片的對比度。

        參數:
        contrast_factor (float): 對比度調整的比例因子。1.0表示原始對比度，>1.0表示更高對比度，<1.0表示更低對比度。
        """
        self.contrast_factor = contrast_factor  # 設定對比度比例
        self.apply_all_filters()  # 應用所有濾鏡
        print(f"Contrast adjusted by factor: {contrast_factor}")  # 打印除錯訊息

    def adjust_saturation(self, saturation_factor):
        """
        調整圖片的飽和度。

        參數:
        saturation_factor (float): 飽和度調整的比例因子。1.0表示原始飽和度，>1.0表示更高飽和度，<1.0表示更低飽和度。
        """
        self.saturation_factor = saturation_factor  # 設定飽和度比例
        self.apply_all_filters()  # 應用所有濾鏡
        print(f"Saturation adjusted by factor: {saturation_factor}")  # 打印除錯訊息

    def sharpen_image(self, sharpen_factor):
        """
        根據滑桿的值銳化圖片。

        參數:
        sharpen_factor (float): 銳化調整的比例因子。1.0表示原始銳度，>1.0表示更高銳度。
        """
        self.sharpen_factor = sharpen_factor  # 設定銳化比例
        self.apply_all_filters()  # 應用所有濾鏡
        print(f"Image sharpened by factor: {sharpen_factor}")  # 打印除錯訊息

    def blur_image(self, blur_factor):
        """
        根據滑桿的值模糊圖片。

        參數:
        blur_factor (float): 模糊調整的比例因子。0.0表示原始模糊度，越大越模糊。
        """
        self.blur_factor = blur_factor  # 設定模糊比例
        self.apply_all_filters()  # 應用所有濾鏡
        print(f"Image blurred by factor: {blur_factor}")  # 打印除錯訊息

    def apply_all_filters(self):
        """
        根據當前的各種濾鏡參數應用濾鏡效果。
        """
        if self.original_img:  # 如果圖片已經載入
            self.current_img = self.original_img.copy()  # 複製原始圖片
            if self.current_angle != 0:  # 如果圖片旋轉角度不為0
                self.current_img = self.current_img.rotate(-self.current_angle, expand=True)  # 旋轉圖片
            if self.is_flipped_horizontally:  # 如果圖片水平翻轉
                self.current_img = self.current_img.transpose(Image.FLIP_LEFT_RIGHT)  # 水平翻轉圖片
            if self.is_flipped_vertically:  # 如果圖片垂直翻轉
                self.current_img = self.current_img.transpose(Image.FLIP_TOP_BOTTOM)  # 垂直翻轉圖片
            if self.resized_width and self.resized_height:  # 如果已經調整大小
                self.current_img = self.current_img.resize((self.resized_width, self.resized_height), Image.LANCZOS)  # 調整圖片大小
            if self.brightness_factor != 1.0:  # 如果亮度比例不為1.0
                enhancer = ImageEnhance.Brightness(self.current_img)  # 創建亮度調整器
                self.current_img = enhancer.enhance(self.brightness_factor)  # 調整亮度
            if self.contrast_factor != 1.0:  # 如果對比度比例不為1.0
                enhancer = ImageEnhance.Contrast(self.current_img)  # 創建對比度調整器
                self.current_img = enhancer.enhance(self.contrast_factor)  # 調整對比度
            if self.saturation_factor != 1.0:  # 如果飽和度比例不為1.0
                enhancer = ImageEnhance.Color(self.current_img)  # 創建飽和度調整器
                self.current_img = enhancer.enhance(self.saturation_factor)  # 調整飽和度
            if self.sharpen_factor != 1.0:  # 如果銳化比例不為1.0
                self.apply_opencv_sharpen()  # 使用OpenCV進行銳化處理
            if self.blur_factor != 0.0:  # 如果模糊比例不為0.0
                self.apply_opencv_blur()  # 使用OpenCV進行模糊處理
            self.update_image()  # 更新畫布顯示圖片

    def apply_opencv_sharpen(self):
        """
        使用 OpenCV 拉普拉斯運算子
        """
        if self.current_img:  # 如果圖片已經載入
            img_cv = cv2.cvtColor(np.array(self.current_img), cv2.COLOR_RGB2BGR)  # 將PIL圖片轉換為OpenCV格式
            laplacian = cv2.Laplacian(img_cv, cv2.CV_64F)  # 使用拉普拉斯運算子進行銳化處理
            sharpened = cv2.convertScaleAbs(img_cv + self.sharpen_factor * laplacian)  # 應用銳化因子
            self.current_img = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))  # 將OpenCV圖片轉換為PIL格式

    def apply_opencv_blur(self):
        """
        使用OpenCV 模糊效果。
        """
        if self.current_img:  # 如果圖片已經載入
            img_cv = cv2.cvtColor(np.array(self.current_img), cv2.COLOR_RGB2BGR)  # 將PIL圖片轉換為OpenCV格式
            blur_type = self.blur_type_var.get()  # 獲取模糊類型
            if blur_type == "average":  # 如果選擇平均模糊
                img_cv = cv2.blur(img_cv, (int(self.blur_factor), int(self.blur_factor)))  # 應用平均模糊
            elif blur_type == "gaussian":  # 如果選擇高斯模糊
                img_cv = cv2.GaussianBlur(img_cv, (int(self.blur_factor) * 2 + 1, int(self.blur_factor) * 2 + 1), 0)  # 應用高斯模糊
            self.current_img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))  # 將OpenCV圖片轉換為PIL格式

    def reset_image(self):
        """
        恢復圖片到上傳時的狀態。
        """
        if self.original_img:  # 如果圖片已經載入
            self.current_img = self.original_img.copy()  # 恢復到原始圖片
            self.scale_factor = 1.0  # 重置縮放比例
            self.current_angle = 0  # 重置旋轉角度
            self.is_flipped_horizontally = False  # 重置水平翻轉狀態
            self.is_flipped_vertically = False  # 重置垂直翻轉狀態
            self.sharpen_factor = 1.0  # 重置銳化比例
            self.blur_factor = 0.0  # 重置模糊比例
            self.brightness_factor = 1.0  # 重置亮度比例
            self.contrast_factor = 1.0  # 重置對比度比例
            self.saturation_factor = 1.0  # 重置飽和度比例
            self.resized_width = None  # 重置調整大小寬度
            self.resized_height = None  # 重置調整大小高度
            self.apply_all_filters()  # 應用所有濾鏡
            print("Image reset to original state")  # 打印除錯訊息

    def save_image(self):
        """
        保存當前圖片到檔案。
        """
        if self.current_img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.current_img.save(file_path)
                print(f"Image saved to {file_path}")  # 打印除錯訊息
