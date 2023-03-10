import os
from datetime import datetime
from github import Github
from quart import Quart, render_template, url_for, request

app = Quart(__name__, static_folder="templates")
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', None)
github = Github(GITHUB_TOKEN)

@app.route('/')
async def home():
    return await render_template("index.html")


@app.route('/file', methods=['POST'])
async def file():
    files = await request.files
    file_request = files['file']
    repo = github.get_repo('GlauciaLS/x9-bot')

    audios = list(map(lambda audio: audio.name, repo.get_contents('resources/audio')))
    gifs = list(map(lambda gif: gif.name, repo.get_contents('resources/gif')))

    if validate_file(file_request, audios, gifs):
        return "Arquivo inválido!"

    if file_request.mimetype == "image/gif":
        path = "gif"
    else:
        path = "audio"

    create_pull_request(file_request, path)

    return "OK!"


@app.route('/soundtrack', methods=['POST'])
async def soundtrack():
    files = await request.files
    file_request = files['file']

    if file_request.mimetype not in ["audio/mpeg"]:
        return "Tipo de arquivo inválido!"

    create_pull_request(file_request, "soundtracks")

    return "OK!"


def create_pull_request(file_request, path):
    repo = github.get_repo('GlauciaLS/x9-bot')
    base = repo.get_branch('main')

    # Create branch
    name_branch = f"feat/{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}"
    new_branch = repo.create_git_ref(f"refs/heads/{name_branch}", base.commit.sha)

    # Commit new file
    new_file_content = file_request.read()
    new_file_path = f"resources/{path}/{file_request.filename}"

    repo.create_file(new_file_path, f'feat: adicionando {file_request.filename}', new_file_content,
                     branch=new_branch.ref)

    # Create PR
    repo.create_pull(title=f"Adição de novo recurso: \"{file_request.filename}\"",
                     body=f"Adição de novo recurso: \"{file_request.filename}\" através da ferramenta automatizada.",
                     head=new_branch.ref, base="main")


def validate_file(file_request, audios, gifs):
    return (file_request.mimetype not in ["image/gif", "audio/mpeg"]) or (file_request.filename in audios) or (
                file_request.filename in gifs)