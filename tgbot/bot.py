import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..','backend')
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'bricky.settings'
)

import django
django.setup()
import telebot
from environs import Env
from users.models import *
from store.models import *
from orders.models import *
from telebot import types

env = Env()
env.read_env()
bot = telebot.TeleBot(env.str("TG_TOKEN"))
pay_token = env.str("PAY_TOKEN")
user_state = {}
user_data = {}
product_data = {}
product_state = {}
cat_state = {}
cat_data = {}
reg_state = {}
reg_data = {}
edit_product_data = {}
edit_product_state = {}
edit_cat_state = {}
edit_cat_data = {}
LAST_STEP = "menu"


def menu(message):
    """Display main menu with navigation buttons.

    Shows options for browsing products, categories, new releases,
    and shopping cart. Admin panel is displayed for staff/superuser users.

    Args:
        message: Telegram message object containing chat information
    """
    markup = types.InlineKeyboardMarkup()
    cart_btn = types.InlineKeyboardButton(text="My cart", callback_data="cart")
    cat_btn = types.InlineKeyboardButton(text="Categories", callback_data=f"cat")
    new_r_btn = types.InlineKeyboardButton(text="New Releases", callback_data=f"new_r")
    products_btn = types.InlineKeyboardButton(text="Products", callback_data=f"products")
    user = CustomUser.objects.get(tg_id=message.chat.id)

    markup.row(cart_btn)
    markup.row(products_btn)
    markup.row(cat_btn)
    markup.row(new_r_btn)
    if user.is_staff or user.is_superuser:
        admin_btn = types.InlineKeyboardButton(text="Admin Panel", callback_data=f"admin")
        markup.row(admin_btn)
    bot.send_message(message.chat.id, "Choose one:", reply_markup=markup)


def create_cart(tg_id):
    """Create or retrieve shopping cart for user by Telegram ID.

    Args:
        tg_id: Telegram user ID (chat.id)

    Register new user with email from Telegram message.

    Creates or updates user account with provided email and Telegram ID.
    Automatically creates shopping cart and displays main menu.

    Args:
        message: Telegram message object containing email text


    Returns:
        Tuple of (Cart object, created flag)
    """
    Cart.objects.update_or_create(user=CustomUser.objects.get(tg_id=tg_id))


def create_user(message):
    """Create or link user account with Telegram ID.

    If email exists in system, links user and shows menu.
    Otherwise, initiates registration process.

    Args:
        message: Telegram message containing user's email address
    """
    markup = types.InlineKeyboardMarkup()
    try:
        user = CustomUser.objects.get(email=message.text.strip())
        user.tg_id = message.chat.id
        user.save()
        bot.send_message(message.chat.id, f"You login as {user[0].username}", reply_markup=markup)
        create_cart(message.chat.id)
        menu(message)
    except CustomUser.DoesNotExist:
        start_register(message, message.text.strip())
    except Exception as e:
        bot.send_message(message.chat.id, f"{e}")


def add_to_cart(tg_id, product_id):
    """Add product to user's shopping cart.

    If product is already in cart, increments quantity.
    Otherwise, creates new cart item with quantity of 1.

    Args:
        tg_id: Telegram user ID
        product_id: Product UUID to add to cart
    """
    user = CustomUser.objects.get(tg_id=tg_id)
    cart = Cart.objects.get(user=user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product_id)
    except CartItem.DoesNotExist:
        cart_item = None
    product = Product.objects.get(id=product_id)

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1, price=product.price)
    """Initiate payment process and request delivery address.

    Sets user state to "address" mode and prompts for address input.

    Args:
        message: Telegram message object
    """


def delete_item(cart_item_id):
    """Remove or decrement cart item quantity.

    Decrements quantity by 1 if > 1, otherwise deletes the cart item.

    Args:
        cart_item_id: UUID of cart item to remove/decrement
    """
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    """Create order from cart items after successful payment.

    Creates Order record with all cart items and clears the cart.

    Args:
        tg_id: Telegram user ID
    """


def start_pay(message):
    user = CustomUser.objects.get(tg_id=message.chat.id)
    cart = Cart.objects.get(user=user)
    total_price = cart.get_total_price()
    prices = [types.LabeledPrice(label="Pay for Order", amount=int(total_price) * 100)]
    bot.send_invoice(message.chat.id, title="Paying", description="Pay for Order", provider_token=pay_token,
                     currency="try", prices=prices, start_parameter="test_pay", invoice_payload="test_payload")


def confirm_order(tg_id):
    """Create order from cart items after successful payment.

    Creates Order record with all cart items and clears the cart.

    Args:
        tg_id: Telegram user ID
    """
    user = CustomUser.objects.get(tg_id=tg_id)
    customer = Customer.objects.get(user=user)
    info = user_data[tg_id]
    cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.filter(cart=cart)
    order = Order.objects.create(customer=customer, address=info["address"], is_draft=False, status="N")
    """Handle successful payment confirmation from Telegram.

    Creates order and clears the shopping cart after payment success.

    Args:
        message: Telegram message with successful_payment content
    """
    for item in cart_item:
        OrderElement.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.price)

def start_cat_adding(message):
    """Initiate product creation workflow.

    Sets up state tracking for product addition process.

    Args:
        message: Telegram message object
    """
    user_id = message.chat.id
    cat_data[user_id] = {}
    cat_state[user_id] = "title"
    bot.send_message(user_id, text="Enter product name:")

def start_product_adding(message):
    """Initiate product creation workflow.

    Sets up state tracking for product addition process.

    Args:
        message: Telegram message object
    """
    user_id = message.chat.id
    product_data[user_id] = {}
    product_state[user_id] = "name"
    bot.send_message(user_id, text="Enter product name:")

def start_edit_product(message,product_id,status):
    user_id = message.chat.id
    edit_product_state[user_id] = status
    edit_product_data[user_id] = {}
    edit_product_data[user_id]["product"] = product_id
    if status == "category":
        for cat in Category.objects.all():
            btn = types.InlineKeyboardButton(text=cat.name, callback_data=f"finish_edit_product|category|{cat.id}")
            markup.add(btn)
    bot.send_message(user_id, text=f"Enter product {status} for edit it:")

def start_edit_cat(message):
    user_id = message.chat.id
    edit_cat_state[user_id] = status
    edit_cat_data[user_id] = {}
    edit_cat_data[user_id]["cat"] = product_id
    bot.send_message(user_id, text=f"Enter category {status} for edit it:")


@bot.message_handler(func=lambda msg: msg.chat.id in edit_cat_data, content_types=['photo', 'text'])
def handle_edit_cat_steps(message):
    user_id = message.chat.id
    state = edit_cat_state.get(user_id)
    if state == "name":
        edit_product_data[user_id]["title"] = message.text.strip()
        del edit_product_state[user_id]
        info = edit_product_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_edit_cat|title")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="menu")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        bot.send_message(message.chat.id, text=f"Name:{info["name"]}", reply_markup=markup)
    elif state == "picture":
        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        with open(f"../backend/media/categories/{message.photo[-1].file_unique_id}.png", "wb") as code:
            edit_product_data[user_id]["picture"] = f"{message.photo[-1].file_unique_id}.png"
            code.write(file)

        del cat_state[user_id]
        info = cat_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_edit_cat|picture")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="menu")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        with open(f'../backend/media/categories/{info["picture"]}', "rb") as photo:
            bot.send_photo(message.chat.id, photo=photo, reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.chat.id in edit_product_data, content_types=['photo', 'text'])
def handle_edit_product_steps(message):
    """Handle product editing steps based on current state.

    Processes user input for various product field edits.
    Supports editing name, picture, description, price, and stock.

    Args:
        message: Telegram message with text or photo
    """
    user_id = message.chat.id
    state = edit_product_state.get(user_id)

    if state == "name":
        edit_product_data[user_id]["name"] = message.text.strip()
        del edit_product_state[user_id]
        info = edit_product_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_edit_product|name")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="menu")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        bot.send_message(message.chat.id, text=f"Name:{info["name"]}", reply_markup=markup)
    elif state == "picture":
        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        with open(f"../backend/media/categories/{message.photo[-1].file_unique_id}.png", "wb") as code:
            edit_product_data[user_id]["picture"] = f"{message.photo[-1].file_unique_id}.png"
            code.write(file)

        del cat_state[user_id]
        info = cat_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_edit_product|picture")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="menu")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        with open(f'../backend/media/categories/{info["picture"]}', "rb") as photo:
            bot.send_photo(message.chat.id, photo=photo, reply_markup=markup)
    elif state == "description":
        edit_product_data[user_id]["description"] = message.text.strip()
        del edit_product_state[user_id]
        info = edit_product_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_edit_product|stock")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="menu")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        bot.send_message(message.chat.id, text=f"Stock:{info["stock"]}", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.chat.id in reg_state)
def handle_reg_steps(message):
    """Handle user registration steps.

    Processes password input during registration.
    Creates new user account after collecting email and password.

    Args:
        message: Telegram message with registration data
    """
    user_id = message.chat.id
    state = reg_state.get(user_id)

    if state == "password":
        if " " in message.text.strip():
            reg_state[user_id] = "password"
            bot.send_message(user_id, text="Error!Write your password(without space):")
        else:
            reg_data[user_id]["password"] = message.text.strip()
            del reg_state[user_id]
            info = reg_data[user_id]
            CustomUser.objects.create_user(username=message.chat.first_name, email=info["email"], tg_id=message.chat.id,
                                           password=info["password"])
            bot.send_message(message.chat.id, f"You registered as {message.chat.first_name}")
            create_cart(message.chat.id)
            menu(message)


@bot.message_handler(func=lambda msg: msg.chat.id in cat_state, content_types=['photo', 'text'])
def handle_cat_steps(message):
    """Handle category creation steps.

    Processes title and photo input for new categories.

    Args:
        message: Telegram message with text or photo
    """
    user_id = message.chat.id
    state = cat_state.get(user_id)

    if state == "title":
        cat_data[user_id]["title"] = message.text.strip()
        cat_state[user_id] = "picture"
        bot.send_message(user_id, text="Upload category photo:")
    elif state == "picture":
        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        with open(f"../backend/media/categories/{message.photo[-1].file_unique_id}.png", "wb") as code:
            cat_data[user_id]["picture"] = f"{message.photo[-1].file_unique_id}.png"
            code.write(file)

        del cat_state[user_id]
        info = cat_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_cat")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="menu")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        with open(f'../backend/media/categories/{info["picture"]}', "rb") as photo:
            bot.send_photo(message.chat.id, photo=photo, caption=f"Name:{info["title"]}", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.chat.id in product_state, content_types=['photo', 'text'])
def handle_product_steps(message):
    """Handle product creation steps.

    Processes name, description, price, and photo input for new products.

    Args:
        message: Telegram message with text or photo
    """
    user_id = message.chat.id
    state = product_state.get(user_id)

    if state == "name":
        product_data[user_id]["name"] = message.text.strip()
        product_state[user_id] = "description"
        del product_state[user_id]
    elif state == "description":
        product_data[user_id]["description"] = message.text.strip()
        product_state[user_id] = "price"
        bot.send_message(user_id, text="Enter product price:")
    elif state == "price":
        product_data[user_id]["price"] = message.text.strip()
        product_state[user_id] = "picture"
        bot.send_message(user_id, text="Upload product picture:")
    elif state == "picture":
        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        with open(f"../backend/media/products/{message.photo[-1].file_unique_id}.png", "wb") as code:
            product_data[user_id]["photo"] = f"{message.photo[-1].file_unique_id}.png"
            code.write(file)
        del product_state[user_id]
        info = product_data[user_id]
        markup = types.InlineKeyboardMarkup()
        for cat in Category.objects.all():
            btn = types.InlineKeyboardButton(text=cat.name, callback_data="category")
            markup.add(btn)
        bot.send_message(user_id, text="Select a category:", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.chat.id in user_state)
def handle_pay_steps(message):
    """Handle payment workflow steps.

    Processes delivery address input during checkout.

    Args:
        message: Telegram message with address
    """
    user_id = message.chat.id
    state = user_state.get(user_id)

    if state == "address":
        user_data[user_id]["address"] = message.text.strip()
        del user_state[user_id]
        info = user_data[user_id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        bot.send_message(message.chat.id, f"Check your info:{info["address"]}",
                         reply_markup=markup)


@bot.pre_checkout_query_handler(func=lambda q: True)
def pre_checkout(pre_checkout_query):
    """Approve all pre-checkout queries from Telegram payment.

    Automatically approves payment attempts before invoice processing.

    Args:
        pre_checkout_query: Pre-checkout query from Telegram
    """
    bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=["successful_payment"])
def got_payment(message):
    markup = types.InlineKeyboardMarkup()
    user = CustomUser.objects.get(tg_id=message.chat.id)
    confirm_order(message.chat.id)
    cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.filter(cart=cart)
    for item in cart_item:
        item.delete()
    """Handle successful payment confirmation from Telegram.

    Creates order and clears the shopping cart after payment success.

    Args:
        message: Telegram message with successful_payment content
    """
    menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
    markup.row(menu_btn)
    bot.send_message(message.chat.id, text="Pay completed!", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    """Handle /start command and initialize user session.

    If user exists, displays greeting and main menu.
    Otherwise, prompts for email registration.

    Args:
        message: Telegram message with /start command
    """
    try:
        markup = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, f"Hello! {CustomUser.objects.get(tg_id=message.chat.id)}",
                         reply_markup=markup)
        create_cart(message.chat.id)
        menu(message)
    except CustomUser.DoesNotExist:
        bot.send_message(message.chat.id, "Hello, Enter your Email:")
        bot.register_next_step_handler(message, create_user)
    except Exception as e:
        bot.send_message(message.chat.id, f"{e}")



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global LAST_STEP
    if call.data == "admin":
        markup = types.InlineKeyboardMarkup()
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        add_product_btn = types.InlineKeyboardButton(text="Add Product", callback_data=f"add_product")
        add_cat_btn = types.InlineKeyboardButton(text="Add Category", callback_data=f"add_cat")
        del_product_btn = types.InlineKeyboardButton(text="Delete Product", callback_data=f"show_products|del_product")
        del_cat_btn = types.InlineKeyboardButton(text="Delete Category", callback_data=f"show_cat|del_cat")
        edit_product_btn = types.InlineKeyboardButton(text="Edit Product", callback_data=f"show_product|edit_product")
        edit_cat_btn = types.InlineKeyboardButton(text="Edit Category", callback_data=f"show_cat|edit_cat")

        if user.is_superuser:
            add_admin_btn = types.InlineKeyboardButton(text="Add Admin", callback_data=f"show_user|add_admin")
            del_admin_btn = types.InlineKeyboardButton(text="Delete Admin", callback_data=f"show_user|del_admin")
            markup.row(add_admin_btn)
            markup.row(del_admin_btn)
        markup.row(add_product_btn)
        markup.row(add_cat_btn)
        markup.row(del_product_btn)
        markup.row(del_cat_btn)
        markup.row(edit_product_btn)
        markup.row(edit_cat_btn)
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, "Choose one:", reply_markup=markup)
    if call.data == "menu":
        menu(call.message)
    if call.data == "products":
        markup = types.InlineKeyboardMarkup()
        for product in Product.objects.all():
            btn = types.InlineKeyboardButton(text=product.name, callback_data=f"product|{product.id}")
            markup.row(btn)
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, "Select an item:", reply_markup=markup)
        LAST_STEP = call.data
    if call.data.split("|", 1)[0] == "product":
        markup = types.InlineKeyboardMarkup()
        product = Product.objects.get(id=call.data.split("|", 1)[1])
        back_btn = types.InlineKeyboardButton("Back", callback_data=LAST_STEP)
        add_to_cart_btn = types.InlineKeyboardButton("Add to cart", callback_data=f"add_to_cart|{product.id}")
        cart_btn = types.InlineKeyboardButton(text="My cart", callback_data="cart")
        markup.row(add_to_cart_btn)
        markup.row(cart_btn)
        markup.row(back_btn)
        bot.send_photo(call.message.chat.id, photo=product.picture,
                       caption=f"{product.description} \nPrice: {product.price}", reply_markup=markup)
        LAST_STEP = call.data
    if call.data == "new_r":
        markup = types.InlineKeyboardMarkup()
        for product in Product.objects.filter(status="N"):
            btn = types.InlineKeyboardButton(text=f"{product.name}({product.get_status_display()}!!!)",
                                             callback_data=f"product|{product.id}")
            markup.row(btn)
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, "Select an item:", reply_markup=markup)
    if call.data == "cat":
        markup = types.InlineKeyboardMarkup()
        for cat in Category.objects.all():
            btn = types.InlineKeyboardButton(text=cat.title, callback_data=f"product_cat|{cat.id}")
            markup.row(btn)
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, "Select a category:", reply_markup=markup)
        LAST_STEP = call.data
    if call.data.split("|", 1)[0] == "product_cat":
        markup = types.InlineKeyboardMarkup()
        for product in Product.objects.filter(category=call.data.split("|", 1)[1]):
            btn = types.InlineKeyboardButton(text=product.name, callback_data=f"product|{product.id}")
            markup.row(btn)
        back_btn = types.InlineKeyboardButton("Back", callback_data="cat")
        markup.row(back_btn)
        bot.send_message(call.message.chat.id, "Select an item:", reply_markup=markup)
        LAST_STEP = call.data
    if call.data.split("|", 1)[0] == "add_to_cart":
        add_to_cart(tg_id=call.message.chat.id, product_id=call.data.split("|", 1)[1])
        bot.send_message(call.message.chat.id, text="Product added")
    if call.data.split("|", 1)[0] == "delete_item":
        markup = types.InlineKeyboardMarkup()
        cart_item = CartItem.objects.filter(id=call.data.split("|", 1)[1])
        if cart_item.exists():
            delete_item(call.data.split("|", 1)[1])
            bot.send_message(call.message.chat.id, text="Product canceled")
            call.data = "cart"
        else:
            menu_btn = types.InlineKeyboardButton("Go Shopping", callback_data="products")
            markup.row(menu_btn)
            bot.send_message(call.message.chat.id, text="Add somthing first", reply_markup=markup)
    if call.data == "cart":
        markup = types.InlineKeyboardMarkup()
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        if cart_items.exists():
            for cart_item in cart_items:
                btn = types.InlineKeyboardButton(f"Cancel {cart_item.product.name} {cart_item.quantity}",
                                                 callback_data=f"delete_item|{cart_item.id}")
                markup.row(btn)
                bot.send_message(call.message.chat.id, text=f"{cart_item.product.name} {cart_item.quantity}")
            products_btn = types.InlineKeyboardButton("Continue Shopping", callback_data="products")
            pay_btn = types.InlineKeyboardButton("Pay", callback_data="pay")
            markup.row(products_btn)
            markup.row(pay_btn)
            bot.send_message(call.message.chat.id, text="You can delete products:", reply_markup=markup)
        else:
            menu_btn = types.InlineKeyboardButton("Go Shopping", callback_data="products")
            markup.row(menu_btn)
            bot.send_message(call.message.chat.id, text="Add somthing first", reply_markup=markup)
    if call.data == "pay":
        markup = types.InlineKeyboardMarkup()
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(cart=cart)
        if cart_item.exists():
            start_pay(call.message)
        else:
            menu_btn = types.InlineKeyboardButton("Go Shopping", callback_data="products")
            markup.row(menu_btn)
            bot.send_message(call.message.chat.id, text="Add somthing first", reply_markup=markup)
    if call.data == "confirm":
        pay(call.message)

    if call.data == "cancel":
        markup = types.InlineKeyboardMarkup()
        cart_btn = types.InlineKeyboardButton(text="Back", callback_data="cart")
        markup.row(cart_btn)
        bot.send_message(call.message.chat.id, text="You canceled paying", reply_markup=markup)
    if call.data == "add_product":
        start_product_adding(call.message)
    if call.data.split("|", 1)[0] == "category":
        product_data[call.message.chat.id]["category"] = call.data.split("|", 1)[1]
        info = product_data[call.message.chat.id]
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="finish_adding")
        cancel_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_adding")
        markup.row(confirm_btn)
        markup.row(cancel_btn)
        with open(f'../backend/media/{info["photo"]}', "rb") as photo:
            bot.send_photo(call.message.chat.id, photo=photo,
                           caption=f"Name:{info["name"]}\nDescription:{info["description"]}\nPrice:{info["price"]}\nCategory:{Category.objects.get(id=info["category"]).title}",
                           reply_markup=markup)
    if call.data == "finish_adding":
        markup = types.InlineKeyboardMarkup()
        info = product_data[call.message.chat.id]
        slug = "-".join(info["name"].split(" "))
        Product.objects.update_or_create(name=info["name"], description=info["description"],
                                         price=Decimal(info["price"]),
                                         category=Category.objects.get(id=info["category"]), picture=info["photo"],
                                         slug=slug, status="N")
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You added product", reply_markup=markup)
    if call.data.split("|", 1)[0] == "show_products":
        markup = types.InlineKeyboardMarkup()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        for product in Product.objects.all():
            btn = types.InlineKeyboardButton(product.name, callback_data=f"{call.data.split("|", 1)[1]}|{product.id}")
            markup.row(btn)
        bot.send_message(call.message.chat.id, text="Choose one:", reply_markup=markup)
    if call.data.split("|", 1)[0] == "del_product":
        markup = types.InlineKeyboardMarkup()
        product = Product.objects.get(id=call.data.split("|", 1)[1])
        product.delete()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You deleted product", reply_markup=markup)
    if call.data.split("|", 1)[0] == "show_cat":
        markup = types.InlineKeyboardMarkup()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        for category in Category.objects.all():
            btn = types.InlineKeyboardButton(category.title,
                                             callback_data=f"{call.data.split("|", 1)[1]}|{category.id}")
            markup.row(btn)
        bot.send_message(call.message.chat.id, text="Choose one:", reply_markup=markup)
    if call.data.split("|", 1)[0] == "del_cat":
        markup = types.InlineKeyboardMarkup()
        category = Category.objects.get(id=call.data.split("|", 1)[1])
        category.delete()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You deleted category", reply_markup=markup)
    if call.data.split("|", 1)[0] == "show_user":
        markup = types.InlineKeyboardMarkup()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        if call.data.split("|", 1)[0] == "add_admin":
            for user in CustomUser.objects.filter(is_staff=False, is_superuser=False):
                btn = types.InlineKeyboardButton(user.username, callback_data=f"{call.data.split("|", 1)[1]}|{user.id}")
                markup.row(btn)
        else:
            for user in CustomUser.objects.filter(is_staff=True, is_superuser=False):
                btn = types.InlineKeyboardButton(user.username, callback_data=f"{call.data.split("|", 1)[1]}|{user.id}")
                markup.row(btn)
        bot.send_message(call.message.chat.id, text="Choose one:", reply_markup=markup)
    if call.data.split("|", 1)[0] == "add_admin":
        markup = types.InlineKeyboardMarkup()
        user = CustomUser.objects.get(id=call.data.split("|", 1)[1])
        user.is_staff = True
        user.save()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You added admin", reply_markup=markup)
    if call.data.split("|", 1)[0] == "del_admin":
        markup = types.InlineKeyboardMarkup()
        user = User.objects.get(id=call.data.split("|", 1)[1])
        user.is_staff = False
        user.save()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You delete admin", reply_markup=markup)
    if call.data == "add_cat":
        start_cat_adding(call.message)
    if call.data == "finish_cat":
        markup = types.InlineKeyboardMarkup()
        info = cat_data[call.message.chat.id]
        Category.objects.update_or_create(title=info["title"], picture=info["picture"])
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You added category", reply_markup=markup)
    if call.data.split("|", 1)[0] == "edit_product":
        markup = types.InlineKeyboardMarkup()
        product = Product.objects.get(id=call.data.split("|", 1)[1])
        name_btn = types.InlineKeyboardButton(f"Name: {product.name}",
                                              callback_data=f"start_edit_product|{product.id}|name")
        description_btn = types.InlineKeyboardButton(f"Description: {product.description}",
                                                     callback_data=f"start_edit_product|{product.id}|des")

        price_btn = types.InlineKeyboardButton(f"Price: {product.price}",
                                               callback_data=f"start_edit_product|{product.id}|price")
        picture_btn = types.InlineKeyboardButton(f"Picture",
                                                 callback_data=f"start_edit_product|{product.id}|picture")
        stock_btn = types.InlineKeyboardButton(f"Stock: {product.stock}",
                                               callback_data=f"start_edit_product|{product.id}|stock")
        cat_btn = types.InlineKeyboardButton(f"Category: {product.category.title}",
                                             callback_data=f"start_edit_product|{product.id}|category")
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        markup.row(name_btn)
        markup.row(description_btn)
        markup.row(picture_btn)
        markup.row(stock_btn)
        markup.row(price_btn)
        markup.row(cat_btn)
        bot.send_message(call.message.chat.id, text="Choose thing you'll edit:", reply_markup=markup)
    if call.data.split("|")[0] == "start_edit_product":
        status = call.data.split("|")[2]
        if call.data.split("|")[2] == "des":
            status = "description"
        start_edit_product(call.message, call.data.split("|")[1], status)
    if call.data.split("|")[0] == "finish_edit_product":
        markup = types.InlineKeyboardMarkup()
        info = edit_product_data[call.message.chat.id]
        product = Product.objects.get(id=info["product"])
        if call.data.split("|")[1] == "category":
            product.category.id = call.data.split("|")[2]
            product.save()
        elif call.data.split("|")[1] == "name":
            product.name = info[call.data.split("|")[1]]
            product.save()
        elif call.data.split("|")[1] == "description":
            product.description = info[call.data.split("|")[1]]
            product.save()
        elif call.data.split("|")[1] == "price":
            product.price = info[call.data.split("|")[1]]
            product.save()
        elif call.data.split("|")[1] == "picture":
            product.picture = info[call.data.split("|")[1]]
            product.save()
        elif call.data.split("|")[1] == "stock":
            product.stock = info[call.data.split("|")[1]]
            product.save()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You edited product", reply_markup=markup)
    if call.data.split("|", 1)[0] == "edit_cat":
        markup = types.InlineKeyboardMarkup()
        cat = Category.objects.get(id=call.data.split("|", 1)[1])
        name_btn = types.InlineKeyboardButton(f"Title: {cat.name}", callback_data=f"start_edit_cat|{cat.id}|title")
        picture_btn = types.InlineKeyboardButton(f"Picture",
                                                 callback_data=f"start_edit_cat|{cat.id}|picture")
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        markup.row(name_btn)
        markup.row(picture_btn)
        bot.send_message(call.message.chat.id, text="Choose thing you'll edit:", reply_markup=markup)
    if call.data.split("|")[0] == "start_edit_cat":
        status = call.data.split("|")[2]
        start_edit_cat(call.message, call.data.split("|")[1], status)
    if call.data.split("|")[0] == "finish_edit_product":
        markup = types.InlineKeyboardMarkup()
        info = edit_product_data[call.message.chat.id]
        cat = Category.objects.get(id=info["cat"])
        if call.data.split("|")[1] == "title":
            cat.name = info[call.data.split("|")[1]]
            cat.save()
        elif call.data.split("|")[1] == "picture":
            cat.picture = info[call.data.split("|")[1]]
            cat.save()
        menu_btn = types.InlineKeyboardButton("Menu", callback_data="menu")
        markup.row(menu_btn)
        bot.send_message(call.message.chat.id, text="You edited product", reply_markup=markup)
bot.infinity_polling()
