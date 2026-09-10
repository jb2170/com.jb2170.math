"""
Hilbert

Redoing this properly having done the Peano-Twisted curve

Redoing this again after doing Peano normal

-> Hilbert       (manual)
-> Peano Twisted (rotate)
-> Hilbert       (rotate, reverse paths)
-> Peano         (rotate, reflect)
-> Hilbert       (rotate, reflect)
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

def rotate_90_layer_parts(layer_parts: list[str], n: int) -> list[str]:
    previous_layer = layers[n-1]
    replacement = {
        previous_layer["n"]: previous_layer["w"],
        previous_layer["w"]: previous_layer["s"],
        previous_layer["s"]: previous_layer["e"],
        previous_layer["e"]: previous_layer["n"],
        previous_layer["nf"]: previous_layer["wf"],
        previous_layer["wf"]: previous_layer["sf"],
        previous_layer["sf"]: previous_layer["ef"],
        previous_layer["ef"]: previous_layer["nf"],
        joiners["upwards"]: joiners["leftwards"],
        joiners["leftwards"]: joiners["downwards"],
        joiners["downwards"]: joiners["rightwards"],
        joiners["rightwards"]: joiners["upwards"],
    }
    return tuple(replacement[part] for part in layer_parts)

def reflect_path(layer_parts: list[str], n: int) -> list[str]:
    # reflect in y-axis
    previous_layer = layers[n-1]
    replacement = {
        previous_layer["n"]: previous_layer["nf"],
        previous_layer["nf"]: previous_layer["n"],
        previous_layer["w"]: previous_layer["ef"],
        previous_layer["wf"]: previous_layer["e"],
        previous_layer["s"]: previous_layer["sf"],
        previous_layer["sf"]: previous_layer["s"],
        previous_layer["e"]: previous_layer["wf"],
        previous_layer["ef"]: previous_layer["w"],
        joiners["upwards"]: joiners["upwards"],
        joiners["downwards"]: joiners["downwards"],
        joiners["leftwards"]: joiners["rightwards"],
        joiners["rightwards"]: joiners["leftwards"],
    }
    return tuple(replacement[part] for part in layer_parts)

def construct_layer(n: int):
    previous_layer = layers[n-1]
    layer_parts_n = (
        previous_layer["ef"],
        joiners["upwards"],
        previous_layer["n"],
        joiners["rightwards"],
        previous_layer["n"],
        joiners["downwards"],
        previous_layer["wf"],
    )
    layer_parts_nf = reflect_path(layer_parts_n, n)

    layer_parts_w = rotate_90_layer_parts(layer_parts_n, n)
    layer_parts_wf = rotate_90_layer_parts(layer_parts_nf, n)

    layer_parts_s = rotate_90_layer_parts(layer_parts_w, n)
    layer_parts_sf = rotate_90_layer_parts(layer_parts_wf, n)

    layer_parts_e = rotate_90_layer_parts(layer_parts_s, n)
    layer_parts_ef = rotate_90_layer_parts(layer_parts_sf, n)

    layers[n] = {
        "n": layer_parts_n,
        "w": layer_parts_w,
        "s": layer_parts_s,
        "e": layer_parts_e,
        "nf": layer_parts_nf,
        "wf": layer_parts_wf,
        "sf": layer_parts_sf,
        "ef": layer_parts_ef,
    }

def flatten(layer):
    non_empty_parts = (part for part in layer if part)
    return " ".join(part if isinstance(part, str) else flatten(part) for part in non_empty_parts)

def main() -> None:
    construct_layer(1)
    construct_layer(2)
    construct_layer(3)
    construct_layer(4)

    tile_of_interest = layers[4]["n"]

    print(flatten(tile_of_interest))

if __name__ == "__main__":
    main()
