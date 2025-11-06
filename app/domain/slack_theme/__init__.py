"""Domain primitives for Slack theme generation."""

from .core import (  # noqa: F401
    NB_SLACK_COLORS,
    complete_colors,
    compute_colors_for_theme,
    generate_slack_theme,
    get_theme,
    is_clear,
    retrieve_elligible_colors,
    theme_to_string,
    to_rgb,
)
