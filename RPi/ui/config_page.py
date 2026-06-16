import gradio as gr
import json
import os


# Constants (keep in sync with bin_manager.py)

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
        "Glass jar":          "pmd",
        "Organic":            "organic",
        "Metal can":          "pmd",
    },
}


# Config I/O

def _load() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as fh:
            return json.load(fh)
    return json.loads(json.dumps(DEFAULT_CONFIG))


def _save(config: dict) -> None:
    with open(CONFIG_PATH, "w") as fh:
        json.dump(config, fh, indent=2)


# HTML helpers

def _bins_html(config: dict) -> str:
    """Render the bins table with colour swatches."""
    bins = config["bins"]
    if not bins:
        return "<p style='color:#888;font-style:italic;padding:12px;'>No bins defined yet.</p>"

    rows = ""
    for name, color in bins.items():
        rows += f"""
        <tr>
          <td style="padding:9px 18px;border-bottom:1px solid #eee;font-weight:600;font-size:.95em;">
            {name}
          </td>
          <td style="padding:9px 18px;border-bottom:1px solid #eee;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:26px;height:26px;background:{color};border-radius:6px;
                          border:1px solid rgba(0,0,0,.12);flex-shrink:0;
                          box-shadow:0 1px 4px rgba(0,0,0,.12);"></div>
              <code style="font-size:.88em;color:#555;">{color}</code>
            </div>
          </td>
        </tr>"""

    return f"""
    <div style="border:1px solid #e0e0e0;border-radius:10px;overflow:hidden;margin:6px 0 14px;">
      <table style="border-collapse:collapse;width:100%;">
        <thead>
          <tr style="background:#f6f6f6;border-bottom:2px solid #e0e0e0;">
            <th style="padding:10px 18px;text-align:left;font-size:.78em;color:#666;
                       text-transform:uppercase;letter-spacing:.08em;font-weight:700;">Bin</th>
            <th style="padding:10px 18px;text-align:left;font-size:.78em;color:#666;
                       text-transform:uppercase;letter-spacing:.08em;font-weight:700;">Color</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""


def _summary_html(config: dict) -> str:
    """Render the class → bin → color overview table."""
    assignments = config["class_assignments"]
    bins_cfg    = config["bins"]
    rows = ""

    for cls in CLASSES:
        bin_name = assignments.get(cls)
        color    = bins_cfg.get(bin_name) if bin_name else None

        if color:
            color_cell = (
                f"<div style='display:flex;align-items:center;gap:8px;'>"
                f"<div style='width:18px;height:18px;background:{color};border-radius:4px;"
                f"border:1px solid rgba(0,0,0,.12);flex-shrink:0;'></div>"
                f"<code style='font-size:.85em;color:#555;'>{color}</code></div>"
            )
        else:
            color_cell = "<span style='color:#ccc;'>—</span>"

        bin_cell = (
            f"<span style='font-weight:600;'>{bin_name}</span>"
            if bin_name
            else "<span style='color:#bbb;font-style:italic;'>unassigned</span>"
        )

        rows += f"""
        <tr>
          <td style="padding:8px 16px;border-bottom:1px solid #eee;font-size:.93em;">{cls}</td>
          <td style="padding:8px 16px;border-bottom:1px solid #eee;">{bin_cell}</td>
          <td style="padding:8px 16px;border-bottom:1px solid #eee;">{color_cell}</td>
        </tr>"""

    return f"""
    <div style="border:1px solid #e0e0e0;border-radius:10px;overflow:hidden;margin:6px 0;">
      <table style="border-collapse:collapse;width:100%;">
        <thead>
          <tr style="background:#f6f6f6;border-bottom:2px solid #e0e0e0;">
            <th style="padding:10px 16px;text-align:left;font-size:.78em;color:#666;
                       text-transform:uppercase;letter-spacing:.08em;font-weight:700;">Class</th>
            <th style="padding:10px 16px;text-align:left;font-size:.78em;color:#666;
                       text-transform:uppercase;letter-spacing:.08em;font-weight:700;">Bin</th>
            <th style="padding:10px 16px;text-align:left;font-size:.78em;color:#666;
                       text-transform:uppercase;letter-spacing:.08em;font-weight:700;">Color</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""


# Shared update builder

def _full_updates(config: dict) -> list:
    bin_names   = list(config["bins"].keys())
    assignments = config["class_assignments"]

    updates: list = [
        _bins_html(config),
        gr.update(choices=bin_names, value=None),   # edit_bin_dd
        gr.update(choices=bin_names, value=None),   # delete_bin_dd
    ]

    for cls in CLASSES:
        val = assignments.get(cls)
        updates.append(
            gr.update(choices=bin_names, value=(val if val in bin_names else None))
        )

    updates.append(_summary_html(config))
    return updates


# Event handlers

def handle_add_bin(name: str, color: str) -> list:
    name   = name.strip().lower().replace(" ", "_")
    config = _load()

    if not name:
        return ["Bin name cannot be empty."] + _full_updates(config)
    if name in config["bins"]:
        return [f"A bin named **'{name}'** already exists."] + _full_updates(config)

    config["bins"][name] = color
    _save(config)
    return [f"Bin **'{name}'** added with color `{color}`."] + _full_updates(config)


def handle_get_bin_color(bin_name: str) -> str:
    """Pre-fill the colour picker when the user selects a bin to edit."""
    if not bin_name:
        return "#888888"
    config = _load()
    return config["bins"].get(bin_name, "#888888")


def handle_edit_bin(bin_name: str, color: str) -> list:
    config = _load()

    if not bin_name or bin_name not in config["bins"]:
        return ["Please select a valid bin first."] + _full_updates(config)

    config["bins"][bin_name] = color
    _save(config)
    return [f"Color for **'{bin_name}'** updated to `{color}`."] + _full_updates(config)


def handle_delete_bin(bin_name: str) -> list:
    config = _load()

    if not bin_name or bin_name not in config["bins"]:
        return ["Please select a valid bin first."] + _full_updates(config)

    in_use = [cls for cls, b in config["class_assignments"].items() if b == bin_name]
    if in_use:
        classes_fmt = ", ".join(f"**{c}**" for c in in_use)
        return [
            f"Cannot delete **'{bin_name}'** — it is still assigned to: {classes_fmt}. "
            "Reassign those classes first."
        ] + _full_updates(config)

    del config["bins"][bin_name]
    _save(config)
    return [f"Bin **'{bin_name}'** has been deleted."] + _full_updates(config)


def handle_save_assignments(*dropdown_values) -> list:
    config = _load()
    for cls, val in zip(CLASSES, dropdown_values):
        config["class_assignments"][cls] = val if val else None
    _save(config)
    return ["Class assignments saved successfully.", _summary_html(config)]


def handle_refresh_json() -> str:
    return json.dumps(_load(), indent=2)


# UI builder

def build_config():
    # Persist defaults to disk on first run
    init_config = _load()
    if not os.path.exists(CONFIG_PATH):
        _save(init_config)

    bin_names_init   = list(init_config["bins"].keys())
    assignments_init = init_config["class_assignments"]

    # Header
    gr.Markdown(
        "## Bin Configuration\n"
        "Assign a **bin** to each class, and pick a **color** for each bin."
    )

    with gr.Tabs():

        # Class Assignments
        with gr.Tab("Class Assignments"):
            gr.Markdown(
                "For each trash class, choose which bin it should go into. "
                "The bin's color will be used on the RGB light of the device."
            )

            class_dropdowns: list[gr.Dropdown] = []
            for cls in CLASSES:
                dd = gr.Dropdown(
                    label=cls,
                    choices=bin_names_init,
                    value=assignments_init.get(cls),
                    allow_custom_value=False,
                )
                class_dropdowns.append(dd)

            assign_btn    = gr.Button("Save Assignments", variant="primary", size="lg")
            assign_status = gr.Markdown("")

            gr.Markdown("---\n### Current Overview")
            summary_html = gr.HTML(value=_summary_html(init_config))

        # Bin Management
        with gr.Tab("Bin Management"):

            gr.Markdown("### Defined Bins")

            with gr.Row():

                with gr.Column():
                    bins_html_display = gr.HTML(value=_bins_html(init_config))

                # Add new bin
                with gr.Column():
                    with gr.Accordion("Add New Bin", open=False):
                        with gr.Row():
                            new_bin_name = gr.Textbox(
                                label="Bin Name",
                                placeholder="e.g. glass, landfill, residual…",
                                scale=3,
                            )
                            new_bin_color = gr.ColorPicker(label="Color", value="#FF0000", scale=1)
                        add_btn    = gr.Button("Add Bin", variant="primary")
                        add_status = gr.Markdown("")

                    # Edit bin color
                    with gr.Accordion("Edit Bin Color", open=False):
                        with gr.Row():
                            edit_bin_dd = gr.Dropdown(
                                label="Select Bin",
                                choices=bin_names_init,
                                value=None,
                                scale=2,
                            )
                            edit_color = gr.ColorPicker(label="New Color", value="#FF0000", scale=1)
                        edit_btn    = gr.Button("Update Color", variant="primary")
                        edit_status = gr.Markdown("")

                    # Delete bin 
                    with gr.Accordion("Delete Bin", open=False):
                        delete_bin_dd = gr.Dropdown(
                            label="Select Bin to Delete",
                            choices=bin_names_init,
                            value=None,
                        )
                        gr.Markdown(
                            "<small>A bin that is still assigned to one or more classes "
                            "cannot be deleted. Reassign those classes first.</small>"
                        )
                        delete_btn    = gr.Button("Delete Bin", variant="stop")
                        delete_status = gr.Markdown("")

        # Raw Config
        with gr.Tab("Config Preview"):
            gr.Markdown(
                "Live view of `bin_config.json`. "
                "Edit through the other tabs - changes are saved automatically."
            )
            config_code = gr.Code(
                value=json.dumps(init_config, indent=2),
                language="json",
                label="bin_config.json",
                interactive=False,
            )
            refresh_btn = gr.Button("Refresh")
            refresh_btn.click(fn=handle_refresh_json, outputs=[config_code])

    # Wire up events

    # This list order MUST match what _full_updates() returns
    bins_changed_outputs = [
        bins_html_display,
        edit_bin_dd,
        delete_bin_dd,
        *class_dropdowns,
        summary_html,
    ]

    # Add bin
    add_btn.click(
        fn=handle_add_bin,
        inputs=[new_bin_name, new_bin_color],
        outputs=[add_status, *bins_changed_outputs],
    )

    # Pre-fill colour picker when a bin is selected for editing
    edit_bin_dd.change(
        fn=handle_get_bin_color,
        inputs=[edit_bin_dd],
        outputs=[edit_color],
    )

    # Edit bin colour
    edit_btn.click(
        fn=handle_edit_bin,
        inputs=[edit_bin_dd, edit_color],
        outputs=[edit_status, *bins_changed_outputs],
    )

    # Delete bin
    delete_btn.click(
        fn=handle_delete_bin,
        inputs=[delete_bin_dd],
        outputs=[delete_status, *bins_changed_outputs],
    )

    # Save class assignments
    assign_btn.click(
        fn=handle_save_assignments,
        inputs=class_dropdowns,
        outputs=[assign_status, summary_html],
    )
