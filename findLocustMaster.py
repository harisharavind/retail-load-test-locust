#!/usr/bin/env python

from kubernetes import client, config

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    labelSelector="app=locust-master"
    fieldSelector="status.phase==Running"
    namespace="syncloadtest"
    ret = v1.list_namespaced_pod(namespace, label_selector=labelSelector, field_selector=fieldSelector, watch=False)
    print(ret.items[0].status.pod_ip)
    
if __name__ == '__main__':
    main()
