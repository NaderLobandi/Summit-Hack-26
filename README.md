# Spotware

> **SummitHack26 · Sustainability Track**
>
> Point your camera at a piece of hardware. Get its carbon footprint, recovery value, and a safe disposal action.

**Spotware turns a phone camera into a triage tool for e-waste.** From an unidentified component on a desk to a defensible disposal decision — in under a minute.

## Why this matters

E-waste is the world's fastest-growing solid waste stream — and most of it is misrouted.

| 62 Mt | $91 B | 22.3% |
| --- | --- | --- |
| global e-waste in 2022, up 82% since 2010 | recoverable metals in the annual stream | formal recycling rate worldwide |

<sub>Source: UN Global E-waste Monitor 2024.</sub>

The bottleneck isn't recycling capacity. It's the moment someone holds a device and asks: *"is this worth saving — and how?"* Spotware answers that question.

## How it works

```
Snap ──▶ Identify ──▶ Act
```

1. **Snap** — Upload a photo or use the webcam. No login, no manual data entry.
2. **Identify** — A vision model returns strict JSON: device class, condition, hazards, confidence.
3. **Act** — Embodied CO₂, recoverable value, and a clear action: refurbish, recycle, or review.

## Architecture

Four layers, each replaceable, talking to each other through normalized JSON contracts.

```
image ─▶ perception JSON ─▶ sustainability record ─▶ decision dict ─▶ user-facing action
```

| Layer | File | Role |
| --- | --- | --- |
| **UI** | `Spotware/app.py` | Streamlit shell — routes input, renders cards, holds session state and chat history |
| **Perception** | `perception.py` | Vision (Gemini VLM) — image → strict JSON, 12 required keys, validated & coerced |
| **Knowledge base** | `sustainability_data.json` + `sources.md` | Curated data — embodied CO₂, recoverable metals, value ranges, hazards, citations |
| **Lookup** | `sustainability.py` | Thin safe layer — aliases, always-safe fallback, source tags |
| **Decision** | `decision.py` | Rules + safety gates → a UI-ready recommendation with an audit trace |

### Perception — vision in, strict JSON out

`perception.py` calls a Gemini vision model with a hand-tuned prompt that demands a single JSON object — no markdown, no commentary. It then **validates and coerces** the result: 12 required keys, booleans normalized from strings, confidence clamped to `[0, 1]`. Images are downsized (longest edge ~1600 px) to keep labels readable while cutting upload size and latency. Example output:

```json
{
  "device_class": "GPU",
  "manufacturer": "NVIDIA",
  "model": "A100",
  "visible_text": ["NVIDIA", "A100", "80GB"],
  "condition": "good",
  "form_factor": "PCIe",
  "generation_hint": "modern",
  "data_bearing": true,
  "contains_hazardous": false,
  "completeness": "complete",
  "confidence": 0.92,
  "notes": "PCIe card, no visible damage"
}
```

### Knowledge base — every number traceable

`sustainability_data.json` covers 11 component categories (`gpu`, `cpu`, `psu`, `ram`, `motherboard`, `ssd`, `hdd`, `network_card`, `server_chassis`, `power_network_cable`, plus an `undetected` fallback). Each record carries embodied CO₂ (kg, sourced from manufacturer PCFs), recoverable metals (grams of Cu, Au, Ag, Al, …), `[low, high]` value ranges, hazard flags, and a `default_action`.

- **Why ranges, not midpoints?** An H100 sells for $15k+ used; a GTX 1060 sells for $50. The spread *is* the signal.
- **Always-safe fallback.** The `undetected` record returns nulls and a `manual_review` action — it never suggests landfill and never invents numbers.
- **Provenance.** `sources.md` tags every number to a citation (e.g. `"embodied_co2_source": "nvidia_h100_pcf_2024"`), documents the LCA decomposition methodology, stays conservative under disagreement, and tracks its own corrections.

### Decision — explainable recommendations

`decision.py` starts from the data's `default_action`, then applies ordered safety rules — low confidence, undetected components, hard hazards, VLM hazard flags, damaged condition, missing major parts, and data-bearing devices can each override it. It computes impact fields (CO₂ avoided, USD value, recoverable metals) and emits a `rule_trace` so the UI can show exactly *why* the final recommendation changed.

```json
{
  "action": "secure_wipe_then_refurbish",
  "label": "Secure wipe → refurbish",
  "reason": "Data-bearing SSD in good condition. Mandatory wipe before resale.",
  "co2_avoided_kg": 20,
  "value_usd": 65,
  "metals_total_g": 62.1,
  "rule_trace": [
    "Starting action from ssd default: refurbish_resell",
    "R7 data_bearing=true on refurbish_resell → secure_wipe_then_refurbish"
  ]
}
```

## Project structure

```text
Summit-Hack-26/
  Spotware/
    app.py                  # Streamlit frontend
    analytics_panel.py      # Usage analytics panel
    cache.py                # Local result cache (spotware_cache.db)
    logo1.png, Demo.jpg
  perception.py             # Vision layer (Gemini VLM) → strict JSON
  sustainability.py         # Lookup layer over the knowledge base
  sustainability_data.json  # Curated component knowledge base
  sources.md                # Citations & methodology for every number
  decision.py               # Decision engine (rules + safety gates)
  test_decision.py          # Tests for the decision rules
  requirements.txt
  images/                   # Sample component images by category
```

## Prerequisites

- Python 3.10+ (3.11/3.12 recommended)
- A Gemini API key

## Setup

1. Open a terminal in the repo root.

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the repo root (next to `perception.py`) — see `.env.example`:

   ```env
   GEMINI_API_KEY=your_real_key_here
   # or: GOOGLE_API_KEY=your_real_key_here

   # optional, defaults to gemini-2.5-flash
   GEMINI_MODEL=gemini-2.5-flash
   ```

## Run locally

From the repo root:

```bash
streamlit run Spotware/app.py
```

Streamlit prints a local URL (typically `http://localhost:8501`) — open it in your browser.

### Using the app

1. Upload an image or take a photo with webcam capture.
2. Click **Run analysis**.
3. Review the identification (device class, manufacturer, model, confidence), the sustainability snapshot (embodied CO₂, scrap/refurb value, hazard flags), and the suggested action.

### Batch-test perception only

Run perception over a folder of images:

```bash
python perception.py images/gpu --print
```

Outputs JSON files under `<folder>/out` by default.

## Why it scales

- **Data is the product.** Add a new component category by editing `sustainability_data.json` + `sources.md` — no code changes.
- **The VLM is replaceable.** Gemini today, a fine-tuned local model tomorrow — same JSON contract.
- **Strict schema = strict tests.** `test_decision.py` covers the decision rules; perception's required-key set is enforced at the boundary.
- **Localizable.** Per-region price ranges and disposal-action vocabularies swap in via a different JSON file.

Built for individuals and repair cafés, datacenter decommissioning crews (the source tags *are* the compliance record), and municipal e-waste programs.

## Troubleshooting

- **`Set GEMINI_API_KEY or GOOGLE_API_KEY...`** — `.env` is missing, misplaced, or the key is invalid. Ensure `.env` sits in the repo root, next to `perception.py`.
- **`ModuleNotFoundError`** — re-activate your venv and re-run `pip install -r requirements.txt`.
- **Streamlit command not found** — use `python -m streamlit run Spotware/app.py`.
- **Unknown component returned** — perception may output a class not in the lookup table; `sustainability.py` safely falls back to `undetected`.

## Future work

- **Custom vision pipeline** — replace the foundation-model VLM with a YOLO detector + ConvNeXt classifier specialized on data-center hardware, for faster inference and bounding boxes in cluttered scenes.
- **Text perception branch** — scene-text detection/recognition to resolve ambiguous cases by reading model numbers, FCC IDs, and logos directly off the device.
- **Continual learning at scale** — fine-tune on a crawled dataset of hardware photos unified under the UNU-KEYS e-waste taxonomy.

## Team

**Team Spotters** — Nader Lobandi, Andrew Ehrig, James Vescovo, Jaxon Packer

<sub>A hardware sustainability assistant, built in 24 hours for SummitHack26.</sub>
