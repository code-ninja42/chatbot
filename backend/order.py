from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db

router = APIRouter()


class Order(BaseModel):
    customer_name: str
    customer_email: str | None = None
    product_id: int
    quantity: int


# PLACE ORDER
@router.post("/orders")
def create_order(
    order: Order,
    db: Session = Depends(get_db)
):

    # Check product
    query = text("""
        SELECT
            id,
            name,
            price,
            stock,
            availability
        FROM products
        WHERE id = :product_id
    """)

    product = db.execute(
        query,
        {"product_id": order.product_id}
    ).fetchone()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Check quantity
    if order.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # Check availability
    if not product.availability:
        raise HTTPException(
            status_code=400,
            detail="Product is not available"
        )

    # Check stock
    if product.stock < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    # Calculate total
    total_amount = float(product.price) * order.quantity

    # Create order
    query = text("""
        INSERT INTO orders
        (
            customer_name,
            customer_email,
            product_id,
            quantity,
            total_amount,
            order_date,
            status,
            tracking_number
        )
        VALUES
        (
            :customer_name,
            :customer_email,
            :product_id,
            :quantity,
            :total_amount,
            CURDATE(),
            'Pending',
            NULL
        )
    """)

    result = db.execute(
        query,
        {
            "customer_name": order.customer_name,
            "customer_email": order.customer_email,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total_amount": total_amount
        }
    )

    # Reduce product stock
    query = text("""
        UPDATE products
        SET stock = stock - :quantity
        WHERE id = :product_id
    """)

    db.execute(
        query,
        {
            "quantity": order.quantity,
            "product_id": order.product_id
        }
    )

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": result.lastrowid,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_amount": total_amount,
        "status": "Pending"
    }


# GET ALL ORDERS
@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):

    query = text("""
        SELECT
            id,
            customer_name,
            customer_email,
            product_id,
            quantity,
            total_amount,
            order_date,
            status,
            tracking_number
        FROM orders
        ORDER BY id DESC
    """)

    result = db.execute(query)

    orders = [dict(row._mapping) for row in result]

    return {
        "orders": orders
    }


# GET ONE ORDER
@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            id,
            customer_name,
            customer_email,
            product_id,
            quantity,
            total_amount,
            order_date,
            status,
            tracking_number
        FROM orders
        WHERE id = :order_id
    """)

    result = db.execute(
        query,
        {"order_id": order_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return dict(result._mapping)