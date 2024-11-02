from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Book, BookUpdate

# Création d'un routeur pour regrouper les routes liées aux livres
router = APIRouter()


@router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    # Encode le modèle `Book` en format JSON
    book = jsonable_encoder(book)
    
    # Insère le livre dans la collection "books" de la base de données
    new_book = request.app.database["books"].insert_one(book)
    
    # Récupère le livre créé en utilisant son identifiant
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book

@router.get("/", response_description="List all books", response_model=List[Book])
def list_books(request: Request):
    # Récupère tous les livres de la collection "books" avec une limite de 100
    books = list(request.app.database["books"].find(limit=100))
    return books



@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    # Cherche le livre correspondant à l'ID dans la base de données
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book
    
    # Lève une erreur si le livre n'est pas trouvé
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.put("/{id}", response_description="Update a book", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    # Filtre les champs non nuls du modèle de mise à jour `BookUpdate`
    book = {k: v for k, v in book.dict().items() if v is not None}
    
    # Si des champs sont fournis pour la mise à jour
    if len(book) >= 1:
        # Applique les mises à jour dans la base de données
        update_result = request.app.database["books"].update_one(
            {"_id": id}, {"$set": book}
        )

        # Si aucun livre n'est modifié, lève une erreur
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    # Récupère le livre mis à jour et le retourne
    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    # Lève une erreur si le livre n'est toujours pas trouvé
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    # Supprime le livre correspondant à l'ID
    delete_result = request.app.database["books"].delete_one({"_id": id})

    # Si le livre est supprimé avec succès, retourne un statut HTTP 204
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Si le livre n'est pas trouvé, lève une erreur 404
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")
