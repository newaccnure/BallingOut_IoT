import math
import csv


def analyse_data(data, drill_id, frequency):
    high_speed = 0
    with open('drills.csv') as drills_csv:
        reader = csv.reader(drills_csv, delimiter=',')
        for row in reader:
            if int(row[0]) == drill_id:
                high_speed = float(row[1])

    previous = {
        "x_accel": data[0][3],
        "y_accel": data[0][4],
        "z_accel": data[0][5],
    }
    previous_speed = {
        "x_speed": 0,
        "y_speed": 0,
        "z_speed": 0,
    }
    g = 9.81
    speed_recordings = [0]

    for i in range(1, len(data)):
        current = {
            "x_accel": data[i][3],
            "y_accel": data[i][4],
            "z_accel": data[i][5],
        }
        accel_dif = {
            "x_dif": abs(current["x_accel"] - previous["x_accel"]),
            "y_dif": abs(current["y_accel"] - previous["y_accel"]),
            "z_dif": abs(current["z_accel"] - previous["z_accel"]),
        }
        current_speed = {
            "x_dif": previous_speed["x_speed"] + accel_dif["x_dif"] * (1 / frequency) * g,
            "y_dif": previous_speed["y_speed"] + accel_dif["y_dif"] * (1 / frequency) * g,
            "z_dif": previous_speed["z_speed"] + accel_dif["z_dif"] * (1 / frequency) * g
        }
        speed = math.sqrt(
            current_speed["x_dif"] * current_speed["x_dif"]
            + current_speed["y_dif"] * current_speed["y_dif"]
            + current_speed["z_dif"] * current_speed["z_dif"])

        speed_recordings.append(speed)

    s = sum(speed_recordings)
    mark = 10 - abs(high_speed - s / len(speed_recordings)) * 10
    return s / len(speed_recordings), round(0 if mark < 0 else mark, 1)
