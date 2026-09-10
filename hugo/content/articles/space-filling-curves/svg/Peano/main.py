"""
Peano
"""

joiners = {
    "upwards":    "v -2",
    "downwards":  "v +2",
    "rightwards": "h +2",
    "leftwards":  "h -2",
}

layers = {
    0: {
        "n": tuple(),
        "w": tuple(),
        "s": tuple(),
        "e": tuple(),

        "nf": tuple(),
        "wf": tuple(),
        "sf": tuple(),
        "ef": tuple(),
    }
}

def rotate_180_layer_parts(layer_parts: list[str], n: int) -> list[str]:
    previous_layer = layers[n-1]
    replacement = {
        previous_layer["n"]: previous_layer["s"],
        previous_layer["s"]: previous_layer["n"],
        previous_layer["nf"]: previous_layer["sf"],
        previous_layer["sf"]: previous_layer["nf"],
        joiners["upwards"]: joiners["downwards"],
        joiners["downwards"]: joiners["upwards"],
        joiners["leftwards"]: joiners["rightwards"],
        joiners["rightwards"]: joiners["leftwards"],
    }
    return tuple(replacement[part] for part in layer_parts)

def reflect_path(layer_parts: list[str], n: int) -> list[str]:
    # reflect in y-axis
    previous_layer = layers[n-1]
    replacement = {
        previous_layer["n"]: previous_layer["nf"],
        previous_layer["nf"]: previous_layer["n"],
        previous_layer["s"]: previous_layer["sf"],
        previous_layer["sf"]: previous_layer["s"],
        joiners["upwards"]: joiners["upwards"],
        joiners["downwards"]: joiners["downwards"],
        joiners["leftwards"]: joiners["rightwards"],
        joiners["rightwards"]: joiners["leftwards"],
    }
    return tuple(replacement[part] for part in layer_parts)

def construct_layer(n: int):
    previous_layer = layers[n-1]
    layer_parts_n = (
        previous_layer["n"],
        joiners["upwards"],
        previous_layer["nf"],
        joiners["upwards"],
        previous_layer["n"],

        joiners["rightwards"],

        previous_layer["sf"],
        joiners["downwards"],
        previous_layer["s"],
        joiners["downwards"],
        previous_layer["sf"],

        joiners["rightwards"],

        previous_layer["n"],
        joiners["upwards"],
        previous_layer["nf"],
        joiners["upwards"],
        previous_layer["n"],
    )
    layer_parts_nf = reflect_path(layer_parts_n, n)

    layer_parts_s = rotate_180_layer_parts(layer_parts_n, n)
    layer_parts_sf = rotate_180_layer_parts(layer_parts_nf, n)

    layers[n] = {
        "n": layer_parts_n,
        "s": layer_parts_s,
        "nf": layer_parts_nf,
        "sf": layer_parts_sf,
    }

def flatten(layer):
    non_empty_parts = (part for part in layer if part)
    return " ".join(part if isinstance(part, str) else flatten(part) for part in non_empty_parts)

def main() -> None:
    construct_layer(1)
    construct_layer(2)
    construct_layer(3)
    construct_layer(4)

    tile_of_interest = layers[3]["n"]

    print(flatten(tile_of_interest))

if __name__ == "__main__":
    main()
