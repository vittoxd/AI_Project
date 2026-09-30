"""
Sistema de recomendación de películas basado en filtrado colaborativo.

Implementa dos enfoques:
  1. Filtrado colaborativo basado en usuarios (user-based):
     recomienda películas que gustaron a usuarios con gustos similares.
  2. Filtrado colaborativo basado en ítems (item-based):
     recomienda películas parecidas a las que el usuario ya valoró bien.

La similitud se calcula con la similitud del coseno sobre las
valoraciones (escala 1 a 5). No requiere librerías externas.
"""

from math import sqrt

# Valoraciones de ejemplo: usuario -> {película: puntuación (1-5)}
RATINGS = {
    "Ana": {
        "Matrix": 5, "Inception": 4, "Interstellar": 5,
        "Titanic": 1, "Toy Story": 2,
    },
    "Bruno": {
        "Matrix": 4, "Inception": 5, "Blade Runner": 5,
        "Titanic": 2, "Coco": 1,
    },
    "Carla": {
        "Titanic": 5, "Coco": 4, "Toy Story": 5,
        "Matrix": 1, "La La Land": 5,
    },
    "Diego": {
        "Interstellar": 4, "Blade Runner": 4, "Inception": 5,
        "Matrix": 5, "La La Land": 2,
    },
    "Elena": {
        "Coco": 5, "Toy Story": 4, "La La Land": 4,
        "Titanic": 4, "Inception": 2,
    },
    "Felipe": {
        "Matrix": 5, "Interstellar": 5, "Blade Runner": 4,
        "Coco": 2,
    },
}


def cosine_similarity(a: dict, b: dict) -> float:
    """Similitud del coseno entre dos vectores dispersos (dict clave -> valor).

    Las claves ausentes cuentan como 0, por lo que dos vectores con pocos
    elementos en común obtienen una similitud baja. Devuelve un valor
    entre -1 y 1.
    """
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[k] * b[k] for k in common)
    norm_a = sqrt(sum(v ** 2 for v in a.values()))
    norm_b = sqrt(sum(v ** 2 for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def mean_centered(ratings: dict) -> dict:
    """Resta la media del usuario a cada valoración.

    Así, una valoración baja aporta información negativa en lugar de
    sumar como si fuera un "me gusta" más débil.
    """
    mean = sum(ratings.values()) / len(ratings)
    return {item: score - mean for item, score in ratings.items()}


def transpose(ratings: dict) -> dict:
    """Convierte {usuario: {película: nota}} en {película: {usuario: nota}}."""
    items = {}
    for user, user_ratings in ratings.items():
        for item, score in user_ratings.items():
            items.setdefault(item, {})[user] = score
    return items


class RecommendationSystem:
    def __init__(self, ratings: dict):
        self.ratings = ratings
        self.centered = {u: mean_centered(r) for u, r in ratings.items()}
        self.item_ratings = transpose(self.centered)

    def similar_users(self, user: str, top_n: int = 3) -> list:
        """Devuelve los usuarios más parecidos a `user` con su similitud."""
        scores = [
            (other, cosine_similarity(self.centered[user], self.centered[other]))
            for other in self.ratings
            if other != user
        ]
        scores.sort(key=lambda pair: pair[1], reverse=True)
        return scores[:top_n]

    def recommend_user_based(self, user: str, top_n: int = 3) -> list:
        """Predice notas para películas no vistas usando usuarios similares."""
        seen = self.ratings[user]
        user_mean = sum(seen.values()) / len(seen)
        weighted, weights = {}, {}

        for other, sim in self.similar_users(user, top_n=len(self.ratings)):
            if sim <= 0:
                continue
            for item, deviation in self.centered[other].items():
                if item in seen:
                    continue
                weighted[item] = weighted.get(item, 0.0) + sim * deviation
                weights[item] = weights.get(item, 0.0) + sim

        predictions = [
            (item, user_mean + weighted[item] / weights[item])
            for item in weighted
        ]
        predictions.sort(key=lambda pair: pair[1], reverse=True)
        return [(item, round(min(5.0, max(1.0, p)), 2)) for item, p in predictions[:top_n]]

    def similar_items(self, item: str, top_n: int = 3) -> list:
        """Devuelve las películas más parecidas a `item`."""
        scores = [
            (other, cosine_similarity(self.item_ratings[item], self.item_ratings[other]))
            for other in self.item_ratings
            if other != item
        ]
        scores.sort(key=lambda pair: pair[1], reverse=True)
        return scores[:top_n]

    def recommend_item_based(self, user: str, top_n: int = 3) -> list:
        """Predice notas para películas no vistas según su parecido con las ya valoradas."""
        seen = self.centered[user]
        user_mean = sum(self.ratings[user].values()) / len(self.ratings[user])
        scores = {}
        for item in self.item_ratings:
            if item in seen:
                continue
            total, norm = 0.0, 0.0
            for seen_item, deviation in seen.items():
                sim = cosine_similarity(self.item_ratings[item], self.item_ratings[seen_item])
                if sim > 0:
                    total += sim * deviation
                    norm += sim
            if norm > 0:
                scores[item] = user_mean + total / norm
        ranking = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
        return [(item, round(min(5.0, max(1.0, s)), 2)) for item, s in ranking[:top_n]]


def main():
    system = RecommendationSystem(RATINGS)

    for user in RATINGS:
        print(f"=== {user} ===")
        neighbors = ", ".join(f"{u} ({s:.2f})" for u, s in system.similar_users(user, 2))
        print(f"  Usuarios similares: {neighbors}")

        user_recs = system.recommend_user_based(user)
        print("  Recomendación (usuarios):", user_recs or "sin recomendaciones")

        item_recs = system.recommend_item_based(user)
        print("  Recomendación (ítems):   ", item_recs or "sin recomendaciones")
        print()

    print("=== Películas parecidas a 'Matrix' ===")
    for item, sim in system.similar_items("Matrix"):
        print(f"  {item}: {sim:.2f}")


if __name__ == "__main__":
    main()
