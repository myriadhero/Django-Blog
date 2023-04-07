from django.utils.text import slugify
from ..models import Category, CategoryTag, Post
from .celeb_list import celeb_list

CATEGORIES = [
    ("Celebrities", 0, False, True, True),
    ("C-Drama", 1, True, True, False),
    ("C-Variety", 2, True, True, False),
    ("C-Pop", 3, True, True, False),
    ("C-Ent", 4, True, True, False),
]

CDRAMAS = [
    "Love Between Fairy And Devil",
    "My Journey To You",
    "Nothing But You",
    "One And Only",
    "Only For Love",
    "Road Home",
    "Stories Of Youth And Love / 199爱",
    "Story of Kunning Palace",
    "The Starry Love",
    "Till The End Of The Moon",
]

CVARS = [
    "Before Sunrise",
    "Go Fridge",
    "Hello Saturday",
    "Keep Running",
    "Memories Beyond Horizon",
    "Story of Kunning Palace Variety",
    "Super Team",
    "Welcome Back To Sound",
    "Zhan Kai Shuo Shuo (展开说说)",
]

CENTS = ["Weibo Night 2022"]


def create_tag(name, category):
    if CategoryTag.objects.filter(name=name).exists():
        return
    tag = CategoryTag(name=name, slug=slugify(name))
    tag.save()
    tag.categories.add(category)
    tag.save()


def create_categories():
    for name, order, front_page, in_menu, is_list in CATEGORIES:
        Category(
            name=name,
            slug=slugify(name),
            order=order,
            show_on_front_page=front_page,
            show_in_menu=in_menu,
            is_tag_list=is_list,
        ).save()


def create_all_tags():
    cat = Category.objects.filter(name="Celebrities").first()
    for celeb in set(celeb_list):
        create_tag(celeb, cat)

    cat = Category.objects.filter(name="C-Drama").first()
    for drama in CDRAMAS:
        create_tag(drama, cat)

    cat = Category.objects.filter(name="C-Variety").first()
    for variety in CVARS:
        create_tag(variety, cat)

    cat = Category.objects.filter(name="C-Ent").first()
    for entert in CENTS:
        create_tag(entert, cat)
