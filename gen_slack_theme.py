from __future__ import annotations

import sys

from app.domain.slack_theme import (
    complete_colors,
    compute_colors_for_theme,
    generate_slack_theme,
    get_theme,
    is_clear,
    retrieve_elligible_colors,
    theme_to_string,
    to_rgb,
)

__all__ = [
    "complete_colors",
    "compute_colors_for_theme",
    "generate_slack_theme",
    "get_theme",
    "is_clear",
    "retrieve_elligible_colors",
    "theme_to_string",
    "to_rgb",
]


if __name__ == "__main__":
    doc = """
------------------------------------------------------------------

This script generates a slack theme based on an image's colors.

Run the following command:
$ python3 gen_slack_theme.py <image-path>

------------------------------------------------------------------
    """
    if len(sys.argv) < 2:
        print(doc)
    else:
        filepath = sys.argv[1]
        theme = generate_slack_theme(filepath)
        print(theme)
