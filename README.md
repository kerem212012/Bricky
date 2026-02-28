# Bricky 🧱

A modern Django-based e-commerce platform with integrated Telegram bot support, designed for seamless shopping experiences and real-time customer engagement.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Development](#development)
- [Project Architecture](#project-architecture)
- [Contributing](#contributing)

## Overview

Bricky is a full-featured e-commerce platform built with Django 5.2, providing a robust backend for managing products, orders, users, and notifications. It features a custom Telegram bot for real-time customer engagement and a comprehensive notification system.

**Version:** 0.1.0  
**Python:** >=3.12  
**Author:** kerem212012

## ✨ Features

### Core E-Commerce
- 🛍️ **Product Catalog** - Manage products with categories, images, and metadata
- 🛒 **Shopping Cart** - Full shopping cart functionality with multiple items
- 📦 **Order Management** - Complete order processing with status tracking
- 🏷️ **Product Categorization** - Organize products into categories

### User Management
- 👤 **Custom User Model** - Extended user model with additional fields
- 🔐 **Authentication System** - User registration and login with email verification
- 📱 **Telegram Integration** - Link Telegram accounts to user profiles
- ✅ **Email Verification** - Secure email-based account verification

### Notifications & Communication
- 📧 **Email Notifications** - Automated email alerts for orders and updates
- 📬 **Newsletter System** - Newsletter subscription and management
- 🤖 **Telegram Bot** - Real-time customer engagement via Telegram
- 💬 **Contact Forms** - Customer inquiries and support requests

### Additional Features
- ❓ **Help/FAQ System** - Knowledge base with categories and articles
- 📄 **Legal Pages** - Terms of Service, Privacy Policy, etc.
- 🖼️ **Media Management** - Product images, categories, and user pictures
- 🎨 **Custom Filters** - Django template filters for enhanced view rendering

## 🛠️ Tech Stack

### Backend Framework
- **Django** 5.2.7 - Web framework
- **Python** 3.12+ - Programming language

### Key Dependencies
- **django-phonenumber-field** - Phone number validation and storage
- **django-debug-toolbar** - Development debugging tools
- **Pillow** - Image processing for product and user media
- **pytelegrambotapi** - Telegram bot API client
- **environs** - Environment variable management
- **ruff** - Python code formatter and linter

### Database
- **SQLite** - Default development database (easily swappable with PostgreSQL)

## 📁 Project Structure

```
bricky/
├── backend/                          # Django backend application
│   ├── bricky/                      # Project configuration
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # URL routing
│   │   ├── asgi.py                  # ASGI configuration
│   │   └── wsgi.py                  # WSGI configuration
│   │
│   ├── core/                        # Core application
│   │   ├── models.py                # Core models (Contact, Help, etc.)
│   │   ├── views.py                 # Core views
│   │   ├── urls.py                  # Core URL patterns
│   │   ├── forms.py                 # Core forms
│   │   ├── templates/               # HTML templates
│   │   │   └── core/
│   │   │       ├── base.html        # Base template
│   │   │       ├── index.html       # Homepage
│   │   │       ├── legal/           # Legal page templates
│   │   │       └── pages/           # Other page templates
│   │   └── templatetags/            # Custom template filters
│   │
│   ├── store/                       # Product catalog app
│   │   ├── models.py                # Category, Product models
│   │   ├── views.py                 # Store views
│   │   ├── urls.py                  # Store URL patterns
│   │   ├── forms.py                 # Store forms
│   │   ├── admin.py                 # Admin configuration
│   │   ├── migrations/              # Database migrations
│   │   └── templates/
│   │       └── store/               # Store page templates
│   │
│   ├── orders/                      # Order management app
│   │   ├── models.py                # Order, Cart, CartItem models
│   │   ├── views.py                 # Order views
│   │   ├── urls.py                  # Order URL patterns
│   │   ├── signals.py               # Order signal handlers
│   │   ├── admin.py                 # Admin configuration
│   │   ├── migrations/              # Database migrations
│   │   └── templates/
│   │       └── orders/              # Order templates
│   │
│   ├── users/                       # User management app
│   │   ├── models.py                # CustomUser model
│   │   ├── views.py                 # User views
│   │   ├── urls.py                  # User URL patterns
│   │   ├── forms.py                 # User registration/login forms
│   │   ├── utils.py                 # User utilities
│   │   ├── admin.py                 # Admin configuration
│   │   ├── migrations/              # Database migrations
│   │   └── templates/
│   │       └── users/               # User page templates
│   │
│   ├── notifications/               # Email notifications app
│   │   ├── models.py                # Notification, Subscription models
│   │   ├── views.py                 # Notification views
│   │   ├── urls.py                  # Notification URL patterns
│   │   ├── forms.py                 # Subscription forms
│   │   ├── admin.py                 # Admin configuration
│   │   ├── migrations/              # Database migrations
│   │   └── templates/
│   │       └── notifications/       # Email templates
│   │
│   ├── media/                       # User-uploaded media
│   │   ├── products/                # Product images
│   │   ├── categories/              # Category images
│   │   └── user_pictures/           # User profile pictures
│   │
│   ├── static/                      # Static files (development)
│   │   ├── core/                    # Core static files
│   │   ├── orders/                  # Order static files
│   │   ├── store/                   # Store static files
│   │   ├── users/                   # User static files
│   │   └── img/                     # Images
│   │
│   ├── staticfiles/                 # Compiled static files (production)
│   │
│   ├── db.sqlite3                   # Development database
│   └── manage.py                    # Django management script
│
├── tgbot/                           # Telegram bot application
│   ├── bot.py                       # Main bot code
│   └── test.py                      # Bot tests
│
├── pyproject.toml                   # Project configuration & dependencies
└── README.md                        # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- pip or poetry package manager

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Bricky
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   **Using pip:**
   ```bash
   pip install -e .
   ```

   **Using Poetry:**
   ```bash
   poetry install
   ```

5. **Navigate to backend directory**
   ```bash
   cd backend
   ```

6. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, uses SQLite by default)
# DATABASE_URL=sqlite:///db.sqlite3

# Email configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook/

# Media files
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

### Django Settings

Key configurations in `bricky/settings.py`:

- **INSTALLED_APPS**: Includes all custom apps (core, store, orders, users, notifications)
- **TEMPLATES**: Template loaders and context processors
- **STATIC_FILES**: Static file handling and compression
- **DATABASES**: Database configuration
- **EMAIL**: Email backend configuration

## 🏃 Running the Application

### Development Server

```bash
cd backend
python manage.py runserver
```

The application will be available at:
- **Frontend**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`

### With Debug Toolbar

Debug Toolbar is included for development. Access it via the `DEBUG` setting.

### Running Telegram Bot

To run the Telegram bot:

**Using pip:**
```bash
cd tgbot
python bot.py
```

**Using Poetry:**
```bash
poetry run python bot.py
```

Or activate the poetry shell first:
```bash
poetry shell
cd tgbot
python bot.py
```

## 🧪 Development

### Creating New Django Apps

**Using pip:**
```bash
cd backend
python manage.py startapp myapp
```

**Using Poetry:**
```bash
cd backend
poetry run python manage.py startapp myapp
```

### Making Database Changes

1. Create migrations:
   ```bash
   # Using pip
   python manage.py makemigrations
   
   # Using Poetry
   poetry run python manage.py makemigrations
   ```

2. Review changes and apply:
   ```bash
   # Using pip
   python manage.py migrate
   
   # Using Poetry
   poetry run python manage.py migrate
   ```

### Code Quality

The project uses **ruff** for code formatting and linting:

**Using pip:**
```bash
ruff check .
ruff format .
```

**Using Poetry:**
```bash
poetry run ruff check .
poetry run ruff format .
```

## 🏗️ Project Architecture

### MVC Pattern
Bricky follows Django's MVT (Model-View-Template) architecture:

- **Models** - Data layer defining the database schema
- **Views** - Business logic handling requests and responses
- **Templates** - Presentation layer with HTML/CSS

### Key Models

#### Users App
- `CustomUser` - Extended user model with Telegram ID and additional fields

#### Store App
- `Category` - Product categories
- `Product` - Product information and inventory

#### Orders App
- `Cart` - Shopping cart per user
- `CartItem` - Items in cart
- `Order` - Order information
- `OrderItem` - Items in order

#### Notifications App
- `Subscription` - Newsletter subscriptions
- `Notification` - Email notification tracking

### Signal Handlers
Order signals handle:
- Automatic order creation on checkout
- Inventory updates
- Notification triggers

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guide
- Use ruff for code formatting
- Write meaningful commit messages
- Add comments for complex logic

## 🤖 Telegram Bot (`bot.py`)

The Telegram bot provides a comprehensive e-commerce interface directly within Telegram, enabling users to browse products, manage shopping carts, and complete purchases.

### Bot Features

#### User Management
- **Authentication**: Link existing accounts via email or register new accounts
- **Account Integration**: Connect Telegram ID with user profiles
- **Custom User Model**: Seamless integration with Django's CustomUser model

#### Product Browsing
- **Product Catalog**: Browse all available products with inline search
- **Categories**: Organize products by category
- **New Releases**: View latest products added to the store
- **Product Details**: View name, description, price, and images

#### Shopping Cart Management
- **Add to Cart**: Add products to shopping cart with automatic quantity tracking
- **Quantity Management**: Increment/decrement item quantities
- **Cart Items**: View all items in cart with current prices
- **Cart Total**: Automatic calculation of total price
- **Remove Items**: Delete or reduce cart item quantities

#### Order & Payment
- **Checkout**: Process orders with delivery address
- **Payment Integration**: Integrated Telegram payment system using LabeledPrice
- **Order Confirmation**: Create orders after successful payment
- **Order Tracking**: View order status and details

#### Admin Panel
- **Product Management**:
  - Create new products (name, description, price, photo, category)
  - Edit existing products (name, description, price, photo, stock, category)
  - Delete products
  - Product photo upload to `/media/products/`

- **Category Management**:
  - Create new categories (title, photo)
  - Edit category details (title, photo)
  - Delete categories
  - Category photo upload to `/media/categories/`

#### Navigation
- **Inline Keyboards**: User-friendly navigation with inline buttons
- **State Management**: Tracks user state machine for multi-step processes
- **Menu System**: Main menu with dynamic buttons based on user roles

### State Machine Architecture

The bot uses state tracking dictionaries for different workflows:

```python
user_state = {}           # Checkout/payment flow states
product_state = {}        # Product creation flow states
cat_state = {}            # Category creation flow states
reg_state = {}            # Registration flow states
edit_product_state = {}   # Product edit flow states
edit_cat_state = {}       # Category edit flow states
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `menu(message)` | Display main navigation menu |
| `create_user(message)` | Create user or link existing account via email |
| `create_cart(tg_id)` | Initialize shopping cart for user |
| `add_to_cart(tg_id, product_id)` | Add products to cart with quantity tracking |
| `delete_item(cart_item_id)` | Remove or decrement cart items |
| `start_pay(message)` | Initiate payment process |
| `confirm_order(tg_id)` | Create order from cart after payment |
| `handle_product_steps(message)` | Multi-step product creation handler |
| `handle_cat_steps(message)` | Multi-step category creation handler |
| `handle_callback_query(call)` | Process inline button interactions |

### Environment Configuration

Required environment variables for bot in `.env`:

```env
# Telegram Bot
TG_TOKEN=your-telegram-bot-token-here
PAY_TOKEN=your-telegram-payment-token-here
```

### Workflow Examples

**User Registration Flow:**
1. User starts bot and provides email
2. Bot checks if email exists in system
3. If exists: links account and displays menu
4. If new: initiates registration (email → password → account created)

**Product Browsing & Purchase Flow:**
1. User selects "Products" or "Categories"
2. Bot displays inline keyboard with options
3. User clicks product to view details
4. User adds to cart (quantity tracked per item)
5. User proceeds to checkout
6. Bot requests delivery address
7. Bot initiates payment via Telegram payment system
8. After payment confirmation: creates order and clears cart

**Admin Product Creation Flow:**
1. Admin selects "Admin Panel" → "Create Product"
2. Bot collects: name → description → price → photo
3. Admin selects product category
4. Bot confirms and creates product in database
5. Photo saved to `/media/products/` with unique filename

### Photo Upload Handling

Photos are processed and saved with unique filenames:
```python
file_unique_id = message.photo[-1].file_unique_id
file_path = f"../backend/media/{category}/{file_unique_id}.png"
```

This ensures no filename conflicts and maintains organized media structure.

### Database Integration

The bot seamlessly integrates with Django models:
- **CustomUser**: User accounts and Telegram ID mapping
- **Product**: Product catalog with prices and details
- **Category**: Product categorization
- **Cart/CartItem**: Shopping cart data persistence
- **Order/OrderItem**: Order history and details
- **Customer**: Customer profile information

### Starting the Bot

The bot uses `bot.infinity_polling()` for continuous message polling and handles:
- Message handlers for text and photo input
- Callback handlers for inline keyboard interactions
- Pre-checkout handlers for payment validation
- Successful payment confirmation handlers

## 📦 Media Files Organization

| Directory | Purpose |
|-----------|---------|
| `/media/products/` | Product images uploaded via bot |
| `/media/categories/` | Category images uploaded via bot |
| `/media/user_pictures/` | User profile pictures |

## 📝 License

This project is part of the Bricky e-commerce platform.

## 📧 Contact

For questions or inquiries:
- **Email**: rockstarfoxykerem@gmail.com
- **Project**: Bricky E-Commerce Platform

---

**Happy coding! 🚀**
