# hello-nb

a tool to help English speakers interpret social media comments (hidden slang) in Chinese using LLM.

Google Translate or built-in translation features only translate words, but slang often carries hidden meanings. Want to truly understand what’s being said and enjoy a more engaging, entertaining experience on RedNote? Try HelloNB! Link to the app: https://hellonb.com/

#### Build the docker image

```bash
docker build -t hellonb:latest .
```

#### Run the docker container

```bash
docker run -e PORT=8080 -p 8080:8080 hellonb
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
docker tag hellonb:latest-cloud us-east1-docker.pkg.dev/deductive-tempo-450104-t0/hellonb-second/hellonb:latest-cloud
```

#### Push the docker image to the Google Artifact Registry

```bash
docker push us-east1-docker.pkg.dev/deductive-tempo-450104-t0/hellonb-second/hellonb:latest-cloud
```

#### For AWS ECR Deployment

```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin 851725289587.dkr.ecr.us-east-1.amazonaws.com
docker build --platform=linux/amd64 -t hellonb:latest-aws .
docker tag hellonb:latest-aws 851725289587.dkr.ecr.us-east-1.amazonaws.com/hellonb-repo:latest
docker push 851725289587.dkr.ecr.us-east-1.amazonaws.com/hellonb-repo:latest
```
