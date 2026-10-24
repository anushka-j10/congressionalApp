"""A1 measurement fixtures, separate from runtime reading and the M1 originals."""

import argparse
import hashlib
import json
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

from eval.generate_samples import SAMPLES, load_font, render_clean

VARIANTS = ("rotation", "perspective", "blur", "shadow", "noise", "compression", "phone_mix")
PARAMETERS = {
    "rotation_degrees": 3.5,
    "perspective_inverse_coefficients": [1.0, 0.03, -30, -0.025, 1.01, 25, 0.00006, -0.000035],
    "blur_radius": 1.3,
    "shadow_min": 105, "shadow_max": 245,
    "noise_max_delta": 16,
    "jpeg_quality": 25,
    "default_jpeg_quality": 90,
    "phone_mix": {"rotation_degrees": 2.2, "blur_radius": 0.85, "jpeg_quality": 30, "all_six_effects": True},
    "seed": 212026,
}


def add_shadow(image):
    width, height = image.size
    # A directional low-light gradient, not a change to the source text.
    gradient = Image.new("L", (width, 1))
    gradient.putdata([int(PARAMETERS["shadow_min"] + (PARAMETERS["shadow_max"] - PARAMETERS["shadow_min"]) * x / max(1, width - 1)) for x in range(width)])
    return ImageChops.multiply(image, gradient.resize((width, height)).convert("RGB"))


def add_noise(image, seed):
    noise = Image.frombytes("L", image.size, random.Random(seed).randbytes(image.width * image.height))
    noise = noise.point(lambda value: round(128 + (value - 128) * PARAMETERS["noise_max_delta"] / 128))
    return ImageChops.add(image, noise.convert("RGB"), offset=-128)


def degrade(image, variant, seed):
    result = image.copy()
    combined = variant == "phone_mix"
    if variant == "rotation" or combined:
        result = result.rotate(PARAMETERS["phone_mix"]["rotation_degrees"] if combined else PARAMETERS["rotation_degrees"],
                               resample=Image.Resampling.BICUBIC, fillcolor=(220, 217, 205))
    if variant == "perspective" or combined:
        result = result.transform(result.size, Image.Transform.PERSPECTIVE,
                                  PARAMETERS["perspective_inverse_coefficients"],
                                  resample=Image.Resampling.BICUBIC, fillcolor=(220, 217, 205))
    if variant == "shadow" or combined:
        result = add_shadow(result)
    if variant == "blur" or combined:
        result = result.filter(ImageFilter.GaussianBlur(PARAMETERS["phone_mix"]["blur_radius"] if combined else PARAMETERS["blur_radius"]))
    if variant == "noise" or combined:
        result = add_noise(result, seed)
    return result


def generate(root, font_path=None):
    root.mkdir(parents=True, exist_ok=True)
    clean, degraded = root / "clean", root / "degraded"
    clean.mkdir(exist_ok=True)
    degraded.mkdir(exist_ok=True)
    manifest = {"parameters": PARAMETERS, "variants": list(VARIANTS), "sources": [],
                "font_sha256": hashlib.sha256(Path(load_font(font_path).path).read_bytes()).hexdigest()}
    for index, (name, kind, title, deadline, amount, action, _) in enumerate(SAMPLES):
        image, truth = render_clean(index, title, deadline, amount, action, font_path)
        image.save(clean / f"{name}.png")
        (clean / f"{name}.txt").write_text(truth, encoding="utf-8")
        # Add truth to originals, but never rewrite their images or JSON.
        if (root / f"{name}.png").is_file():
            (root / f"{name}.txt").write_text(truth, encoding="utf-8")
        for variant_index, variant in enumerate(VARIANTS):
            seed = PARAMETERS["seed"] + index * 100 + variant_index
            sample = degrade(image, variant, seed)
            quality = PARAMETERS["phone_mix"]["jpeg_quality"] if variant == "phone_mix" else PARAMETERS["jpeg_quality"] if variant == "compression" else PARAMETERS["default_jpeg_quality"]
            stem = f"{name}__{variant}"
            sample.save(degraded / f"{stem}.jpg", quality=quality, subsampling=2)
            (degraded / f"{stem}.txt").write_text(truth, encoding="utf-8")
        manifest["sources"].append({"sample": name, "doc_type": kind,
                                    "ground_truth_sha256": hashlib.sha256(truth.encode()).hexdigest(),
                                    "clean_image_sha256": hashlib.sha256((clean / f"{name}.png").read_bytes()).hexdigest()})
    # Keep corpus metadata outside the original eight expected-field JSON files.
    (root.parent / "reader-corpus.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent / "samples")
    options = parser.parse_args()
    generate(options.root, options.font)
