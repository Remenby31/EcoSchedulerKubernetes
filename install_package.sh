# install helm snap
sudo snap install helm --classic

# install package from helm chart
helm repo add kepler https://sustainable-computing-io.github.io/kepler-helm-chart
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts

helm repo update

helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
helm install kepler kepler/kepler --namespace monitoring --create-namespace
helm install grafana grafana/grafana --namespace monitoring --create-namespace

echo "[i] Go to https://github.com/helm/charts/issues/15742 to fix the issue, if prometheus keep crashing"

