import cv2
import numpy as np
import dearpygui.dearpygui  as dpg

def to_rgb(bgr_img):
    return bgr_img[..., [2, 1, 0]]

def normalize(img):
    return img.astype(np.float32) / 255

def run():
    video_file = 'data/1607125853136.mp4'
    cap = cv2.VideoCapture(video_file)
    assert cap.isOpened(), f'can not open video file {video_file}'
    _, first_frame = cap.read()
    h, w = first_frame.shape[:2]

    raw_data = np.zeros((h,w,3), np.float32)
    with dpg.texture_registry():
        texture_id = dpg.add_raw_texture(w, h, raw_data, format=dpg.mvFormat_Float_rgb)
    with dpg.window(label="Main"):
        dpg.add_image(texture_id)

    # equal to dpg.start_dearpygui()
    if not dpg.is_viewport_created():
        dpg.setup_viewport()
    while(dpg.is_dearpygui_running()):
        print('loop----------')
        ret, bgr_img = cap.read()
        if not ret:
            break
        # 需要转换为rgb格式，并归一化到[0, 1]
        norm_rgb_img = normalize(to_rgb(bgr_img))
        raw_data[...] = norm_rgb_img[...]
        dpg.render_dearpygui_frame()   
    dpg.cleanup_dearpygui()


        
if __name__ == '__main__':
    run()