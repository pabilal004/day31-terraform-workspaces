# Day 35 — Kubernetes Persistent Storage

## Objective

Learn how Kubernetes Pods use persistent storage through PersistentVolumes (PV) and PersistentVolumeClaims (PVC).

## Concepts

- **PV (PersistentVolume):** provides storage capacity.
- **PVC (PersistentVolumeClaim):** requests storage.
- **Pod:** uses the PVC to access the storage.
- **emptyDir:** temporary Pod storage; data is removed when the Pod is deleted.
- **StorageClass:** supports dynamic storage provisioning.
- **RWO:** ReadWriteOnce.

Relationship:

`Pod → PVC → PV → Storage`

## Hands-on

1. Create the PV:
   ```bash
   kubectl apply -f pv.yaml
   ```

2. Create the PVC:
   ```bash
   kubectl apply -f pvc.yaml
   ```

3. Verify the PV and PVC are bound:
   ```bash
   kubectl get pvc,pv
   ```

4. Create the Pod:
   ```bash
   kubectl apply -f pod.yaml
   ```

5. Write data to the mounted volume:
   ```bash
   kubectl exec day35-pod -- sh -c 'echo "Day 35 persistent data" > /data/test.txt'
   ```

6. Verify the data:
   ```bash
   kubectl exec day35-pod -- cat /data/test.txt
   ```

7. Delete and recreate the Pod:
   ```bash
   kubectl delete pod day35-pod
   kubectl apply -f pod.yaml
   ```

8. Verify that the data survived Pod deletion:
   ```bash
   kubectl exec day35-pod -- cat /data/test.txt
   ```

Expected result:

`Day 35 persistent data`

## Important lesson

Deleting the Pod did not delete the data because the Pod was using a PVC bound to a PV.

The lab PV uses `hostPath` because this practice was performed on a local kind cluster. In production Kubernetes environments, storage is normally provided through a suitable StorageClass and a real storage backend rather than a node-local hostPath.

## Cleanup

When finished with the lab:

```bash
kubectl delete pod day35-pod
kubectl delete pvc day35-pvc
kubectl delete pv day35-pv
```

## Result

Day 35 completed:

- PV created and verified
- PVC created and bound to the PV
- Pod mounted the PVC at `/data`
- Persistent data written successfully
- Data verified after Pod deletion and recreation
- Final test: **10/10**
