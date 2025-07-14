from flask import Flask, request, render_template, send_file, Response
import os
import uuid
from datetime import datetime
import yt_dlp

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
            'cookiefile': 'youtube.com_cookies.txt'  # ✅ 쿠키 파일 지정
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

@app.route("/index_en.html")
def index_en():
    return render_template("index_en.html")

@app.route("/index_jp.html")
def index_jp():
    return render_template("index_jp.html")

@app.route("/robots.txt")
def robots():
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://talktime.shop/sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")

@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = [
        '/',
        '/index_en.html',
        '/index_jp.html',
        '/about',
        '/privacy',
        '/terms',
        '/contact'
    ]

    base_url = "https://talktime.shop"
    lastmod = datetime.utcnow().date().isoformat()

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{base_url}{page}</loc>")
        xml.append(f"    <lastmod>{lastmod}</lastmod>")
        xml.append("    <changefreq>monthly</changefreq>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")
    xml_content = "\n".join(xml)
    return Response(xml_content, mimetype='application/xml')

if __name__ == "__main__":
    app.run(debug=True)
