from flask import Flask, render_template, request
import afvink4

# constructor
app = Flask(__name__)


# URL
@app.route('/', methods=["GET", "POST"])
def nucleotide_to_protein():
    seq = request.args.get("seq", "")
    page_title = "Converter"
    if seq != "":
        translate = afvink4.input(seq)
        return render_template("afvink4.html", seq=seq,
                               page_title=page_title, translate=translate)
    return render_template("afvink4.html", seq=seq, page_title=page_title)


if __name__ == '__main__':
    app.run()