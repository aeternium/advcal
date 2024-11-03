import random

import requests
from nicegui import ui


files = requests.get("https://picsum.photos/v2/list?page=4&limit=24").json()

days = list(range(24))
random.shuffle(days)

ui.page_title("Adventkalender")
ui.label("Adventkalender").tailwind().font_size("5xl").font_weight("bold").text_align("center").width("full")


with (
    ui.dialog() as dialog,
    ui.card().style("max-width: none") as card,
    ui.image() as full_image,
    ui.page_sticky(x_offset=18, y_offset=18).style("background: none"),
    ui.button(icon="download") as button,
):
    dialog
    card.tailwind().width("full").max_height("full").max_width("full")
    button.props("fab")


def fullscreen_image(file):
    full_image.set_source(file)
    button.clear()
    button.on_click(lambda url=file: ui.download(url))
    dialog.open()


with ui.row() as row:
    row.tailwind().flex_basis("1").justify_content("evenly")
    for day in days:
        with ui.card() as card:
            card.on("click", lambda f=files[day]["download_url"]: fullscreen_image(f))
            with (
                ui.image(f"https://picsum.photos/id/{files[day]['id']}/600/400") as image,
                ui.label(f"{day + 1 }.") as label,
            ):
                image.style("min-width: 27vw")
                label.classes("absolute-bottom text-subtitle2 text-center")
                label.tailwind().font_size("3xl").font_weight("black")

ui.run(port=8089)
