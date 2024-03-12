import re
import requests

def list_kepler_pods(api_instance):
    """Liste tous les pods en commence par kepler-."""
    kepler_pods = [] # Liste des pods commençant par kepler-
    ret = api_instance.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if i.metadata.name.startswith("kepler-"):
            kepler_pods.append(i)

    return kepler_pods

def get_data_kepler_from_pod(pod, port=9102):
    """Faire un GET sur le port  dans /metrics du pod."""
    url = f"http://{pod.status.pod_ip}:{port}/metrics"
    response = requests.get(url)    
    print(f"GET {url} {response.status_code}")
    return response.text

def filter_data_kepler(data):
    """Filtrer les données pour ne garder que celles qui nous intéressent."""
    conso_totale_joule = 0
    for line in data.split("\n"):
        # Energie consommée par le conteneur
        if line.startswith("kepler_container_core_joules_total{"):
            conso_totale_joule = float(line.split(" ")[-1])
        # Energie consommée par la mémoire DRAM
        elif line.startswith("kepler_container_dram_joules_total{"):
            conso_totale_joule += float(line.split(" ")[-1])
        # Energie consommée par les packages (Node)
        elif line.startswith("kepler_node_core_joules_total{"):
            #conso_totale_joule += float(line.split(" ")[-1])
            name_pod = re.search(r'instance="([^"]*)"', line).group(1)
        # Energie consommée par la mémoire DRAM (Node)
        elif line.startswith("kepler_node_dram_joules_total{"):
            #conso_totale_joule += float(line.split(" ")[-1])
            pass
        # Energie consommée par les packages (Node)
        elif line.startswith("kepler_node_package_joules_total{"):
            #conso_totale_joule += float(line.split(" ")[-1])
            pass
        # Energie consommée par la plateforme (Node)
        elif line.startswith("kepler_node_platform_joules_total{"):
            #conso_totale_joule += float(line.split(" ")[-1])
            pass
            
        
    return conso_totale_joule, name_pod

def getDataKepler(v1):
    Lconso = []
    kepler_pods = list_kepler_pods(v1)
    for pod in kepler_pods:
        data = get_data_kepler_from_pod(pod)
        # On enregistre les données dans un fichier
        with open(f"{pod.metadata.name}.txt", "w") as f:
            f.write(data)
        conso_node, name_pod = filter_data_kepler(data)
        Lconso.append([name_pod, conso_node])
    return Lconso