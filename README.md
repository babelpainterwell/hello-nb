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

To run the container in Google Cloud Run,
**Executables in the container image must be compiled for Linux 64-bit. Cloud Run specifically supports the Linux x86_64 ABI format.**

```bash
docker build --platform=linux/amd64 -t hellonb:latest-cloud .
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
docker tag hellonb:latest-cloud us-east1-docker.pkg.dev/hellonb-448704/hellonb-first-docker-repo/hellonb:latest-cloud
```

#### Push the docker image to the Google Artifact Registry

```bash
docker push us-east1-docker.pkg.dev/hellonb-448704/hellonb-first-docker-repo/hellonb:latest-cloud
```
