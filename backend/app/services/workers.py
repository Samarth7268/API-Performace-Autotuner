import os, psutil

def recommend_workers():
    cpu = os.cpu_count() or 2
    mem_gb = psutil.virtual_memory().available / (1024**3)
    if mem_gb < 2:
        return max(1, cpu)
    if mem_gb < 4:
        return cpu + 1
    return cpu * 2 + 1
