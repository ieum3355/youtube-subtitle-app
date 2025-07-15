
from flask import Flask, request, render_template, send_file, Response
import os
import uuid
from datetime import datetime
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        video_url = request.form["url"]
        subtitle_filename = f"{uuid.uuid4()}.srt"
        cookie_path = os.path.join(os.getcwd(), "youtube.com_cookies.txt")

        ydl_opts = {
            'writesubtitles': True,
            'subtitlesformat': 'srt',
            'skip_download': True,
            'outtmpl': subtitle_filename,
        }

        if os.path.exists(cookie_path):
            ydl_opts["cookiefile"] = cookie_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                if not info.get("requested_subtitles"):
                    message = "⚠️ 자막이 없는 영상입니다. (또는 비공개/연령제한 영상일 수 있습니다)"
                    return render_template("index.html", message=message)
                return send_file(subtitle_filename, as_attachment=True)
        except Exception as e:
            message = f"❌ 오류 발생: {e}"
            return render_template("index.html", message=message)
        finally:
            if os.path.exists(subtitle_filename):
                os.remove(subtitle_filename)

    return render_template("index.html", message=message)

# ✅ 기본 페이지들
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ✅ 다국어 페이지
@app.route("/index_en.html")
def index_en():
    return render_template("index_en.html")

@app.route("/index_jp.html")
def index_jp():
    return render_template("index_jp.html")

@app.route("/about_en")
def about_en():
    return render_template("about_en.html")

@app.route("/about_jp")
def about_jp():
    return render_template("about_jp.html")

@app.route("/privacy_en")
def privacy_en():
    return render_template("privacy_en.html")

@app.route("/privacy_jp")
def privacy_jp():
    return render_template("privacy_jp.html")

@app.route("/terms_en")
def terms_en():
    return render_template("terms_en.html")

@app.route("/terms_jp")
def terms_jp():
    return render_template("terms_jp.html")

@app.route("/contact_en")
def contact_en():
    return render_template("contact_en.html")

@app.route("/contact_jp")
def contact_jp():
    return render_template("contact_jp.html")

# ✅ robots.txt 직접 서빙
@app.route("/robots.txt")
def robots():
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://talktime.shop/sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")

# ✅ sitemap.xml 자동 생성
@app.route("/sitemap.xml")
def sitemap():
    pages = [
        '/', '/index_en.html', '/index_jp.html',
        '/about', '/about_en', '/about_jp',
        '/privacy', '/privacy_en', '/privacy_jp',
        '/terms', '/terms_en', '/terms_jp',
        '/contact', '/contact_en', '/contact_jp'
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
