from kubernetes import client, config

def main():
    # Load in-cluster config
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods in all namespaces:")
    
    pods = v1.list_pod_for_all_namespaces(watch=False)
    
    for pod in pods.items:
        print(f"{pod.metadata.namespace} - {pod.metadata.name}")

if __name__ == '__main__':
    main()
