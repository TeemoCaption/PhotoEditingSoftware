import tkinter as tk
from tkinter import filedialog, ttk
from image_processor import ImageProcessor  # 引用自定義的ImageProcessor類別

# 建立主視窗
root = tk.Tk()
root.title("修圖軟體 v1.0")
# 設定視窗寬高
root.minsize(width=1280, height=720)

# 設定grid佈局
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)  # 左側區域設定較小的比例
root.grid_columnconfigure(1, weight=5)  # 右側區域設定較大的比例

# 建立左側圖片預覽區域
left_frame = tk.Frame(root, bd=2, relief="sunken")
left_frame.grid(row=0, column=0, sticky="nsew")

# 在左側框架中新增一個畫布來顯示圖片
canvas = tk.Canvas(left_frame, bg="gray")
canvas.grid(row=0, column=0, sticky="nsew")

# 調整left_frame的grid設定
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# 建立右側設定區域的畫布
right_canvas = tk.Canvas(root)
right_canvas.grid(row=0, column=1, sticky="nsew")

# 新增垂直捲動條
scrollbar = tk.Scrollbar(root, orient="vertical", command=right_canvas.yview)
scrollbar.grid(row=0, column=2, sticky="ns")
right_canvas.configure(yscrollcommand=scrollbar.set)

# 在畫布上新增一個框架
right_frame = tk.Frame(right_canvas)
right_canvas.create_window((0, 0), window=right_frame, anchor="nw")

# 調整right_frame的grid設定
right_frame.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))

# 字型設定
font_settings = ("微軟正黑體", 12)

# 圖片上傳按鈕
upload_button = tk.Button(right_frame, text="上傳圖片", font=font_settings)
upload_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

# 恢復預設按鈕
reset_button = tk.Button(right_frame, text="恢復預設", font=font_settings)
reset_button.grid(row=0, column=1, pady=10, padx=10, sticky="w")

# 新增保存圖片按鈕
save_button = tk.Button(right_frame, text="保存圖片", command=lambda: image_processor.save_image(), font=font_settings)
save_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")

# 調整圖片大小區域
resize_frame = tk.Frame(right_frame, bd=2, relief="groove")
resize_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="w")

resize_label = tk.Label(resize_frame, text="調整圖片大小", font=font_settings)
resize_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 調整圖片大小的輸入框(寬度)
resize_label_w = tk.Label(resize_frame, text="寬度:", font=font_settings)
resize_label_w.grid(row=1, column=0, pady=10, padx=5, sticky="w")
resize_text_w = tk.Entry(resize_frame, font=font_settings)
resize_text_w.grid(row=1, column=1, pady=10, padx=5, sticky="w")

# 調整圖片大小的輸入框(高度)
resize_label_h = tk.Label(resize_frame, text="高度:", font=font_settings)
resize_label_h.grid(row=1, column=2, pady=10, padx=5, sticky="w")
resize_text_h = tk.Entry(resize_frame, font=font_settings)
resize_text_h.grid(row=1, column=3, pady=10, padx=5, sticky="w")

# 調整圖片大小按鈕
resize_button = tk.Button(resize_frame, text="調整大小", command=lambda: image_processor.resize_command(), font=font_settings)
resize_button.grid(row=1, column=4, pady=10, padx=5, sticky="w")

# 旋轉圖片區域
rotate_frame = tk.Frame(right_frame, bd=2, relief="groove")
rotate_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="w")

rotate_label = tk.Label(rotate_frame, text="旋轉圖片", font=font_settings)
rotate_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 旋轉圖片的滑桿
rotate_slider = tk.Scale(rotate_frame, from_=0, to=360, orient=tk.HORIZONTAL, length=300, font=font_settings)
rotate_slider.grid(row=0, column=1, pady=10, padx=5)

# 旋轉圖片按鈕
rotate_button = tk.Button(rotate_frame, text="旋轉", command=lambda: image_processor.rotate_command(rotate_slider.get()), font=font_settings)
rotate_button.grid(row=0, column=2, pady=10, padx=5)

# 翻轉圖片區域
flip_frame = tk.Frame(right_frame, bd=2, relief="groove")
flip_frame.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="w")

flip_label = tk.Label(flip_frame, text="翻轉圖片", font=font_settings)
flip_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 垂直翻轉圖片按鈕
flip_button_vertical = tk.Button(flip_frame, text="垂直翻轉", command=lambda: image_processor.flip_vertical(), font=font_settings)
flip_button_vertical.grid(row=0, column=1, pady=10, padx=5)

# 水平翻轉圖片按鈕
flip_button_horizontal = tk.Button(flip_frame, text="水平翻轉", command=lambda: image_processor.flip_horizontal(), font=font_settings)
flip_button_horizontal.grid(row=0, column=2, pady=10, padx=5)

# 亮度調整區域
brightness_frame = tk.Frame(right_frame, bd=2, relief="groove")
brightness_frame.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="w")

brightness_label = tk.Label(brightness_frame, text="亮度調整", font=font_settings)
brightness_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 亮度調整滑桿
brightness_slider = tk.Scale(brightness_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=300, font=font_settings)
brightness_slider.grid(row=0, column=1, pady=10, padx=5)
brightness_slider.set(1.0)  # 設定滑桿預設值為1.0

# 亮度調整按鈕
brightness_button = tk.Button(brightness_frame, text="調整亮度", command=lambda: image_processor.adjust_brightness(brightness_slider.get()), font=font_settings)
brightness_button.grid(row=0, column=2, pady=10, padx=5)

# 對比度調整區域
contrast_frame = tk.Frame(right_frame, bd=2, relief="groove")
contrast_frame.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="w")

contrast_label = tk.Label(contrast_frame, text="對比度調整", font=font_settings)
contrast_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 對比度調整滑桿
contrast_slider = tk.Scale(contrast_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=300, font=font_settings)
contrast_slider.grid(row=0, column=1, pady=10, padx=5)
contrast_slider.set(1.0)  # 設定滑桿預設值為1.0

# 對比度調整按鈕
contrast_button = tk.Button(contrast_frame, text="調整對比度", command=lambda: image_processor.adjust_contrast(contrast_slider.get()), font=font_settings)
contrast_button.grid(row=0, column=2, pady=10, padx=5)

# 飽和度調整區域
saturation_frame = tk.Frame(right_frame, bd=2, relief="groove")
saturation_frame.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky="w")

saturation_label = tk.Label(saturation_frame, text="飽和度調整", font=font_settings)
saturation_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 飽和度調整滑桿
saturation_slider = tk.Scale(saturation_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=300, font=font_settings)
saturation_slider.grid(row=0, column=1, pady=10, padx=5)
saturation_slider.set(1.0)  # 設定滑桿預設值為1.0

# 飽和度調整按鈕
saturation_button = tk.Button(saturation_frame, text="調整飽和度", command=lambda: image_processor.adjust_saturation(saturation_slider.get()), font=font_settings)
saturation_button.grid(row=0, column=2, pady=10, padx=5)

# 濾鏡區域
filter_frame = tk.Frame(right_frame, bd=2, relief="groove")
filter_frame.grid(row=7, column=0, columnspan=3, pady=10, padx=10, sticky="w")

filter_label = tk.Label(filter_frame, text="濾鏡效果", font=font_settings)
filter_label.grid(row=0, column=0, pady=10, padx=5, sticky="w")

# 銳化滑桿
sharpen_slider = tk.Scale(filter_frame, from_=1.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, length=300, font=font_settings)
sharpen_slider.grid(row=0, column=1, pady=10, padx=5)
sharpen_slider.set(1.0)  # 設定滑桿預設值為1.0

# 銳化按鈕
sharpen_button = tk.Button(filter_frame, text="調整銳化", command=lambda: image_processor.sharpen_image(sharpen_slider.get()), font=font_settings)
sharpen_button.grid(row=0, column=2, pady=10, padx=5)

# 模糊滑桿
blur_slider = tk.Scale(filter_frame, from_=0.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, length=300, font=font_settings)
blur_slider.grid(row=1, column=1, pady=10, padx=5)
blur_slider.set(0.0)  # 設定滑桿預設值為0.0

# 模糊按鈕
blur_button = tk.Button(filter_frame, text="調整模糊", command=lambda: image_processor.blur_image(blur_slider.get()), font=font_settings)
blur_button.grid(row=1, column=2, pady=10, padx=5)

# 模糊效果選擇框
blur_type_frame = tk.Frame(filter_frame)
blur_type_frame.grid(row=2, column=1, columnspan=3, sticky="w", pady=10)

blur_type_var = tk.StringVar(value="average")
blur_avg_rb = ttk.Radiobutton(blur_type_frame, text="平均濾波器", variable=blur_type_var, value="average")
blur_avg_rb.grid(row=0, column=0, padx=5, sticky='w')

blur_gaussian_rb = ttk.Radiobutton(blur_type_frame, text="高斯濾波器", variable=blur_type_var, value="gaussian")
blur_gaussian_rb.grid(row=0, column=1, padx=5, sticky='w')

# 建立ImageProcessor物件
image_processor = ImageProcessor(canvas, left_frame, resize_text_w, resize_text_h, blur_type_var)

# 上傳圖片按鈕設定事件
upload_button.config(command=image_processor.upload_image)

# 恢復預設按鈕設定事件
reset_button.config(command=image_processor.reset_image)

# 綁定滾輪事件
canvas.bind("<MouseWheel>", image_processor.zoom)

# 循環顯示視窗
root.mainloop()
