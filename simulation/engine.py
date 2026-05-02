import numpy as np

# Estados de las celdas
EMPTY = 0
TREE = 1
FIRE = 2


def create_grid(size):
    """Crea una cuadrícula vacía de tamaño size x size."""
    return np.zeros((size, size), dtype=np.int8)


def step(grid, p, f):
    """
    Avanza la simulación un paso aplicando las reglas de Drossel-Schwabl.
    
    Reglas:
    - Celda vacía -> árbol con probabilidad p
    - Árbol vecino de fuego -> se incendia
    - Árbol sin vecinos en llamas -> se incendia por rayo con probabilidad f
    - Celda en llamas -> vacía
    
    Retorna la nueva cuadrícula y el tamaño del incendio ocurrido en este paso.
    """
    size = grid.shape[0]
    new_grid = grid.copy()

    # Detectar qué árboles tienen vecinos en llamas
    fire_neighbor = np.zeros((size, size), dtype=bool)
    fire_positions = np.argwhere(grid == FIRE)
    for r, c in fire_positions:
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                if grid[nr, nc] == TREE:
                    fire_neighbor[nr, nc] = True

    # Aplicar reglas
    random_p = np.random.random((size, size))
    random_f = np.random.random((size, size))

    # Vacía -> árbol con prob p
    new_grid[(grid == EMPTY) & (random_p < p)] = TREE

    # Árbol con vecino en llamas -> fuego
    new_grid[(grid == TREE) & fire_neighbor] = FIRE

    # Árbol sin vecino en llamas -> rayo con prob f
    new_grid[(grid == TREE) & ~fire_neighbor & (random_f < f)] = FIRE

    # Fuego -> vacío
    new_grid[grid == FIRE] = EMPTY

    # Contar árboles quemados en este paso
    fire_size = int(np.sum((grid == TREE) & fire_neighbor) + 
                    np.sum((grid == TREE) & ~fire_neighbor & (random_f < f)))

    return new_grid, fire_size


def get_stats(grid):
    """Retorna estadísticas básicas de la cuadrícula."""
    size = grid.shape[0]
    total = size * size
    tree_density = float(np.sum(grid == TREE) / total)
    return {
        "tree_density": round(tree_density, 4),
        "tree_count": int(np.sum(grid == TREE)),
        "fire_count": int(np.sum(grid == FIRE)),
        "empty_count": int(np.sum(grid == EMPTY)),
    }