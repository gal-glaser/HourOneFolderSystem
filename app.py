from hashlib import new
from sys import path
from flask import Flask, request, render_template
import os, shutil, json


app = Flask(__name__)
folder_dir = f"{os.path.dirname(__file__)}/folder_system"


@app.route('/', methods=['GET'])
def route():
    path = request.args.get('path') if 'path' in request.args else ""
    path = os.path.join(folder_dir, path)
    try:
        if os.path.isfile(path):
            fp = open(path)
            file = json.load(fp)
            fp.close()
            return file
            # return render_template("file_view.html", path=path, file=file)
        folders = list(os.walk(path))[0][1]
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return {"folders": folders, "files": files}
        # return render_template("folder_view.html", path=path, folders=folders, files=files)
    except IndexError:
        return f'The directory "{path}" does not exist'



@app.route('/all/', methods=['GET'])
def all_routes():
    try:
        folders = {}
        for folder in list(os.walk(folder_dir))[0][1]:
            folders[folder] = get_folders_and_files(os.path.join(folder_dir,folder))
        files = [f for f in os.listdir(folder_dir) if os.path.isfile(os.path.join(folder_dir, f))]
        return {"folders": folders, "files": files}
        # return render_template("folder_view.html", path=path, folders=folders, files=files)
    except IndexError:
        return f'The directory "{folder_dir}" does not exist'


def get_folders_and_files(folder):
    folders = list(os.walk(folder))[0][1]
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if len(folders) == 0:
        return {"folders": [], "files": files}
    result = {}
    for f in folders:
        result[f] = get_folders_and_files(os.path.join(folder_dir,folder, f))
    return {"folders": result, "files": files}



@app.route('/copy/', methods=['POST'])
def copy_folder():
    data = request.get_json()
    if not ("original_path" in  data and "new_path" in data):
        return 'The request must contain original_path and new_path'
    try:
        og_path = os.path.join(folder_dir, data["original_path"])
        nw_path = os.path.join(folder_dir, data["new_path"])
        new_folder_name = os.path.basename(os.path.normpath(og_path))
        nw_path = os.path.join(nw_path,new_folder_name)
        shutil.copytree(og_path, nw_path)
        return f'<h1>The folder "{og_path}" was successfully copied to {nw_path}!</h1>'
    except FileExistsError:
        return f'<h1>A folder with this name already exists, try a different name</h1>'
    except FileNotFoundError:
        return f'<h1>Path does not exist</h1>'


@app.route('/move/', methods=['POST'])
def move_folder():
    data = request.get_json()
    if not ("original_path" in  data and "new_path" in data):
        return 'The request must contain original_path and new_path'
    try:
        if data["original_path"] == "":
            return f'<h1>Not allowed to move main folder</h1>'
        og_path = os.path.join(folder_dir, data["original_path"])
        nw_path = os.path.join(folder_dir, data["new_path"])
        og_exists, nw_exists =  os.path.exists(og_path),  os.path.exists(nw_path)
        if not (og_exists and nw_exists):
            return ("" if og_exists else "<h1>original_path does not exist</h1>") + \
                   ("" if nw_exists else "<h1>new_path does not exist</h1>")
        if not(os.path.isdir(og_path) and os.path.isdir(nw_path)):
            return "<h1>Both paths must be folders</h1>"
        new_folder_name = os.path.basename(os.path.normpath(og_path))
        nw_path = os.path.join(nw_path,new_folder_name)
        shutil.copytree(og_path, nw_path)
        shutil.rmtree(og_path)
        return f'<h1>The folder "{og_path}" was successfully moved to {nw_path}!</h1>'
    except FileExistsError:
        return f'<h1>A folder with this name already exists, try a different name</h1>'
    except FileNotFoundError:
        return f'<h1>Path does not exist</h1>'


@app.route('/createfolder/', methods=['POST'])
def create_folder():
    data = request.get_json()
    if not ("path" in  data and "name" in data):
        return 'The request must contain path and name'
    try:
        os.mkdir(os.path.join(folder_dir, data["path"], data["name"]))
        return f'<h1>The folder "{data["name"]}" was created!</h1>'
    except FileExistsError:
        return f'<h1>A folder with this name already exists, try a different name</h1>'
    except FileNotFoundError:
        return f'<h1>Path does not exist</h1>'


@app.route('/createfile/', methods=['POST'])
def create_file():
    data = request.get_json()
    if not all(arg in data for arg in ("path", "name", "content")):
        return 'The request must contain path, name and content'
    try:
        path = os.path.join(folder_dir, data["path"], f'{data["name"]}.json')
        if os.path.exists(path):
            raise FileExistsError
        with open(path, "w") as fp:
            json.dump(data["content"], fp)
            fp.close()
        return f'<h1>The file "{data["name"]}" was created!</h1>'
    except FileExistsError:
        return f'<h1>A file with this name already exists, try a different name</h1>'
    except KeyError:
        return 'The request must contain path and name'
    except FileNotFoundError:
        return f'<h1>Path does not exist</h1>'


@app.route('/delete/', methods=['DELETE'])
def delete():
    data = request.get_json()
    if 'path' not in data:
        return 'The request must contain path'
    path = os.path.join(folder_dir, data["path"])
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f'<h1>The file "{data["path"]}" was deleted!</h1>'
        shutil.rmtree(path)
        return f'<h1>The folder "{data["path"]}" was deleted!</h1>'
    except FileNotFoundError:
        return f'<h1>Path does not exist</h1>'


if __name__ == "__main__":
    app.run(debug=True)