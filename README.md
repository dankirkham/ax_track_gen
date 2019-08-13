# Creating A Course Using A Map
1. Create a JSON file similar to the following:
```
{
    "metersPerPixel": 0.45491,
    "start": {
        "left": [365, 242],
        "right": [344, 242]
    },
    "finish": {
        "left": [164, 401],
        "right": [186, 403]
    },
    "cones": [
        [360, 232],
        [358, 233],
        [360, 242],
    ]
}

```
1. Using an image, populate the "cones" array with a list of cones [x, y] pixel coordinates.
2. Populate "start" and "finish" with left and right location of lines.
3. Using a tool such as Google Map's Measure Distance feature, determine the metersPerPixel. This can be done by finding pixels between light poles and the corresponding distance.
4. Invoke the tool using `python ax_track_gen.py <json file> -o default.clf`.
5. Move the `default.clf` to the same directory as [HolyMoose's AX Creator](https://holymooses.com/autocross/)'s `AutocrossCreator.exe` program.
6. Run `AutocrossCreator.exe`.
7. Load layout using `CTRL+L`.
8. Add pointer cones and walls.
9. Export track using `CTRL+E`. `Exported!` should be echo'd in the terminal.
10. `moose_ax_creator.kn5` will be present in the directory and can be loaded in Assetto Corsa.
