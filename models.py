import uuid
from typing import Optional
from pydantic import BaseModel, Field

# Définition du modèle de données pour un livre
class Book(BaseModel):
    # Génère un identifiant unique (UUID) pour chaque instance de livre par défaut
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    
    # Champ obligatoire pour le titre du livre
    title: str = Field(...)
    
    # Champ obligatoire pour l'auteur du livre
    author: str = Field(...)
    
    # Champ obligatoire pour le synopsis du livre
    synopsis: str = Field(...)

    # Configuration interne du modèle pour Pydantic
    class Config:
        # Permet d'utiliser des noms de champs alias lors de la création d'instances
        allow_population_by_field_name = True
        
        # Exemple de structure JSON pour aider à la documentation et aux tests
        schema_extra = {
            "example": {
                "_id": "0066de609-b04a-4b30-b46c-32537cf1f6e",  # Exemple d'UUID pour l'identifiant
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "..."
            }
        }

# Définition d'un modèle de mise à jour pour le livre, avec des champs optionnels
class BookUpdate(BaseModel):
    # Titre optionnel, utilisé uniquement si une mise à jour du titre est nécessaire
    title: Optional[str]
    
    # Auteur optionnel
    author: Optional[str]
    
    # Synopsis optionnel
    synopsis: Optional[str]

    # Configuration interne du modèle de mise à jour
    class Config:
        # Exemple de structure JSON pour une mise à jour, utile pour la documentation et les tests
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }
