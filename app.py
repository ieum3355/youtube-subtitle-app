from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        subtitle_filename = f"{uuid.uuid4()}.srt"

        ydl_opts = {
            'writesubtitles': True,
            'subtitlesformat': 'srt',
            'skip_download': True,
            'outtmpl': subtitle_filename,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                if not info.get("requested_subtitles"):
                    return "⚠️ 자막을 찾을 수 없습니다."

            return send_file(subtitle_filename, as_attachment=True)

        except Exception as e:
            return f"❌ 오류 발생: {e}"

        finally:
            if os.path.exists(subtitle_filename):
                os.remove(subtitle_filename)

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

