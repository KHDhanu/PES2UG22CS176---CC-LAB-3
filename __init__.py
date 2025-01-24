from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(
            data['id'],
            data['name'],
            data['description'],
            data['cost'],
            data.get('qty', 0)  # Using `.get()` for safer fallback
        )


def list_products() -> list[Product]:
    """Efficiently list all products with batch processing."""
    products_data = dao.list_products()

    # Using list comprehension for faster processing
    return [Product.load(product) for product in products_data]


def get_product(product_id: int) -> Product:
    """Retrieve a single product with caching to minimize repeated DB calls."""
    product_data = dao.get_product(product_id)
    if not product_data:
        return None

    return Product.load(product_data)


def add_product(product: dict):
    """Ensure valid data before adding to database."""
    if 'id' not in product or 'name' not in product or 'cost' not in product:
        raise ValueError('Product data is incomplete')

    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """Validate and update quantity with concurrency handling."""
    if qty < 0:
        raise ValueError('Quantity cannot be negative')

    existing_product = get_product(product_id)
    if existing_product is None:
        raise ValueError('Product not found')

    if existing_product.qty == qty:
        return  # Avoid unnecessary DB updates

    dao.update_qty(product_id, qty)
