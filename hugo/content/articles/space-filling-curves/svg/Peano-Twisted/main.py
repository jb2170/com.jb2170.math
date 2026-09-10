"""
Idea 1: Level 1 Tile

#########
#       #
# HHH H #
# H H H #
# H H H #
# H H H #
# H HHH #
#       #
#########

Start with a 'level-1' 'north' tile defined by 'v -4 h +2 v +4 h +2 v -4'
and also consider its rotated east south and west variants.
Join them up as 'N v -2 W v -2 N h +2 E v +2 S v +2 E h +2 N v -2 W v -2 N'
to create the next-level north tile.
In this way we are expanding 'upwards' through the levels, starting with level-1.

Idea 2: Empty Quantum Level 0

How about we start with an empty level 0 tile. This would indicate to us that:
1. The pattern is determined purely by the joiners, ie that there is no need for a
   'quantum' level-1 tile, because a level-0 empty tile satisfies.
2. We can expand 'downwards' by replacing the empty quantum tile with a self-similar copy.
   ~~Perhaps there is some Noetherian-like symmetry going on here.~~
   Do we want to see our recursive process as creating level-(n+1) 'upwards' by conjoining
   level-n tiles together, or do we want to see it as creating level-(n+1) 'downwards' by
   replacing at the heart of level-n tiles the empty quantum level-0 tiles with level 1 tiles?

Idea 3: Empty Diagonals

Instead of referring to the tiles by N E S W, looking at level-1 tiles and the overall direction
traversed within them more carefully indicates that it would be more obvious
to referring to them as NE NW SE SW compass directions.

Idea 4: Nonempty Diagonals

What would tiles look like if they had non-empty level 0 tiles? I conjecture that this would just be a
'tensor-product-like' composition of two tiles, and perhaps both of them still have empty quantum.
Maybe this is a reason why the Penrose Tiling is so interesting. It cannot be reduced to an empty quantum? [citation needed tbh].

"""

joiners = {
    "upwards":    "v -2",
    "downwards":  "v +2",
    "rightwards": "h +2",
    "leftwards":  "h -2",
}

layers = {
    0: {
        "ne": tuple(),
        "nw": tuple(),
        "se": tuple(),
        "sw": tuple(),
    }
}

# Octagonal-ish version
# Not as pleasing as I thought it might be
# layers = {
#     0: {
#         "ne": ("l +2 -2",),
#         "nw": ("l -2 -2",),
#         "se": ("l +2 +2",),
#         "sw": ("l -2 +2",),
#     }
# }

def rotated_layer_parts(layer_parts: list[str], n: int) -> list[str]:
    previous_layer = layers[n-1]
    replacement = {
        previous_layer["ne"]: previous_layer["nw"],
        previous_layer["nw"]: previous_layer["sw"],
        previous_layer["sw"]: previous_layer["se"],
        previous_layer["se"]: previous_layer["ne"],
        joiners["upwards"]: joiners["leftwards"],
        joiners["leftwards"]: joiners["downwards"],
        joiners["downwards"]: joiners["rightwards"],
        joiners["rightwards"]: joiners["upwards"],
    }
    return tuple(replacement[part] for part in layer_parts)

def construct_layer(n: int):
    previous_layer = layers[n-1]
    layer_parts_ne = (
        previous_layer["ne"],
        joiners["upwards"],
        previous_layer["nw"],
        joiners["upwards"],
        previous_layer["ne"],
        joiners["rightwards"],
        previous_layer["se"],
        joiners["downwards"],
        previous_layer["sw"],
        joiners["downwards"],
        previous_layer["se"],
        joiners["rightwards"],
        previous_layer["ne"],
        joiners["upwards"],
        previous_layer["nw"],
        joiners["upwards"],
        previous_layer["ne"],
    )
    layer_parts_nw = rotated_layer_parts(layer_parts_ne, n)
    layer_parts_sw = rotated_layer_parts(layer_parts_nw, n)
    layer_parts_se = rotated_layer_parts(layer_parts_sw, n)
    layers[n] = {
        "ne": layer_parts_ne,
        "nw": layer_parts_nw,
        "sw": layer_parts_sw,
        "se": layer_parts_se,
    }

# really bad code because we want to keep the SVG code for the
# layer-1 all on one line

# def flatten_tile

# poorly named constants
N_IN_TILE = 9
N_CONJOIN_TILES = N_IN_TILE - 1
N_BASE = N_IN_TILE + N_CONJOIN_TILES

# def tile_flatten_main

# def tile_flatten_ish(layer, indent_level: int = 1):
#     # we don't want to recurse down to level-0, the empty quantum
#     # instead we want to recurse down to level-1, because it makes sense
#     # for the SVG. Mathematically yes we could go down to level-0.
#     if layer[0] == tuple():
#         # level-1 tile
#         # clear out the empty `tuple()`s so we don't have empty spaces
#         indent = " " * (indent_level - 1)
#         return indent + " ".join(tuple(part for part in layer if isinstance(part, str)))
#     else:
#         indent = " " * indent_level
#         str_parts = tuple(indent + part if isinstance(part, str) else tile_flatten_ish(part, indent_level = indent_level + 1) for part in layer)
#         return "\n".join(str_parts)

def tile_flatten_ish_0(write_to: list, layer, indent_level: int = 0):
    indent = " " * indent_level
    for part in layer:
        if isinstance(part, str):
            write_to.append(f"{indent}{part}\n")
        else:
            tile_flatten_ish_0(write_to, part, indent_level + 1)

def tile_flatten_ish_1(write_to: list, layer, indent_level: int = 0):
    indent = "  " * indent_level
    if not layer[0]:
        # level-0, so `layer` is level-1
        s = indent + " ".join(part for part in layer if isinstance(part, str)) + "\n"
        write_to.append(s)
    else:
        for part in layer:
            if isinstance(part, str):
                s = f"{indent}{part}\n"
                write_to.append(s)
            else:
                tile_flatten_ish_1(write_to, part, indent_level - 1)

def flatten(layer):
    non_empty_parts = (part for part in layer if part)
    return " ".join(part if isinstance(part, str) else flatten(part) for part in non_empty_parts)

def main() -> None:
    construct_layer(1)
    construct_layer(2)
    construct_layer(3)
    construct_layer(4)

    tile_of_interest = layers[3]["ne"]

    # write_to = []
    # tile_flatten_ish_1(write_to, tile_of_interest, 3)
    # print("".join(write_to), end="")

    print(flatten(tile_of_interest))

if __name__ == "__main__":
    main()
