import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CREATE EVENT
@kopf.on.create('mycompany.com', 'v1', 'appconfigs')
def create_fn(spec, name, namespace, **kwargs):
    app_name = spec.get('appName', 'defaultapp').lower()
    replicas = spec.get('replicas', 1)

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {"name": app_name, "image": "nginx"}
                    ]
                },
            },
        },
    }

    api = kubernetes.client.AppsV1Api()
    try:
        api.create_namespaced_deployment(namespace=namespace, body=deployment)
        logger.info(f"Deployment '{name}' created with {replicas} replicas for '{app_name}'")
        return {'message': f"Deployment '{name}' created"}
    except ApiException as e:
        logger.error(f"Failed to create Deployment: {e}")
        raise kopf.PermanentError(str(e))


# UPDATE EVENT
@kopf.on.update('mycompany.com', 'v1', 'appconfigs')
def update_fn(spec, name, namespace, **kwargs):
    replicas = spec.get('replicas', 1)

    deployment_patch = {"spec": {"replicas": replicas}}

    api = kubernetes.client.AppsV1Api()
    try:
        api.patch_namespaced_deployment(name=name, namespace=namespace, body=deployment_patch)
        logger.info(f"Deployment '{name}' updated to {replicas} replicas")
        return {'message': "Updated"}
    except ApiException as e:
        logger.error(f"Failed to update deployment: {e}")
        raise kopf.PermanentError(str(e))


# DELETE EVENT
@kopf.on.delete('mycompany.com', 'v1', 'appconfigs')
def delete_fn(name, namespace, **kwargs):
    api = kubernetes.client.AppsV1Api()
    try:
        api.delete_namespaced_deployment(name=name, namespace=namespace)
        logger.info(f"Deployment '{name}' deleted")
    except ApiException as e:
        if e.status != 404:
            raise kopf.PermanentError(str(e))