from kubernetes import client, config
import keplerData
import random
import time


# === Récupération des pods ===

def list_pending_pods(api_instance):
    """Liste tous les pods en attente."""
    pending_pods = []
    ret = api_instance.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if i.status.phase == "Pending":
            pending_pods.append(i)
    return pending_pods

def list_all_pods(api_instance):
    """Liste tous les pods du cluster."""
    ret = api_instance.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print(f"{i.metadata.namespace} {i.metadata.name} {i.status.phase}")

# === Scheduler ===

def schedule_pod(api_instance, pod, node):
    print(f"Pod {pod.metadata.name} programmé sur {node}")
    """Schedule un pod sur un noeud donné."""
    target = client.V1ObjectReference()
    target.kind = "Node"
    target.apiVersion = "v1"
    target.name = node
    body = client.V1Binding(metadata=client.V1ObjectMeta(name=pod.metadata.name), target=target)
    body.target = target
    try:
        api_instance.create_namespaced_binding(namespace=pod.metadata.namespace, body=body, _preload_content=False)
    except client.rest.ApiException as e:
        print(f"Exception when calling CoreV1Api->create_namespaced_binding: {e}")
    time.sleep(3) # Attendre 3 secondes pour que le pod soit effectivement programmé

# === Choix des noeuds ===

def get_random_node(api_instance):
    """Récupère un noeud aléatoire du cluster."""
    nodes = api_instance.list_node().items
    return random.choice(nodes).metadata.name

def get_node_with_less_pods(api_instance):
    """Récupère le noeud avec le moins de pods."""
    nodes = api_instance.list_node().items
    nodes.sort(key=lambda node: len(node.spec.pod_cidr))
    return nodes[0].metadata.name

def get_node_with_less_consumption(api_instance):
    """Récupère le noeud avec la moins de consommation."""
    Lconso = keplerData.getDataKepler(api_instance)
    print(Lconso)
    Lconso.sort(key=lambda node: node[1])
    print('Node with less consumption:', Lconso[0][0], 'with', Lconso[0][1], 'Joules')
    return Lconso[0][0]

# === Main ===

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Scheduler Python démarré. En attente de pods en attente...")
    while True:
        pending_pods = list_pending_pods(v1)
        for pod in pending_pods:
            node = get_node_with_less_consumption(v1)
            schedule_pod(v1, pod, node)               
        time.sleep(2)  # Attendre 2 secondes avant la prochaine vérification

if __name__ == "__main__":
    main()
