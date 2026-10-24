"""Generate only fictional test documents, never real resident notices."""

import argparse
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

SAMPLES = [
    ("parking_01", "parking_ticket", "PARKING TICKET", "2026-10-29", "45.00", "Pay the fictional parking charge by the deadline.", False),
    ("parking_02", "parking_ticket", "PARKING VIOLATION NOTICE", "2026-11-02", "65.00", "Request a review of the fictional citation by the deadline.", True),
    ("court_01", "court_notice", "MUNICIPAL COURT NOTICE", "2026-11-03", None, "Attend the fictional hearing on the scheduled date.", False),
    ("court_02", "court_notice", "SUMMONS TO DEMONSTRATION COURT", "2026-11-05", None, "Return the fictional response form by the deadline.", True),
    ("utility_01", "utility_bill", "ELECTRIC UTILITY BILL", "2026-11-04", "82.35", "Pay the fictional electric bill by the due date.", False),
    ("utility_02", "utility_bill", "WATER UTILITY BILL", "2026-11-06", "37.20", "Pay the fictional water bill by the due date.", True),
    ("school_01", "school_letter", "SCHOOL LETTER TO FAMILIES", "2026-10-30", None, "Return the fictional school permission form by the deadline.", False),
    ("school_02", "school_letter", "SCHOOL CONFERENCE LETTER", "2026-11-07", None, "Confirm a fictional parent conference appointment by the deadline.", True),
]


def content_lines(index, deadline, amount, action):
    """Single text source for the image renderer and OCR ground truth."""
    return [
        "Fictional Notice Decoder Demonstration Office",
        "Recipient: Invented Resident " + chr(65 + index),
        "100 Example Lane, Demo Town, ZZ 00000",
        "Reference: SYNTHETIC-ONLY-" + str(index + 1).zfill(3),
        "Issued: 2026-10-21", "", "Deadline: " + deadline,
        "Amount due: " + ("$" + amount if amount else "Not specified"), "",
        "What to do: " + action, "",
        "This invented document is for software testing only.",
        "No real agency, person, case, account, or payment is involved.",
        "Contact: placeholder only; do not send money or personal data.",
    ]


def render_clean(index, title, deadline, amount, action, font_path=None):
    """Return the original, undegraded layout and its exact visible text."""
    font, heading = load_font(font_path), load_font(font_path, 38)
    image = Image.new("RGB", (1200, 1550), (252, 250, 245))
    draw = ImageDraw.Draw(image)
    banner = "SYNTHETIC SAMPLE - NOT A REAL NOTICE"
    draw.text((90, 100), banner, font=font, fill="black")
    draw.text((90, 205), title, font=heading, fill="black")
    wrapped_lines = []
    y = 320
    for line in content_lines(index, deadline, amount, action):
        for wrapped in textwrap.wrap(line, width=58) or [""]:
            draw.text((90, y), wrapped, font=font, fill=(25, 25, 25))
            wrapped_lines.append(wrapped)
            y += 49
    truth = "\n".join([banner, "", title, ""] + wrapped_lines) + "\n"
    return image, truth


def load_font(path=None, size=30):
    candidates = [path] if path else [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    raise RuntimeError("Pass --font with a readable TrueType font path.")


def generate(destination, font_path=None):
    destination.mkdir(parents=True, exist_ok=True)
    for index, (name, kind, title, deadline, amount, action, photo) in enumerate(SAMPLES):
        image, _ = render_clean(index, title, deadline, amount, action, font_path)
        if photo:
            image = image.rotate(1.7 if index % 4 == 1 else -1.5,
                                 resample=Image.Resampling.BICUBIC, fillcolor=(215, 211, 201))
            # A smooth two-direction light gradient, with no randomness.
            light = Image.new("L", image.size)
            pixels = light.load()
            for y in range(image.height):
                for x in range(image.width):
                    pixels[x, y] = int(190 + 45 * x / image.width + 15 * y / image.height)
            image = ImageChops.multiply(image, light.convert("RGB"))
            image = image.filter(ImageFilter.GaussianBlur(0.35))
        image.save(destination / f"{name}.png")
        expected = {
            "synthetic": True, "doc_type": kind, "deadline": deadline,
            "amount": amount, "action": action,
            "image_effects": ["rotation", "uneven_lighting", "mild_blur"] if photo else [],
        }
        (destination / f"{name}.json").write_text(json.dumps(expected, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--font")
    options = parser.parse_args()
    generate(Path(__file__).resolve().parent / "samples", options.font)
