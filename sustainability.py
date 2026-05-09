from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

_DATA_PATH = Path(__file__).with_name("sustainability_data.json")

# Synonyms from perception output -> canonical key in sustainability_data.json
_ALIASES = {
    "graphics_card": "gpu",
    "video_card": "gpu",
    "processor": "cpu",
    "mainboard": "motherboard",
    "hard_drive": "hdd",
    "hard_disk_drive": "hdd",
    "solid_state_drive": "ssd",
    "nic": "network_card",
    "ethernet_card": "network_card",
    "cable": "power_network_cable",
    "network_cable": "power_network_cable",
    "power_cable": "power_network_cable",
    "chassis": "server_chassis",
    "server_case": "server_chassis",
    "unknown": "undetected",
}


def _load_data() -> dict[str, dict[str, Any]]:
    with _DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("sustainability_data.json must be a top-level object")
    return data


_DATA = _load_data()


def normalize_component_name(component_name: str | None) -> str:
    """Return canonical component key used by the sustainability table."""
    if not component_name:
        return "undetected"

    key = component_name.strip().lower().replace("-", "_").replace(" ", "_")
    key = _ALIASES.get(key, key)

    if key in _DATA:
        return key
    return "undetected"


def get_sustainability_record(component_name: str | None) -> dict[str, Any]:
    """Lookup sustainability metadata for a component.

    Always returns a record. Unknown components map to the `undetected` record.
    """
    key = normalize_component_name(component_name)
    record = deepcopy(_DATA[key])
    record["component_type"] = key
    return record


def component_exists(component_name: str | None) -> bool:
    """True if component name resolves to a known, non-fallback component."""
    return normalize_component_name(component_name) != "undetected"


def list_supported_components() -> list[str]:
    """List canonical component names, excluding fallback entry."""
    return sorted(k for k in _DATA.keys() if k != "undetected")


def get_data_sources(component_name: str | None) -> dict[str, str | None]:
    """Return source tags used for the selected component record."""
    record = get_sustainability_record(component_name)
    return {
        "embodied_co2_source": record.get("embodied_co2_source"),
        "materials_source": record.get("materials_source"),
        "refurb_source": record.get("refurb_source"),
    }


__all__ = [
    "component_exists",
    "get_data_sources",
    "get_sustainability_record",
    "list_supported_components",
    "normalize_component_name",
]
