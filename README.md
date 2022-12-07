# DFK-Autoplayer

## Docker

# build
docker build -t dfk-autoplay:latest .

# local
docker run -p 9000:8080 dfk-autoplay:latest

### Deploy

# AWS CLI
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 579907623869.dkr.ecr.us-east-1.amazonaws.com 

# Tag
docker tag dfk-autoplayer:latest 579907623869.dkr.ecr.us-east-1.amazonaws.com/dfk-autoplayer:latest

# Push
docker push 579907623869.dkr.ecr.us-east-1.amazonaws.com/dfk-autoplayer:latest
