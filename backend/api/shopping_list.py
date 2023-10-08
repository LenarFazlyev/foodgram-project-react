from datetime import datetime


def create_shopping_list(ingredients):
    today = datetime.today()
    shopping_list = f'Ваш список покупок на: {today:%Y-%m-%d}\n\n'
    shopping_list += '\n'.join(
        [
            f'- {ingredient["name"]} '
            f'({ingredient["measurement_unit"]})'
            f' - {ingredient["cart_amount"]}'
            for ingredient in ingredients
        ]
    )
    return shopping_list
