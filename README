To create a running docker image:

docker build --tag folder-system .
docker run -d -p 5000:5000 folder-system

Examples for using the API:

to get all directory tree (of folder_system):
http://localhost:5000/all/

to get the folders and files in a specific directory:
http://localhost:5000/?path=my%20folder/another%20folder

to show the content of a specific file:
http://localhost:5000/?path=my%20folder/my%20file.json

to create a folder:
http://localhost:5000/createfolder/
{
"name": "folder name",
"path": "containing path"
}

to create a file (you can put any values inside content):
http://localhost:5000/createfile/
{
"name": "my first file",
"content": {
"title": "yay",
"description": "amazing"
},
"path": "lala"
}

to move a folder ("newest folder" moved to be inside "lala"):
http://localhost:5000/move/
{
"original_path": "new/newest folder",
"new_path": "lala"
}

to copy a folder ("newest folder" copied to be inside "lala"):
http://localhost:5000/copy/
{
"original_path": "new/newest folder",
"new_path": "lala"
}

to delete a folder or a file:
http://localhost:5000/delete/
{
"path": "lala/new"
}
or
{
"path": "lala/new/lala/my first file.json"
}
