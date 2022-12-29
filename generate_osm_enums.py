#!/usr/bin/env python3

import argparse
import json
import os.path
import typing
from itertools import chain

import taginfo.query
from tocase.for_strings import ToCase

PRIMARY_FEATURES = [
    "aerialway",
    "aeroway",
    "amenity",
    "barrier",
    "boundary",
    "craft",
    "emergency",
    "geological",
    "healthcare",
    "highway",
    "historic",
    "landuse",
    "leisure",
    "man_made",
    "military",
    "natural",
    "office",
    "place",
    "power",
    "public_transport",
    "railway",
    "route",
    "shop",
    "sport",
    "telecom",
    "tourism",
    "water",
    "waterway",
]


def get_values(key: str) -> list[str]:
    """Download a key's values from `taginfo <https://taginfo.openstreetmap.org/>`_"""
    values = []
    highest_count = None
    for entry in taginfo.query.values_of_key_with_data(key):
        if highest_count is None:
            highest_count = entry["count"]
        elif entry["count"] / highest_count < 0.01:
            break
        else:
            values.append(entry["value"])
    return values


def generate_enum(key: str, values: typing.Iterable[str]) -> str:
    """Generate a rust enum for a specific key"""
    return "\n".join(chain(
        [f"pub enum {ToCase(key).pascal()} {{"],
        (f"\t{ToCase(value).pascal()}," for value in values),
        ["}"],
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tags", help="Json file caching the osm tags", default="tags.json")
    parser.add_argument("--rust", help="Rust file to generate", default="tags.rs")
    args = parser.parse_args()

    if not os.path.exists(args.tags):
        print("Couldn't find cached tags.")
        print("Downloading them...")
        with open(args.tags, "w") as f:
            json.dump({key: get_values(key) for key in PRIMARY_FEATURES}, f)
        print("Finished!")

    with open(args.tags) as f:
        tags: dict[str, list[str]] = json.load(f)

    tags_enum = "\n".join(chain(
        ["pub enum Tag {"],
        (f"\t{ToCase(key).pascal()}({ToCase(key).pascal()})," for key in tags),
        ["}"],
    ))

    with open(args.rust, "w") as f:
        f.write(tags_enum)
        f.write("\n\n")
        for key, values in tags.items():
            f.write(generate_enum(key, values))
            f.write("\n\n")


if __name__ == "__main__":
    main()
