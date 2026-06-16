import json
import os
from typing import Optional

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin_config.json")

CLASSES: list[str] = [
    "Cardboard",
    "Plastic packaging",
    "Plastic bottle",
    "Glass jar",
    "Organic",
    "Metal can",
]

DEFAULT_CONFIG: dict = {
    "bins": {
        "cardboard": "#8B4513",
        "organic":   "#4CAF50",
        "plastic":   "#FFD700",
        "pant":      "#FF9800",
        "pmd":       "#2196F3",
    },
    "class_assignments": {
        "Cardboard":          "cardboard",
        "Plastic packaging":  "pmd",
        "Plastic bottle":     "pant",
        "Glass jar":          "pmdd",
        "Organic":            "organic",
        "Metal can":          "pmd",
    },
}

def load_config() -> dict:
    """Load and return the full configuration dict from disk."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as fh:
            return json.load(fh)
    # Return a deep copy of the default so the caller can mutate it safely
    return json.loads(json.dumps(DEFAULT_CONFIG))

def get_bin_for_class(class_name: str) -> Optional[str]:
    config = load_config()
    return config["class_assignments"].get(class_name)


def get_color_for_class(class_name: str) -> Optional[str]:
    config = load_config()
    bin_name = config["class_assignments"].get(class_name)
    if bin_name:
        return config["bins"].get(bin_name)
    return None


def get_all_class_info() -> dict[str, dict]:
    config = load_config()
    result: dict[str, dict] = {}
    for cls in CLASSES:
        bin_name = config["class_assignments"].get(cls)
        color    = config["bins"].get(bin_name) if bin_name else None
        result[cls] = {"bin": bin_name, "color": color}
    return result


# Public functions

def get_cardboard_info() -> dict:
    return {
        "bin":   get_bin_for_class("Cardboard"),
        "color": get_color_for_class("Cardboard"),
    }

def get_plastic_packaging_info() -> dict:
    return {
        "bin":   get_bin_for_class("Plastic packaging"),
        "color": get_color_for_class("Plastic packaging"),
    }

def get_plastic_bottle_info() -> dict:
    return {
        "bin":   get_bin_for_class("Plastic bottle"),
        "color": get_color_for_class("Plastic bottle"),
    }

def get_glass_jar_info() -> dict:
    return {
        "bin":   get_bin_for_class("Glass jar"),
        "color": get_color_for_class("Glass jar"),
    }

def get_organic_info() -> dict:
    return {
        "bin":   get_bin_for_class("Organic"),
        "color": get_color_for_class("Organic"),
    }

def get_metal_can_info() -> dict:
    return {
        "bin":   get_bin_for_class("Metal can"),
        "color": get_color_for_class("Metal can"),
    }
