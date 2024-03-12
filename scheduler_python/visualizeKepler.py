from kubernetes import client, config
import keplerData
import matplotlib.pyplot as plt
import time

"""Visualize the kepler data in real time."""

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Visualisation des données Kepler démarrée.")
    time_start = time.time()
    data_dict = {}  # Dictionnaire pour stocker les données de chaque nœud

    while True:
        Lconso = keplerData.getDataKepler(v1)
        for data in Lconso:
            node_name = data[0]
            consommation_total = data[1]
            # On plot la valeur sur un graphique
            if node_name not in data_dict:
                data_dict[node_name] = {"Lx": [], "Ly": []}
                
            data_dict[node_name]["Lx"].append(time.time() - time_start)
            data_dict[node_name]["Ly"].append(consommation_total)

        plt.clf()  # Effacer le tracé précédent
        for node_name, data in data_dict.items():
            plt.plot(data["Lx"], data["Ly"], label=node_name)

        plt.xlabel("Temps (s)")
        plt.ylabel("Consommation (Joules)")
        plt.title("Consommation énergétique des noeuds")
        plt.legend()  # Ajouter une légende pour identifier chaque nœud
        plt.draw()
        plt.pause(1)  # Attendre 1 secondes avant la prochaine vérification

if __name__ == "__main__":
    main()