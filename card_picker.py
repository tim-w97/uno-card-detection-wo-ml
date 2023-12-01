import math

from control import RobotProxy

pickup_pitch = math.radians(25)
rotation_90 = math.radians(90)

x_pos_prepare = 0.12

x_pos_min = 0.2
x_pos_max = 0.35
x_pos_middle = (x_pos_min + x_pos_max) / 2

y_pos_min = -0.17
y_pos_max = 0.17

z_pos = 0.075
z_pos_up = 0.2

# setting up the robot
print("init")

proxy = RobotProxy()
proxy.connect()


def pick_up_card(card_number):
    if card_number not in range(1, 7):
        raise ValueError(f"card number {card_number} doesn't exist.")

    x_pos = x_pos_min
    y_pos = y_pos_min
    yaw = rotation_90

    if card_number > 3:
        y_pos = y_pos_max
        yaw = -rotation_90

    if card_number % 3 == 2:
        x_pos = x_pos_middle

    if card_number % 3 == 0:
        x_pos = x_pos_max

    # open the grabber in case it's closed
    proxy.release()

    # prepare to pick up a card
    proxy.move(
        x=x_pos_prepare,
        y=y_pos,
        z=z_pos,
        roll=rotation_90,
        pitch=pickup_pitch,
        yaw=yaw
    )

    # pick up card with given card_number
    proxy.move(
        x=x_pos,
        y=y_pos,
        z=z_pos,
        roll=rotation_90,
        pitch=pickup_pitch,
        yaw=yaw
    )

    proxy.grab()

    # move card up
    proxy.move(
        x=x_pos,
        y=y_pos,
        z=z_pos_up,
        roll=rotation_90,
        pitch=pickup_pitch,
        yaw=yaw
    )

    # move to home pose, but little bit higher
    proxy.moveJoints(0, 0.5, -0.7, 0, 0, 0)

    # move to card stack
    proxy.move(
        x=-0.01,
        y=-0.2,
        z=0.14,
        roll=rotation_90,
        pitch=0.6,
        yaw=-rotation_90
    )

    proxy.release()
    proxy.moveToHomePose()


pick_up_card(1)

# disconnecting the robot
proxy.disconnect()