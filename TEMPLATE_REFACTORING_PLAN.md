# Template Refactoring Plan for Bricky LEGO Store

## Current Structure Analysis

### Apps & Templates
- **Core App**: 13 templates (main store pages)
- **Store App**: Product displays
- **Users App**: 6 templates (authentication, profile)
- **Orders App**: Order management
- **Notifications App**: (no templates currently)

---

## Refactoring Recommendations

### 1. **Create Shared Component Library (Base Components)**

Create reusable template components in `core/templates/components/`:

```
components/
├── cards/
│   ├── product_card.html          # Reusable product card
│   ├── review_card.html            # Review display card
│   ├── order_card.html             # Order summary card
│   └── category_card.html          # Category card
├── forms/
│   ├── form_field.html             # Generic form field
│   ├── search_form.html            # Search bar component
│   └── filter_form.html            # Filter controls
├── messages/
│   ├── alert.html                  # Alert/notification component
│   ├── toast.html                  # Toast notification
│   └── inline_messages.html        # Form validation messages
├── pagination/
│   ├── pagination.html             # Pagination controls
│   └── page_info.html              # Page information display
├── headers/
│   ├── page_header.html            # Page title & breadcrumb
│   ├── hero_section.html           # Hero banner section
│   └── breadcrumb.html             # Breadcrumb navigation
├── footers/
│   ├── footer_main.html            # Main footer
│   └── footer_widgets.html         # Footer widgets
├── lists/
│   ├── grid_list.html              # Grid layout container
│   ├── table_list.html             # Table layout
│   └── item_list.html              # Vertical list
└── sections/
    ├── features_section.html       # Features/benefits section
    ├── newsletter_cta.html         # Newsletter signup
    ├── testimonials.html           # User testimonials
    └── stats_section.html          # Statistics display
```

### 2. **Create Template Inheritance Structure**

```
templates/
├── base.html                       # Root template
├── layouts/
│   ├── main_layout.html            # Standard main layout (sidebar + content)
│   ├── full_width_layout.html      # Full-width layout
│   ├── minimal_layout.html         # Minimal layout (no extras)
│   ├── dashboard_layout.html       # For user dashboard/profile
│   └── admin_layout.html           # For admin/management pages
└── includes/
    ├── navbar.html                 # Navigation bar
    ├── sidebar.html                # Sidebar navigation
    ├── breadcrumb.html             # Breadcrumb navigation
    ├── footer.html                 # Footer
    ├── messages.html               # Django messages display
    └── head_meta.html              # Meta tags (SEO)
```

### 3. **App-Specific Template Organization**

#### Core App
```
core/templates/core/
├── index.html                      # Homepage
├── pages/
│   ├── about.html                  # About page
│   ├── contact.html                # Contact form
│   ├── privacy_policy.html
│   └── terms_of_service.html
├── shop/
│   ├── shop.html                   # Shop listing (refactored)
│   ├── category.html               # Category view (refactored)
│   ├── search.html                 # Search results (refactored)
│   └── new_releases.html           # New products
├── product/
│   ├── detail.html                 # Product detail page
│   ├── _reviews.html               # Reviews section (include)
│   ├── _specifications.html        # Product specs (include)
│   └── _related.html               # Related products (include)
├── cart/
│   ├── cart.html                   # Shopping cart
│   ├── _items.html                 # Cart items list (include)
│   └── _summary.html               # Cart summary (include)
├── checkout/
│   ├── checkout.html               # Checkout page
│   ├── _shipping_form.html         # Shipping info (include)
│   ├── _payment_form.html          # Payment form (include)
│   └── _order_summary.html         # Order summary (include)
├── newsletter/
│   ├── subscribe.html              # Newsletter signup
│   └── success.html                # Success page
└── email/
    ├── order_confirmation.html
    ├── password_reset.html
    └── email_verify.html
```

#### Users App
```
users/templates/users/
├── auth/
│   ├── login.html
│   ├── register.html               # (create if missing)
│   ├── password_reset.html         # (create if missing)
│   └── password_reset_confirm.html # (create if missing)
├── email/
│   ├── email_verify.html
│   ├── email_verified_success.html
│   ├── email_verified_failed.html
│   └── email_resend.html
├── profile/
│   ├── profile.html                # Profile dashboard
│   ├── profile_edit.html           # Edit profile
│   ├── _orders_history.html        # Orders list (include)
│   ├── _saved_addresses.html       # Saved addresses (include)
│   ├── _preferences.html           # User preferences (include)
│   └── _account_settings.html      # Account settings (include)
└── dashboard/
    └── dashboard.html              # Main dashboard
```

#### Orders App
```
orders/templates/orders/
├── order_confirmation.html         # Order confirmation
├── order_history.html              # Orders list
├── order_detail.html               # Order detail view
├── _order_item.html                # Single order item (include)
├── _tracking.html                  # Order tracking (include)
└── _status_timeline.html           # Status timeline (include)
```

#### Store App
```
store/templates/store/
├── product_list.html               # Products grid/list
├── category_list.html              # Categories grid
└── _product_item.html              # Single product (include)
```

### 4. **Key Refactoring Changes**

#### A. Extract Repeating Components
- **Product Card**: Used in shop, category, search, new_releases → Create `_product_card.html`
- **Review Display**: Used in product detail → Create `_review_item.html`
- **Forms**: Contact, Newsletter, Review → Use consistent form styling
- **Messages/Alerts**: Create centralized message display system

#### B. Improve Code Reusability
- Replace inline JavaScript with shared utilities
- Consolidate CSS classes and naming
- Use `{% include %}` for repeated sections
- Use `{% block %}` for consistent override points

#### C. Data Organization
- Move complex template logic to views
- Use `context_processors` for global data
- Simplify templates with calculated properties

#### D. Naming Conventions
- Use descriptive, hierarchical names
- Follow Django best practices
- Include purpose in filename (`_form.html`, `_list.html`, etc.)

### 5. **Specific Template Improvements**

#### Product Detail Page (`product_detail.html`)
✅ Already refactored with:
- External CSS files
- Star rating component
- Review message templates

**Still needs:**
- Extract reviews section into include
- Extract specs into include
- Extract related products into include

#### Cart Page (`cart.html`)
✅ Already refactored with external CSS

**Still needs:**
- Extract cart items into component
- Extract summary into component
- Use consistent pricing display

#### Homepage (`index.html`)
**Refactor:**
- Extract hero section to component
- Extract product grid to component
- Extract categories section to component
- Extract features section to component
- Extract newsletter CTA to component

#### Shop/Category Pages
**Refactor:**
- Extract filter form to component
- Extract products grid to component
- Create consistent pagination component
- Standardize product card display

### 6. **Best Practices to Implement**

1. **Use Template Includes for Reusable Sections**
   ```django
   {% include 'components/cards/product_card.html' with product=product %}
   ```

2. **Use Block Tags for Customization**
   ```django
   {% block title %}Default Title{% endblock %}
   ```

3. **Create Template Tags for Complex Logic**
   - `{% rating_stars rating=5 %}`
   - `{% product_badge product=product %}`
   - `{% format_price price=99.99 %}`

4. **Use Context Processors for Global Data**
   - Cart count in navbar
   - Current categories for sidebar
   - Site settings

5. **DRY Principle**
   - Never repeat HTML structure
   - Use includes/components for repeated patterns
   - Consolidate similar templates

### 7. **CSS Organization (Already Done)**

✅ Static CSS files created:
- `cart.css` / `cart-utils.css`
- `product-detail.css` / `product-detail-utils.css`
- `category.css`
- `new_releases.css`
- `review_messages.css`
- `newsletter_subscribe.css`
- `newsletter_success.css`
- `checkout.css`

### 8. **JavaScript Organization**

Existing JS files:
- `cart.js` / `cart-config.js`
- `product-detail.js` / `product-detail-config.js`
- `review-system.js`
- `review-messages.js`
- `search.js`

**Create shared utilities:**
- `common.js` - Shared functions (API calls, notifications)
- `form-handler.js` - Form submission handling
- `modal.js` - Modal dialog system

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
1. Create component library structure
2. Extract common components (card, alert, pagination)
3. Consolidate navbar/footer

### Phase 2: Core App (Week 2)
1. Refactor homepage
2. Refactor shop/category pages
3. Refactor product detail (further)
4. Refactor cart/checkout

### Phase 3: Users & Orders (Week 3)
1. Refactor authentication pages
2. Refactor user profile
3. Refactor order pages

### Phase 4: Polish & Optimize (Week 4)
1. Create template tags for complex logic
2. Add caching strategies
3. Performance optimization
4. SEO improvements

---

## Expected Outcomes

✅ **Reduced Duplication**: -40% template code
✅ **Improved Maintainability**: Centralized component updates
✅ **Better Performance**: Component caching opportunity
✅ **Consistency**: Uniform styling & behavior across app
✅ **Scalability**: Easy to add new pages using existing components
✅ **Developer Experience**: Clear structure, easy to understand

---

## Commands to Get Started

```bash
# Create component directories
mkdir -p core/templates/components/{cards,forms,messages,pagination,headers,footers,lists,sections}
mkdir -p core/templates/layouts
mkdir -p core/templates/includes

# Move/create component files
touch core/templates/components/cards/product_card.html
touch core/templates/components/forms/search_form.html
# ... and so on
```

---

## Questions to Clarify

1. **Priority**: Which pages are highest priority?
2. **Scope**: Should we include email templates in refactoring?
3. **Mobile**: Should we optimize for mobile-first?
4. **Accessibility**: WCAG compliance needed?
5. **I18n**: Multi-language support needed?

Would you like me to start with any specific phase or component?
