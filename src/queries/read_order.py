"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    # TODO: écrivez la méthode
    r = get_redis_conn()    # récupère la connexion Redis
    keys = r.keys(f"order:*")
    if not keys:
        return []

    # on extrait les IDs et on trie par ordre décroissant
    order_ids = []
    for key in keys:
        try:
            order_id = int(key.decode().split(":")[1])
            order_ids.append(order_id)
        except Exception as e:
            continue

    order_ids = sorted(order_ids, reverse=True)[:limit]
    order_ids = [f'order:{oid}' for oid in order_ids]

    # on récupère les données des commandes
    orders = []
    for order_key in order_ids:
        order_data = r.hgetall(order_key)
        if order_data:
            order = {k.decode(): v.decode() for k, v in order_data.items()}
            order['id'] = int(order_key.decode().split(":")[1])
            order['user_id'] = int(order['user_id'])
            order['total_amount'] = float(order['total_amount'])
            orders.append(order)
        
    return orders

def get_highest_spending_users():
    """Get report of best selling products"""
    # TODO: écrivez la méthode
    # triez le résultat par nombre de commandes (ordre décroissant)
    return []