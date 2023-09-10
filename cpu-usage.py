# cpu-usage.py - by DFT 2023-09-10
import psutil
import cv2
import numpy as np
import math

AppName = "cpu-usage.py"

cv2_timer = 50  # Sleep timer

cpu_timer = 0.250

bgColor = 199

image = None

width, height = 250, 120

center_x, center_y = width // 2, height - 1


def image_init():
    global bgColor, width, height, image
    image = bgColor * np.ones((height, width, 3), dtype=np.uint8)


def draw_semi_circle():
    global image, center_x, center_y
    color = (99, 199, 9)
    thickness = 2
    radius = 100
    start_angle = 180
    end_angle = 360
    cv2.ellipse(image, (center_x, center_y), (radius, radius), 0, start_angle, end_angle, color, thickness)
    radius -= 5
    thickness = -1
    color = (48, 115, 30)
    cv2.ellipse(image, (center_x, center_y), (radius, radius), 0, start_angle, 300, color, thickness)

    color = (0, 200, 255)  
    cv2.ellipse(image, (center_x, center_y), (radius, radius), 0, 300, 340, color, thickness)

    color = (37, 0, 255)
    cv2.ellipse(image, (center_x, center_y), (radius, radius), 0, 340, 360, color, thickness)

    i = 180
    while i <= 360:
        if i % 10 == 0:
            draw_line_inside_semi_circle(i, (225, 255, 255), 2, 100, 85)
        elif i % 5 == 0:
            draw_line_inside_semi_circle(i, (75, 99, 99), 2, 100, 90)

        i += 1
    radius = 55
    thickness = -1
    color = (199, 222, 222)
    cv2.ellipse(image, (center_x, center_y), (radius, radius), 0, start_angle, end_angle, color, thickness)


def draw_line_inside_semi_circle(position, color=(0, 0, 0), thickness=5, radius=100, radius_i=0):
    global image, center_x, center_y

    xi = center_x + int(radius_i * math.cos(math.radians(position)))
    yi = center_y + int(radius_i * math.sin(math.radians(position)))
    end_x = center_x + int(radius * math.cos(math.radians(position)))
    end_y = center_y + int(radius * math.sin(math.radians(position)))
    center_point = (xi, yi)
    cv2.line(image, center_point, (end_x, end_y), color, thickness)


def draw_line_inside_semi_circle2(position, color=(0, 0, 0), thickness=5, radius=100, radius_i=0):
    global image, center_x, center_y

    xi = center_x + int(radius_i * math.cos(math.radians(position)))
    yi = center_y + int(radius_i * math.sin(math.radians(position)))
    end_x = center_x + int(radius * math.cos(math.radians(position)))
    end_y = center_y + int(radius * math.sin(math.radians(position)))
    center_point = (xi, yi)
    cv2.line(image, center_point, (end_x, end_y), (255, 55, 255), thickness + 3)
    cv2.line(image, center_point, (end_x, end_y), color, thickness)


def write_text(message):
    global image, center_x, center_y
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    font_color = (55, 55, 55)  
    font_thickness = 2

    text_size = cv2.getTextSize(message, font, font_scale, font_thickness)[0]
    text_x = center_x - text_size[0] // 2
    text_y = height - 20  
    
    cv2.putText(image, message, (text_x, text_y), font, font_scale, font_color, font_thickness)


def home():
    global AppName, width, height, image, cpu_timer, cv2_timer

    cv2.namedWindow(AppName, cv2.WINDOW_NORMAL)

    cv2.resizeWindow(AppName, width, height)

    image_init()

    draw_semi_circle()

    while True:

        image_init()

        draw_semi_circle()

        cpu_usage = psutil.cpu_percent(cpu_timer, True)

        perc = ((((np.max(cpu_usage) * 180) / -100) - 180) * -1)

        i_perc = int(((180 - perc) * -100) / 180)

        draw_line_inside_semi_circle2(perc, (0, 25, 255), 3, 100, 15)

        write_text(str(i_perc) + "%")

        cv2.imshow(AppName, image)

        key = cv2.waitKey(cv2_timer)

        if key == ord("q"):
            break

    cv2.waitKey(0)

    cv2.destroyAllWindows()


home()
