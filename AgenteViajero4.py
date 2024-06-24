import itertools

# Matriz de distancias
matriz_dist = [
    [0, 9, 0, 0, 15, 0, 0, 0, 0, 22, 0, 0, 0, 0],     # A
    [9, 0, 11, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # B
    [0, 11, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # C
    [0, 0, 19, 0, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0],    # D
    [15, 17, 0, 15, 0, 0, 14, 16, 0, 0, 0, 0, 0, 0],  # E
    [0, 0, 0, 14, 0, 0, 0, 15, 12, 0, 0, 0, 0, 0],    # F
    [0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 14, 25, 0, 0],    # G
    [0, 0, 0, 0, 16, 15, 0, 0, 15, 0, 0, 17, 0, 0],   # H
    [0, 0, 0, 0, 0, 12, 0, 15, 0, 0, 0, 0, 19, 0],    # I
    [22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],      # J
    [0, 0, 0, 0, 0, 0, 14, 0, 0, 6, 0, 0, 0, 14],     # K
    [0, 0, 0, 0, 0, 0, 25, 17, 0, 0, 0, 0, 18, 18],   # L
    [0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 18, 0, 24],    # M
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 18, 24, 0],    # N
]

# Lista de ciudades
ciudades = list('ABCDEFGHIJKLMN')

# Implementación del algoritmo de Held-Karp
def alg_HK(matriz_dist, ciudad_inicial):
    n = len(matriz_dist)
    # Tabla de memoización para almacenar la ruta más corta que visita cada subconjunto de nodos
    C = {}
    
    # Inicializar con la distancia desde el nodo inicial a cada nodo
    for k in range(n):
        if k != ciudad_inicial and matriz_dist[ciudad_inicial][k] != 0:  # only consider reachable nodes
            C[(1 << k, k)] = (matriz_dist[ciudad_inicial][k], ciudad_inicial)
    
    # Iterar sobre subconjuntos de longitud creciente
    for tam_subset in range(2, n):
        for subset in itertools.combinations(range(n), tam_subset):
            if ciudad_inicial in subset:
                continue
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            for k in subset:
                if k == ciudad_inicial:
                    continue
                prev_bits = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == ciudad_inicial or m == k or (prev_bits, m) not in C:
                        continue
                    if matriz_dist[m][k] != 0:  # Solo considerar nodos dentro de la ruta o alcanzables
                        res.append((C[(prev_bits, m)][0] + matriz_dist[m][k], m))
                if res:
                    C[(bits, k)] = min(res)
    
    # Encontrar ciclo más óptimo
    bits = (2**n - 1) & ~(1 << ciudad_inicial)
    res = []
    for k in range(n):
        if k == ciudad_inicial:
            continue
        if (bits, k) in C and matriz_dist[k][ciudad_inicial] != 0:  # Considerar solo nodos alcanzables
            res.append((C[(bits, k)][0] + matriz_dist[k][ciudad_inicial], k))
    if not res:
        return None, float('inf')
    opt, parent = min(res)
    
    # Reconstruír la ruta
    ruta = []
    bits = (2**n - 1) & ~(1 << ciudad_inicial)
    for i in range(n - 1):
        ruta.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits
    
    ruta.append(ciudad_inicial)
    ruta.reverse()
    
    return ruta, opt

# Especificar ciudad inicial (E)
ciudad_inicial = ciudades.index('E')

# Resolver problema del viajero
indices_ruta, min_distance = alg_HK(matriz_dist, ciudad_inicial)

if indices_ruta is None:
    print("No se pudo encontrar una ruta óptima")
else:
    # Convertir los índices a su respectiva ciudad
    ruta_ciudades = [ciudades[i] for i in indices_ruta]
    # Agregar la ciudad inicial para completar el circuito
    ruta_ciudades.append(ciudades[ciudad_inicial])

    # Imprimir el resultado
    print("Ruta más corta: ", " -> ".join(ruta_ciudades))
    print("Distancia total: ", min_distance)