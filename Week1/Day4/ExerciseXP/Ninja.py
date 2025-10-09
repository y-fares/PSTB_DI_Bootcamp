# Instructions
# These are the rules of the Game of Life (as stated in Wikipedia):

# The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead, (or populated and unpopulated, respectively).

# Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
# Using these rules, implement the Game. (Hint: use Classes !!!!)
# Use a few different initial states to see how the game ends.

# Notes:

# Display the grid after each generation
# The end of the game is fully determined by the initial state. So have it pass through your program and see how it ends.
# Be creative, but use classes
# The game can have fixed borders and can also have moving borders. First implement the fixed borders. Each “live” cell that is going out of the border, exits the game.
# Bonus: Make the game with ever expandable borders, make the maximum border size a very large number(10,000) so you won’t cause a memory overflow

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Iterable, Set, Tuple, Dict, List
import json
import time
import hashlib

Cell = Tuple[int, int]

# ---------- Règles ----------
def next_state(is_alive: bool, n_alive_neighbors: int) -> bool:
    """Applique les règles de Conway."""
    if is_alive and n_alive_neighbors < 2:
        return False          # sous-population
    if is_alive and n_alive_neighbors in (2, 3):
        return True           # survie
    if is_alive and n_alive_neighbors > 3:
        return False          # surpopulation
    if not is_alive and n_alive_neighbors == 3:
        return True           # reproduction
    return False

# ---------- Audit ----------
@dataclass
class GenerationAudit:
    gen: int
    births: int
    deaths: int
    alive: int

# ---------- Grille bornée ----------
@dataclass
class BoundedLife:
    rows: int
    cols: int
    alive: Set[Cell] = field(default_factory=set)
    audits: List[GenerationAudit] = field(default_factory=list)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int) -> Iterable[Cell]:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    yield (nr, nc)

    def step(self, gen: int = 0) -> None:
        next_alive: Set[Cell] = set()
        births = deaths = 0
        # Pour limiter les calculs, on ne regarde que cellules vivantes + leur voisinage
        to_check: Set[Cell] = set(self.alive)
        for (r, c) in list(self.alive):
            to_check.update(self.neighbors(r, c))

        for (r, c) in to_check:
            alive_now = (r, c) in self.alive
            n = sum((nr, nc) in self.alive for (nr, nc) in self.neighbors(r, c))
            alive_next = next_state(alive_now, n)
            if alive_next:
                next_alive.add((r, c))
                if not alive_now:
                    births += 1
            elif alive_now:
                deaths += 1

        self.alive = next_alive
        self.audits.append(GenerationAudit(gen, births, deaths, len(self.alive)))

    # Affichage texte simple
    def render(self) -> str:
        lines = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append("█" if (r, c) in self.alive else "·")
            lines.append("".join(row))
        return "\n".join(lines)

    # Sérialisation minimaliste
    def to_json(self) -> str:
        payload = {
            "rows": self.rows,
            "cols": self.cols,
            "alive": list(sorted(self.alive)),
        }
        return json.dumps(payload)

    @staticmethod
    def from_json(s: str) -> "BoundedLife":
        obj = json.loads(s)
        return BoundedLife(
            rows=obj["rows"],
            cols=obj["cols"],
            alive=set(tuple(x) for x in obj["alive"])
        )

# ---------- Grille sparse extensible ----------
@dataclass
class SparseLife:
    alive: Set[Cell] = field(default_factory=set)
    audits: List[GenerationAudit] = field(default_factory=list)
    limit: int = 5000  # => espace logique ~10000x10000 (de -limit à +limit)

    def step(self, gen: int = 0) -> None:
        if not self.alive:
            self.audits.append(GenerationAudit(gen, 0, 0, 0))
            return

        counts: Dict[Cell, int] = {}
        for (r, c) in self.alive:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nbr = (r + dr, c + dc)
                    # Limiter l’extension (anti-explosion mémoire)
                    if abs(nbr[0]) <= self.limit and abs(nbr[1]) <= self.limit:
                        counts[nbr] = counts.get(nbr, 0) + 1

        next_alive: Set[Cell] = set()
        births = deaths = 0

        to_check = set(counts.keys()) | set(self.alive)
        for cell in to_check:
            n = counts.get(cell, 0)
            alive_now = cell in self.alive
            alive_next = next_state(alive_now, n)
            if alive_next:
                next_alive.add(cell)
                if not alive_now:
                    births += 1
            elif alive_now:
                deaths += 1

        self.alive = next_alive
        self.audits.append(GenerationAudit(gen, births, deaths, len(self.alive)))

    def bounds(self) -> Tuple[int, int, int, int]:
        if not self.alive:
            return (0, 0, 0, 0)
        rs = [r for r, _ in self.alive]
        cs = [c for _, c in self.alive]
        return (min(rs), max(rs), min(cs), max(cs))

    def render(self, pad: int = 1, max_size: int = 40) -> str:
        """Rendu fenêtré autour du pattern (évite d’imprimer 10k×10k)."""
        if not self.alive:
            return "(empty)"
        rmin, rmax, cmin, cmax = self.bounds()
        rmin -= pad; rmax += pad; cmin -= pad; cmax += pad
        # Clamp pour rester lisible
        if rmax - rmin + 1 > max_size or cmax - cmin + 1 > max_size:
            # Fenêtrage centré
            rc = (rmin + rmax)//2
            cc = (cmin + cmax)//2
            half = max_size // 2
            rmin, rmax = rc - half, rc + half
            cmin, cmax = cc - half, cc + half

        lines = []
        for r in range(rmin, rmax + 1):
            row = []
            for c in range(cmin, cmax + 1):
                row.append("█" if (r, c) in self.alive else "·")
            lines.append("".join(row))
        return "\n".join(lines)

    def to_json(self) -> str:
        payload = {"alive": list(sorted(self.alive)), "limit": self.limit}
        return json.dumps(payload)

    @staticmethod
    def from_json(s: str) -> "SparseLife":
        obj = json.loads(s)
        return SparseLife(alive=set(tuple(x) for x in obj["alive"]), limit=obj.get("limit", 5000))

# ---------- Détection de fin ----------
class EndDetector:
    """
    Détecte:
      - état stable (répétition immédiate)
      - oscillation (répétition sur fenêtre d'historique)
    """
    def __init__(self, history: int = 200):
        self.seen: Dict[str, int] = {}
        self.history = history

    @staticmethod
    def _hash_state(alive: Set[Cell]) -> str:
        # Hash indépendant de l’ordre
        h = hashlib.blake2b(digest_size=16)
        for cell in sorted(alive):
            h.update(f"{cell[0]},{cell[1]};".encode())
        return h.hexdigest()

    def push(self, gen: int, alive: Set[Cell]) -> Tuple[bool, str]:
        key = self._hash_state(alive)
        if key in self.seen:
            prev = self.seen[key]
            period = gen - prev
            return True, ("stable" if period == 1 else f"oscillation (période {period})")
        self.seen[key] = gen
        # purge vieille histoire pour garder O(1) mémoire amorti
        if len(self.seen) > self.history:
            # enlève arbitrairement le plus ancien
            to_del = min(self.seen.items(), key=lambda kv: kv[1])[0]
            self.seen.pop(to_del, None)
        return False, ""

# ---------- Presets ----------
def preset_blinker(center=(5,5)) -> Set[Cell]:
    r, c = center
    return {(r, c-1), (r, c), (r, c+1)}

def preset_block(top_left=(2,2)) -> Set[Cell]:
    r, c = top_left
    return {(r, c), (r, c+1), (r+1, c), (r+1, c+1)}

def preset_glider(start=(0,0)) -> Set[Cell]:
    r, c = start
    return {(r, c+1), (r+1, c+2), (r+2, c), (r+2, c+1), (r+2, c+2)}

# ---------- Runner d'exemple ----------
def run_bounded_demo(rows=12, cols=20, steps=50, delay=0.05):
    game = BoundedLife(rows, cols, alive=preset_glider((1,1)) | preset_block((6,10)))
    end = EndDetector()
    for gen in range(steps):
        print(f"\nGénération {gen}")
        print(game.render())
        ended, reason = end.push(gen, game.alive)
        if ended:
            print(f"\nFin détectée: {reason}")
            break
        game.step(gen)
        time.sleep(delay)
    # Audit final
    print("\nAudit (dernières générations) :")
    for a in game.audits[-5:]:
        print(asdict(a))

def run_sparse_demo(steps=100, delay=0.05):
    game = SparseLife(alive=preset_glider((0,0)) | preset_blinker((10, 10)))
    end = EndDetector()
    for gen in range(steps):
        print(f"\nGénération {gen}")
        print(game.render())
        ended, reason = end.push(gen, game.alive)
        if ended:
            print(f"\nFin détectée: {reason}")
            break
        game.step(gen)
        time.sleep(delay)
    # Audit final
    print("\nAudit (dernières générations) :")
    for a in game.audits[-5:]:
        print(asdict(a))

if __name__ == "__main__":
    # Décommente l’un des deux pour tester rapidement :
    run_bounded_demo()
    #run_sparse_demo()
    pass
