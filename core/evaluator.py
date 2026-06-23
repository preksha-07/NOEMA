from core.qubo import compute_energy

def evaluate_paths(paths, Q):
    results = []

    for idx, path in enumerate(paths):
        energy = compute_energy(path, Q)

        results.append({
            "id": idx,
            "path": path,
            "energy": energy
        })

    return results