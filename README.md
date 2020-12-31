# CV Generator

CV (curriculum vitae) and biography website generation and its deployment to GCP (Google App Engine).


## Requirements

* Python 3


## Usage

1. Install packages: `pip install -r requirements.txt`.
2. Edit markdown (e.g. `markdown/cv.md`).
3. Edit and set parameters in `cv.conf`.
4. Convert markdown to html: `./build.sh` or individually `./convert.py markdown/cv.md -o app/html/cv.html`.
5. Deploy pages: `./install_local.sh` for example.


## Deploy the app to GCP (GAE)

For manual deployment,

```
./build.sh
cd app
CLOUDSDK_PYTHON=python3 gcloud auth login
CLOUDSDK_PYTHON=python3 gcloud app deploy --project <Your Project ID>
```

For automated deployment, see [GitHub Actions](https://github.com/kotarot/cv-generator/actions).


## Demo
[https://kotaroterada.jp/cv](https://kotaroterada.jp/cv)
