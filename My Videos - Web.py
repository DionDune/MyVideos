import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 




basedir = os.path.abspath(os.path.dirname(__file__))
global viddir 

# Put desired directory here. Only prerequisite is that the foler NEEDS to be called Videos, because flask.
viddir = "C:\\Scripts - Flask\\Videos"

viddir_Static = viddir.split("\\")
viddir_Static.pop(len(viddir_Static) - 1)
viddir_Static = "\\".join(viddir_Static)

app = Flask(__name__, static_folder = viddir_Static)
app.config["SQLALCHEMY_DATABASE_URI"] =\
   'sqlite:///' + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    icon = db.Column(db.String(200))

    def __repr__(self):
        return f"<User {self.username}>"




#region Functions

class Continue_First(Exception):
        pass


def filter_videos(videos_list, parameters):
    continue_video = Continue_First()
    
    if len(parameters) == 0:
        return videos_list

    videos = []
    for video in videos_list:
        try:
            for param in parameters:
                if param.lower() not in video.lower():
                    raise continue_video
                videos.append(video)
        except Continue_First:
            continue
    return videos

#endregion


#region AppRoutes

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory("Assets\\", filename, as_attachment=True)


@app.route("/", methods=["POST","GET"])
def page_home():
    params = []
    if request.method == "POST":
        params = [request.form.get("Search_Box")]
    #video_files = filter_videos(os.listdir(f"{viddir}\\Videos"), params)
    #video_files = filter_videos(os.listdir(f"{viddir}\\Videos"), params)
    video_files = filter_videos(os.listdir(f"{viddir}"), params)
    return render_template("home.html", video_files = video_files, account=None)


@app.route("/view/<video>")
def content_view(video):
    is_video = False
    if video.split(".")[-1] in ["mp4", "gif"]:
        is_video = True
    #return render_template("content_view.html", video=video, is_video=is_video, video_files=filter_videos(os.listdir(f"{viddir}\\Videos"), [f".{video.split('.')[-1]}"]))
    return render_template("content_view.html", video=video, is_video=is_video, video_files=filter_videos(os.listdir(f"{viddir}"), [f".{video.split('.')[-1]}"]))


@app.route("/reset")
def reset_database():
    db.drop_all()
    db.create_all()
    return url_for("page_home")

#endregion




if __name__ == "__main__":
    app.run(debug = True)
