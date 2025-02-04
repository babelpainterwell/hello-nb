# hello-nb

a tool to help English speakers interpret social media comments (hidden slang) in Chinese using LLM.

#### Build the docker image

```bash
docker build -t hellonb:latest .
```

#### Run the docker container

```bash
docker run -e PORT=8080 -p 8000:8080 hellonb
```

#### Google Artifact Registry Repo

```bash
hellonb-first-docker-repo
```

#### Authenticate to the Google Artifact Registry

```bash
gcloud auth configure-docker us-east1-docker.pkg.dev
```

#### Tag the docker image

```bash
docker tag hellonb:latest us-east1-docker.pkg.dev/hellonb-448704/hellonb-first-docker-repo/hellonb:latest
```

#### Push the docker image to the Google Artifact Registry

```bash
docker push us-east1-docker.pkg.dev/hellonb-448704/hellonb-first-docker-repo/hellonb:latest
```
