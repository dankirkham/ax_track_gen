import argparse
import json
import struct

start_binary = [
    bytes(
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x00"
    ),
    bytes(b"\x00\x00\x00\x00"),
    bytes(
        b"\x00\x00\x80\x3F" +
        b"\x69\x17\x8C\xBE" +
        b"\xF5\x72\x40\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\xF5\x72\x40\xBF" +
        b"\x69\x17\x8C\xBE" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\xCD\xCC\x4C\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x0A\xD7\xA3\x3E" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x80\x3F"
    )
]

cone_binary = [
    bytes(
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x00"
    ),
    bytes(b"\x00\x00\x00\x00"),
    bytes(
        b"\x00\x00\x80\x3F" +
        b"\x00\x00\x00\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x3F" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x00\x00" +
        b"\x00\x00\x80\x3F"
    )
]

def find_center(cones):
    mini = [10000, 10000]
    maxi = [0, 0]

    for cone in cones:
        if cone[0] < mini[0]:
            mini[0] = cone[0]
        if cone[1] < mini[1]:
            mini[1] = cone[1]

        if cone[0] > maxi[0]:
            maxi[0] = cone[0]
        if cone[1] > maxi[1]:
            maxi[1] = cone[1]

    return [
        mini[0] + ((maxi[0] - mini[0]) / 2),
        mini[1] + ((maxi[1] - mini[1]) / 2)
    ]

def generate_cones(cones, out_file, scale, center):
    for cone in cones:
        x_pixels = cone[0] - center[0]
        y_pixels = cone[1] - center[1]

        x_meters = x_pixels * scale
        y_meters = y_pixels * scale

        print("{}, {}".format(x_meters, y_meters))

        out_file.write(cone_binary[0])
        out_file.write(bytearray(struct.pack("f", x_meters)))
        out_file.write(cone_binary[1])
        out_file.write(bytearray(struct.pack("f", y_meters)))
        out_file.write(cone_binary[2])

def generate_starts(starts, out_file, scale, center):
    for start in starts:
        x_pixels = start[0] - center[0]
        y_pixels = start[1] - center[1]

        x_meters = x_pixels * scale
        y_meters = y_pixels * scale

        print("{}, {}".format(x_meters, y_meters))

        out_file.write(start_binary[0])
        out_file.write(bytearray(struct.pack("f", x_meters)))
        out_file.write(start_binary[1])
        out_file.write(bytearray(struct.pack("f", y_meters)))
        out_file.write(start_binary[2])

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("cone_file")
    parser.add_argument("-o", default="out.bin")

    args = parser.parse_args()

    with open(args.cone_file) as f:
        data = json.load(f)

    out_file = open(args.o, 'wb')

    center = find_center(data['cones'])
    scale = data['metersPerPixel']

    generate_starts([
        data['start']['right'],
        data['start']['left'],
        data['finish']['left'],
        data['finish']['right'],
    ], out_file, scale, center)

    out_file.write(bytearray(struct.pack("I", 4 + len(data['cones']))))

    generate_starts([
        data['start']['left'],
        data['start']['right'],
        data['finish']['left'],
        data['finish']['right'],
    ], out_file, scale, center)

    generate_cones(data['cones'], out_file, scale, center)

    out_file.close()


if __name__ == "__main__":
    main()

# 269 pixels = 95 * 2 ft = 190 ft = 57.912 meters
#    thus 0.21528624535 meters per pixel
