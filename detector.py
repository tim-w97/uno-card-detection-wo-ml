from ultralytics import YOLO
from image_transformer import transform_image
from color_detector import determine_color
from uno_classes import UnoCard, Color

import cv2
import config
import numpy

"""
This methods predicts all uno cards from the given image

1. Capture a image from the given camera
2. If it's the robot camera, transform the image so the number detection works better
3. Predict all uno cards and their corresponding positions (1-6)
4. Return an array of tuples (Uno Card, Position)
"""
def predict_uno_cards(camera_index = config.robot_camera) -> [(UnoCard, int)]:
    # Assert the right amount of cards
    card_amount = 1
    if camera_index == config.robot_camera:
        card_amount = 6

    # Preparation
    predict_uno_cards = []
    model = YOLO(config.model_path)
    card_numbers = model.names

    # ignore this code (start)
    # but leave it here so the color detector works
    def patch(a):
        return a.item()

    setattr(numpy, "asscalar", patch)

    # ignore this code (end)
    while len(predict_uno_cards) != card_amount:
        try:
            # Capture the image
            image = capture_picture(camera_index)

            # Predict all uno cards from the image
            result = predict(model, image)

            # Build cards from boxes
            predicted_uno_cards = build_cards(result, image, card_numbers)
        except:
            input("An error occured with the detection. Please check your setup")

    # check if mapping is necessary
    if camera_index == config.stack_camera:
        # transform to correct form
        card, _ = predict_uno_cards[0]
        return [(card, 0)]

    # return the mapped cards
    return map_to_position(predicted_uno_cards)

def build_cards(result, image, card_numbers):
    sol = []
    for box in result.boxes:
        # get the predicted card number
        predicted_class = int(box.cls)
        card_number = card_numbers[predicted_class]

        # get coordinates of the bounding box
        # xyxy means x1 and y1 of the top left corner and x2 and y2 of the bottom right corner
        bounding_boxes = box.xyxy.tolist()

        if len(bounding_boxes) == 0:
            continue

        bounding_box = bounding_boxes[0]

        center_right = (
            int(bounding_box[2]),
            int((bounding_box[1] + bounding_box[3]) / 2)
        )

        color_bgr = image[
            center_right[1],
            center_right[0]
        ]

        color = determine_color(color_bgr)
        uno_card = UnoCard(card_number, color)

        sol.append((uno_card, (bounding_box[0], bounding_box[1])))
    return sol

def predict(model, image):
    results = model(image)

    if len(results) == 0:
        raise "Cannot predict a card"

    return results[0]

def capture_picture(camera_index):
    # capture the image
    camera = cv2.VideoCapture(camera_index)

    ret, frame = camera.read()

    if not ret:
        raise "Failed to capture the image"
    
    # if it's the robot cam, we need to change the perspective so the uno card detection works better
    if camera_index == config.robot_camera:
        frame = transform_image(frame)
    
    return frame


def map_to_position(results: [(UnoCard, (float,float))]) -> [(UnoCard, int)]:
    # 1. remove duplicates
    results = remove_duplicates(results)

    # 2. sort by y
    sort_y(results)

    # 3. sort by x
    sort_x(results)

    # 3. transform cards
    sol = calculate_positions(results)

    return sol

def sort_y(entries: [(UnoCard, float, float)]) -> None:
    length = len(entries)
    for i in range(0, length):
        smallestIdx = i
        for j in range(i + 1, length):
            _, (s_x,s_y) = entries[smallestIdx]
            _, (r_x, r_y) = entries[j]
            if r_y < s_y:
                smallestIdx = j
        tmp = entries[smallestIdx]
        entries[smallestIdx] = entries[i]
        entries[i] = tmp

# Note: That should not be part of the grade
def sort_x(entries: [(UnoCard, float, float)]) -> None:
    for i in range(0, 3):
        smallestIdx = i
        for j in range(i + 1, 3):
            _, (s_x,s_y) = entries[smallestIdx]
            _, (r_x, r_y) = entries[j]
            if r_x < s_x:
                smallestIdx = j     
        tmp = entries[smallestIdx]
        entries[smallestIdx] = entries[i]
        entries[i] = tmp  

    for i in range(3, 6):
        smallestIdx = i
        for j in range(i + 1, 6):
            _, (s_x,s_y) = entries[smallestIdx]
            _, (r_x, r_y) = entries[j]
            if r_x < s_x:
                smallestIdx = j     
        tmp = entries[smallestIdx]
        entries[smallestIdx] = entries[i]
        entries[i] = tmp

def remove_duplicates(entries: [(UnoCard, (float, float))], allowance = 5) -> [(UnoCard, (float, float))]:
    # 1. map all 
    # 2. check in every insertion if entry already exists
    sol = []
    for entry in entries:
        card, (x, y) = entry
        exists = False
        for s in sol:
            card_s, (s_x, s_y) = s
            if abs(s_y - y) <= allowance and abs(s_x - x) <= allowance:
                exists = True
                break
        if not exists:
            sol.append(entry)
    return sol

def calculate_positions(entries: [(UnoCard, (float, float))]) -> [(UnoCard, int)]:
    idx = 3
    sol = []
    for r in entries:
        card, boundings = r
        sol.append((card, idx))
        idx -= 1
        if idx == 0:
            idx = 6
    return sol

# test the method
# cards = predict_uno_cards(
#     image=cv2.imread('uno cards test image.jpeg')
# )
# for card, position in cards:
#     print(card, position)