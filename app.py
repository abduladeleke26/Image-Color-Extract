from PIL import Image
from collections import Counter, defaultdict
from flask import Flask, render_template, request
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76

app = Flask(__name__)

def closeColor(color, groups, threshold=15):
    color_lab = rgb2lab(np.array(color, dtype=np.uint8).reshape(1, 1, 3) / 255.0)[0][0]

    for group in groups:
        group_lab = rgb2lab(np.array(group, dtype=np.uint8).reshape(1, 1, 3) / 255.0)[0][0]
        if deltaE_cie76(color_lab, group_lab) < threshold:
            return group
    return None

def color_analyze(image, x, delta):
    image = Image.open(image).convert("RGB")

    image = image.resize((200, 200))

    counts = Counter(image.getdata())

    groups = defaultdict(int)


    for color, count in counts.items():
        closest = closeColor(color, groups, delta)
        if closest:
            groups[closest] += count
        else:
            groups[color] = count


    sortedd = sorted(groups.items(), key=lambda item: item[1], reverse=True)[:x]

    total_pixels = sum(groups.values())

    colors = ["#{:02x}{:02x}{:02x}".format(*color) for color, _ in sortedd]
    percents = [f"{round(count / total_pixels * 100, 2)}%" for _, count in sortedd]

    return colors, percents


picture = "static/img/Picture.png"
starter = "static/img/Starter.png"


@app.route('/')
def home():
    num = 5
    delta = 15
    picture = starter
    colors, percents = color_analyze(starter, num, delta)
    return render_template("index.html", colors=colors, percents=percents, num=num, photo=starter, delta=delta)


@app.route('/colors', methods=["POST"])
def uploaded():
    file = request.files["picture"]
    num = int(request.form.get("num", 5))
    delta = int(request.form.get("delta", 15))
    if file:
        file.save(picture)
    colors, percents = color_analyze(picture, num, delta)
    return render_template("index.html", colors=colors, percents=percents, num=num, photo=picture, delta=delta)


if __name__ == "__main__":
    app.run(debug=True)
