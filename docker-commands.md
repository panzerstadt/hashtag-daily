## build (do only this if you want to update your app)
#### before
delete the app of the same name in `kubernetes engine > workloads`
#### then
docker build -t hashtag-app .
docker tag hashtag-app gcr.io/dan-tokyo-server/hashtag-app:latest
gcloud docker -- push gcr.io/dan-tokyo-server/hashtag-app:latest
kubectl run hashtag-app --image=gcr.io/dan-tokyo-server/hashtag-app:latest --port=5000

## deploy
kubectl expose deployment hashtag-app --type=LoadBalancer --target-port=5000 --port 80

## one time
gcloud auth login
gcloud config set project dan-tokyo-server
gcloud container clusters create hashtag-app-cluster --num-nodes=2 --zone=asia-northeast1-a
gcloud container clusters get-credentials hashtag-app-cluster
kubectl get nodes