from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
from yt_dlp import YoutubeDL
import os
import shutil
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# إعداد مجلد التحميلات
DOWNLOADS_FOLDER = './downloads'

@app.route('/', methods=['GET', 'POST'])
def index():
    video_title = None  # متغير لتخزين اسم الفيديو
    available_formats = []  # قائمة لتخزين الجودات المتاحة
    if request.method == 'POST':
        video_url = request.form['video_url']
        save_path = request.form.get('save_path', DOWNLOADS_FOLDER)
        video_type = request.form.get('video_type', 'best')

        try:
            # إعداد المكتبة yt_dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'progress_hooks': [download_progress_hook],  # إضافة دالة التقدم
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات الفيديو وتحميله
                info_dict = ydl.extract_info(video_url, download=True)
                video_title = info_dict.get('title', 'غير معروف')  # الحصول على اسم الفيديو
                available_formats = info_dict.get('formats', [])  # الحصول على الجودات المتاحة
                return redirect(url_for('status', title=video_title, path=save_path))  # إعادة التوجيه إلى صفحة الحالة

        except Exception as e:
            return f"حدث خطأ: {e}"
    
    return render_template('index.html', video_title=video_title, available_formats=available_formats)  # تمرير اسم الفيديو والجودات المتاحة إلى القالب


def download_progress_hook(d):
    if d['status'] == 'downloading':
        print("Sending progress update...")
        socketio.emit('progress', {
            'filename': d['filename'],
            'downloaded': d['downloaded_bytes'],
            'total': d['total_bytes'],
            'speed': d['speed'],
            'format': d.get('format'),
            'percentage': d['downloaded_bytes'] / d['total_bytes'] * 100 if d['total_bytes'] > 0 else 0
        })
    elif d['status'] == 'finished':
        print(f"تم التحميل بنجاح: {d['filename']}")
        socketio.emit('finished', {'filename': d['filename']})  # إرسال إشعار بالانتهاء


# لعرض الملفات التي تم تحميلها
@app.route('/downloads/<filename>')
def send_file(filename):
    return send_from_directory(DOWNLOADS_FOLDER, filename)

@app.route('/get_video_title', methods=['POST'])
def get_video_title():
    data = request.get_json()
    video_url = data.get('url')
    title = "غير معروف"  # القيمة الافتراضية
    available_formats = []  # قائمة لتخزين الجودات المتاحة

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            title = info_dict.get('title', 'غير معروف')  # الحصول على اسم الفيديو
            available_formats = info_dict.get('formats', [])  # الحصول على الجودات المتاحة
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({'title': title, 'available_formats': available_formats})  # إعادة الجودات المتاحة مع اسم الفيديو

# إضافة دالة جديدة لعرض صفحة الحالة
@app.route('/status')
def status():
    title = request.args.get('title', 'غير معروف')
    path = request.args.get('path', '')
    return render_template('status.html', title=title, path=path, msg="تم التحميل")  # تحديث الرسالة هنا

if __name__ == '__main__':
    socketio.run(app, debug=True)
