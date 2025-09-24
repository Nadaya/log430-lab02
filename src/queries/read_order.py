"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order
from models.user import User
from collections import defaultdict

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
    # TODO: écrivez la méthode --> FAIT 
    r = get_redis_conn()   
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
    # TODO: écrivez la méthode --> FAIT
    # triez le résultat par nombre de commandes (ordre décroissant)
    session = get_sqlalchemy_session()
    orders = session.query(Order).all()

    expenses_by_user = defaultdict(float)
    for order in orders:
        expenses_by_user[order.user_id] += order.total_amount
    highest_spending_users = sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)

    # on récupère les noms 
    result = []
    for user_id in highest_spending_users:
        user = session.query(User).filter_by(id=user_id[0]).first()
        result.append({'name': user.name})
    return result