"""AI atmosphere images. Provider is chosen by which key the environment has:

  OPENAI_API_KEY      -> OpenAI Images (model from ZS_OPENAI_IMAGE_MODEL, default gpt-image-1)
  (none)              -> no generation; the skill lists the images a person must supply

Rules (references/images.md): English prompt, photographic, ends with "no people, no text, no logos,
no watermarks"; never real people, never the client's premises presented as real; mark ai: true in site.json.
"""
import base64
import json
import os
import urllib.request

SUFFIX = " Photorealistic, natural light, editorial composition, no people, no faces, no text, no letters, no logos, no watermarks."


def provider():
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return None


def generate(prompt, out_path, size="1536x1024"):
    p = provider()
    if not p:
        raise SystemExit("no image provider configured (set OPENAI_API_KEY on the environment). "
                         "List the needed images for the client instead; see references/images.md")
    full = prompt.rstrip(". ") + "." + SUFFIX
    body = {"model": os.environ.get("ZS_OPENAI_IMAGE_MODEL", "gpt-image-1"), "prompt": full, "size": size, "n": 1}
    if os.environ.get("ZS_OPENAI_IMAGE_QUALITY"):
        body["quality"] = os.environ["ZS_OPENAI_IMAGE_QUALITY"]
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    item = d["data"][0]
    if item.get("b64_json"):
        out_path.write_bytes(base64.b64decode(item["b64_json"]))
    else:
        out_path.write_bytes(urllib.request.urlopen(item["url"], timeout=120).read())
    return out_path
