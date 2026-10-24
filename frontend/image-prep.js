// Native decoders apply EXIF orientation. libheif handles HEIF container rotation.
// Do not rotate the decoded pixels again: that would double-rotate phone photos.
export async function preparePhoto(file) {
  if (!file || file.size === 0) throw new Error("Choose a photo first.");
  if (file.size > 25 * 1024 * 1024) throw new Error("Photo is too large. Choose one under 25 MB.");
  if (file.type && !file.type.startsWith("image/")) throw new Error("Choose an image, not a document or other file.");
  let image;
  let url;
  let canvas;
  try {
    url = URL.createObjectURL(file);
    const nativeImage = new Image();
    nativeImage.src = url;
    try {
      await nativeImage.decode();
      image = nativeImage;
    } catch {
      const brand = new TextDecoder().decode(await file.slice(8, 12).arrayBuffer());
      if (!/^(heic|heix|hevc|hevx|mif1|msf1)$/.test(brand)) {
        throw new Error("That file is not a readable photo. Choose a JPEG, PNG, WebP, or HEIC image.");
      }
      const { heicTo } = await import("/vendor/heic-to.js");
      image = await heicTo({ blob: file, type: "bitmap" });
    }
    const width = image.naturalWidth || image.width;
    const height = image.naturalHeight || image.height;
    if (!width || !height || width * height > 60_000_000) {
      throw new Error("Photo dimensions are too large. Choose a smaller photo.");
    }
    const scale = Math.min(1, 1600 / Math.max(width, height));
    canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.round(width * scale));
    canvas.height = Math.max(1, Math.round(height * scale));
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
    const jpeg = await new Promise((resolve, reject) => {
      canvas.toBlob((blob) => blob ? resolve(blob) : reject(new Error("Could not prepare this photo. Try another one.")), "image/jpeg", 0.9);
    });
    if (jpeg.size > 10 * 1024 * 1024) throw new Error("Photo is still too large. Choose a smaller photo.");
    return jpeg;
  } finally {
    if (url) URL.revokeObjectURL(url);
    if (image?.close) image.close();
    if (image instanceof HTMLImageElement) image.src = "";
    if (canvas) { canvas.width = 1; canvas.height = 1; }
  }
}
