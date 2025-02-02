from PIL import Image
from collections import Counter
from flask import Flask, render_template, request


app = Flask(__name__)
def color_analyze(image,x):
    image = Image.open(image)

    image = image.convert("RGB")

    pixels = list(image.getdata())



    every_pixel = ["#{:02x}{:02x}{:02x}".format(r, g, b) for r, g, b in pixels]




    counts = Counter(pixels)




    top_colors = counts.most_common(x)

    colors = []
    percent = []
    for color in top_colors:
        colors.append(color[0])
        percent.append(str(round(color[1]/len(every_pixel) * 100,2)) + "%")


    top_hex_colors = ["#{:02x}{:02x}{:02x}".format(*color) for color, _ in top_colors]





    return top_hex_colors, percent


picture = "static/img/Picture.png"
starter = "static/img/Starter.png"

@app.route('/')
def home():

    num = 5
    color, percent = color_analyze(starter,num)
    return render_template("index.html", colors=color, percents=percent, num=num, photo=starter)


@app.route('/upload', methods=["POST"])
def uploaded():
    file = request.files["picture"]
    num = request.form.get("num")
    if file:
        file.save(picture)

        color, percent = color_analyze(picture, int(num))
    else:
        color, percent = color_analyze(picture, int(num))
    return render_template("index.html", colors=color, percents=percent, num=num, photo=picture)




if __name__ == "__main__":
    app.run(debug=True)


