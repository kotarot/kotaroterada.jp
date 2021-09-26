# kotaroterada.jp (formerly Bio/CV Generator)

Biography and CV (curriculum vitae) website generation and its deployment to GCP (Google App Engine).


## Requirements

* Python 3


## Usage -- Generate HTML pages

1. Install packages: `pip install -r requirements.txt`.
2. Edit markdown (e.g. `markdown/bio.md`).
3. Edit and set parameters in `bio.conf`.
4. Convert markdown to html: `./build.sh` or individually `./convert.py markdown/bio.md -o app/html/bio.html`.


## Usage -- Run the server on localhost

```bash
cd app

# Run directly with Flask
python main.py
# then go to http://127.0.0.1:5000/

# Run with gunicorn
gunicorn -b 127.0.0.1:8000 main:app
# then go to http://127.0.0.1:8000/
```


## Deploy the app to GCP (GAE)

For manual deployment,

```bash
./build.sh
cd app
gcloud auth login
gcloud app deploy
gcloud app deploy dispatch.yaml
```

For automated deployment, see [GitHub Actions](https://github.com/kotarot/kotaroterada.jp/actions).


## Demo

[https://kotaroterada.jp/bio](https://kotaroterada.jp/bio)
