# hello-nb

a tool to help English speakers interpret social media comments (hidden slang) in Chinese using LLM.

#### rate-limiter

#### detect fraud - 5 requests per miniute

#### Build the docker image

```bash
docker build -t hellonb:latest .
```

#### Run the docker container

```bash
docker run -e PORT=8000 -p 8000:8000 hellonb
```
