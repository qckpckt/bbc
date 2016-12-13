### Docker build
docker build -t bbc .

### Docker run
docker run -it -p 8000:8000 -v `pwd`:/app --env-file .env bbc_new:latest
