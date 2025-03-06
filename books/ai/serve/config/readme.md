## serving model use Kserve

### install kserve
https://github.com/kserve/kserve
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.16.0/kserve.yaml
```

### install kserve-controller
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.16.0/kserve-controller.yaml
```

### install kserve-runtimes
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.16.0/kserve-runtimes.yaml
```

### install kserve-models
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.16.0/kserve-models.yaml
```

### install kserve-inferenceservice
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.16.0/kserve-inferenceservice.yaml
```

### install kserve-metrics-collector
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.16.0/kserve-metrics-collector.yaml
``` 






