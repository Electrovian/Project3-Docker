# Project 3 - Docker Text Processing

## 1) Prepare input files

The repo includes placeholder input files so the image can build locally.
Before final submission, replace these with your course-provided files:

- `IF.txt`
- `AlwaysRememberUsThisWay.txt`

Both files must stay in this `dockerapp` folder.

## 2) Build image

```powershell
cd dockerapp
docker build -t project3-text-processor:latest .
```

## 3) Run container

```powershell
docker run --rm --name project3-run project3-text-processor:latest
```

The container will:

- Read `/home/data/IF.txt` and `/home/data/AlwaysRememberUsThisWay.txt`
- Write `/home/data/output/result.txt`
- Print result content to console, then exit

## 4) Screenshot proof (Docker Desktop + running container)

Because the script exits quickly, run this temporary command to keep the container visible:

```powershell
docker run -d --name project3-screenshot project3-text-processor:latest sh -c "python /app/script.py && sleep 120"
docker ps
```

Take the screenshot:

```powershell
Start-Process "ms-screenclip:"
```

After screenshot:

```powershell
docker rm -f project3-screenshot
```

## 5) Check image size (< 200MB target)

```powershell
docker images project3-text-processor:latest
```

## 6) Export tar for submission

Replace `YOUR_EMAIL_USERNAME` with your school email username.

```powershell
docker save -o YOUR_EMAIL_USERNAME.tar project3-text-processor:latest
```

Validation:

```powershell
docker load -i YOUR_EMAIL_USERNAME.tar
docker run --rm project3-text-processor:latest
```

## 7) Extra credit (Kubernetes with 2 replicas)

Apply manifest:

```powershell
kubectl apply -f k8s/deployment.yaml
kubectl get pods
```

Generate the requested output file:

```powershell
kubectl get pods > kube_output.txt
cat kube_output.txt
```
