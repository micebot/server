from typing import List, Dict

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from server.db.repo import products as repo
from server.models import schemas
from server.models.oauth2 import auth

router = APIRouter()


@router.get(
    "/",
    summary="Get all the products.",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Product],
)
def get_products(
    skip: int = 0,
    limit: int = 50,
    taken: bool = False,
    db: Session = Depends(auth),
):
    if entities := repo.get_products(
        db=db, skip=skip, limit=limit, taken=taken
    ):
        return entities

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No products registered yet.",
    )


@router.post(
    "/",
    summary="Register a new product.",
    response_model=schemas.Product,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: schemas.ProductCreation, db: Session = Depends(auth)
):
    if repo.get_product_by_code(db=db, code=product.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The code is already in use by another product.",
        )

    return repo.create_product(db=db, product=product)


@router.put(
    "/{code}",
    summary="Updates an existing product.",
    response_model=schemas.Product,
    status_code=status.HTTP_200_OK,
)
def update_product(
    code: str, product: schemas.ProductUpdate, db: Session = Depends(auth)
):
    if db_product := repo.get_product_by_code(db=db, code=code):
        if repo.get_product_by_code(db=db, code=product.code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The code is already in use by another product.",
            )
        return repo.update_product(
            db=db, product=product, db_product=db_product
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No product found for the code specified.",
    )


@router.delete(
    "/{code}",
    summary="Delete a registed product.",
    response_model=Dict[str, bool],
    status_code=status.HTTP_200_OK,
)
def delete_product(code: str, db: Session = Depends(auth)):
    if product := repo.get_product_by_code(db=db, code=code):
        if product.taken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot delete products already taken.",
            )
        repo.delete_product(db=db, product=product)
        return {"deleted": True}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No product found for the code specified.",
    )
