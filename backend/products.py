from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db

router = APIRouter()


class Product(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    price: float
    stock: int = 0
    availability: bool = True


# GET ALL PRODUCTS
@router.get("/products")
def get_products(db: Session = Depends(get_db)):

    query = text("""
        SELECT
            id,
            name,
            description,
            category,
            price,
            stock,
            availability,
            created_at
        FROM products
    """)

    result = db.execute(query)

    products = [dict(row._mapping) for row in result]

    return {
        "products": products
    }


# GET ONE PRODUCT
@router.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            id,
            name,
            description,
            category,
            price,
            stock,
            availability,
            created_at
        FROM products
        WHERE id = :product_id
    """)

    result = db.execute(
        query,
        {"product_id": product_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return dict(result._mapping)


# ADD PRODUCT
@router.post("/products")
def add_product(
    product: Product,
    db: Session = Depends(get_db)
):

    query = text("""
        INSERT INTO products
        (
            name,
            description,
            category,
            price,
            stock,
            availability
        )
        VALUES
        (
            :name,
            :description,
            :category,
            :price,
            :stock,
            :availability
        )
    """)

    result = db.execute(
        query,
        {
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "stock": product.stock,
            "availability": product.availability
        }
    )

    db.commit()

    return {
        "message": "Product added successfully",
        "product_id": result.lastrowid
    }