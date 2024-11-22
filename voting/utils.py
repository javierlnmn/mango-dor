from .models import Category

def get_current_category_for_user(user):
    categories = Category.objects.all().order_by('name')
    current_category = None
    current_category_number = 0
    total_categories_number = categories.count()

    for index, category in enumerate(categories):
        if not category.user_category_voting_complete(user):
            current_category = category
            current_category_number = index + 1
            break

    return current_category, current_category_number, total_categories_number
