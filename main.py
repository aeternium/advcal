import random

import requests
from nicegui import ui

# Festive theme CSS
festive_css = """
<style>
    /* Background for the whole page */
    body {
        background-color: #3d1e1e; /* Darkish red */
        color: #f5f5f5; /* Light text for contrast */
        font-family: 'Arial', sans-serif;
    }

    /* Card styling */
    .card-festive {
        background-color: #5a2a2a; /* Slightly lighter red */
        border-radius: 12px;
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
        padding: 20px;
        border: 2px solid #9a6a6a; /* Subtle border */
    }

    /* Headings */
    .text-gold {
        color: #ffd700; /* Gold for festive sparkle */
        font-weight: bold;
    }

    /* Button styling */
    .button-festive {
        background-color: #8b4513; /* Darker, warm brown */
        color: #f5f5f5;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button-festive:hover {
        background-color: #a0522d; /* Darker orange-brown for hover effect */
    }

    /* Decorative elements */
    .highlight-green {
        color: #228b22; /* Deep green for accents */
    }

    /* Snowflake styling */
    .snowflake {
        position: fixed;
        top: -10px; /* Start slightly above the viewport */
        color: white;
        font-size: 1em;
        pointer-events: none;
        animation: fall linear infinite;
    }
    /* Snowflake animation */
    @keyframes fall {
        from {
            transform: translateY(-10px); /* Start above the screen */
            opacity: 1; /* Visible at the top */
        }
        to {
            transform: translateY(100vh); /* Fall to the bottom of the screen */
            opacity: 0; /* Fade out at the bottom */
        }
    }
</style>
"""

# Inject the festive theme CSS into the app's <head> section
ui.add_head_html(festive_css)

# JavaScript for snowfall effect
snow_js = """
<script>
    let snowflakeCount = 0;
    const maxSnowflakes = 50;  // Limit the maximum number of snowflakes

    function createSnowflake() {
        // Check if snowflake count exceeds limit
        if (snowflakeCount >= maxSnowflakes) return;

        const snowflake = document.createElement('div');
        snowflake.classList.add('snowflake');
        snowflake.innerText = '❄';
        
        // Randomize size, position, and speed
        snowflake.style.left = Math.random() * 100 + 'vw';
        snowflake.style.fontSize = Math.random() * 1.5 + 0.5 + 'em';
        snowflake.style.animationDuration = Math.random() * 5 + 3 + 's';

        document.body.appendChild(snowflake);
        snowflakeCount++;  // Increment the snowflake count

        // Remove snowflake after falling out of view and decrement count
        snowflake.addEventListener('animationend', () => {
            snowflake.remove();
            snowflakeCount--;  // Decrement the snowflake count
        });
    }

    // Create snowflakes at intervals
    setInterval(createSnowflake, 200);
</script>
"""

# Inject JavaScript for snowfall effect
ui.add_body_html(snow_js)


files = requests.get("https://picsum.photos/v2/list?page=4&limit=24").json()

days = list(range(24))
random.shuffle(days)

ui.page_title("Adventkalender")
ui.label("Adventkalender").classes("text-gold").tailwind().font_size("5xl").font_weight("bold").text_align(
    "center"
).width("full")


with (
    ui.dialog() as dialog,
    ui.card().style("max-width: none") as card,
    ui.image() as full_image,
    ui.page_sticky(x_offset=18, y_offset=18).style("background: none"),
    ui.button(icon="download").classes("button-festive") as button,
):
    dialog
    card.classes("card-festive").tailwind().width("full").max_height("full").max_width("full")
    button.props("fab")


def fullscreen_image(file):
    full_image.set_source(file)
    button.clear()
    button.on_click(lambda url=file: ui.download(url))
    dialog.open()


with ui.row() as row:
    row.tailwind().flex_basis("1").justify_content("evenly")
    for day in days:
        with ui.card().classes("card-festive") as card:
            card.on("click", lambda f=files[day]["download_url"]: fullscreen_image(f))
            with (
                ui.image(f"https://picsum.photos/id/{files[day]['id']}/600/400") as image,
                ui.label(f"{day + 1 }.") as label,
            ):
                image.style("min-width: 27vw")
                label.classes("absolute-bottom text-subtitle2 text-center")
                label.tailwind().font_size("3xl").font_weight("black")

ui.run(port=8089)
