# Review Success/Error Message Templates

## Overview
Complete HTML and JavaScript templates for displaying review submission success, error, info, and moderation messages.

## Files Created/Modified

### 1. Template: `core/templates/core/review_messages.html`
Reusable message template component with four message types:

#### Message Types:
- **Success Message** - Shown after successful review submission
- **Error Message** - Shown when review submission fails, with error details
- **Info Message** - Shown when user has already reviewed the product
- **Moderation Message** - Shown when review is pending approval

#### Features:
- Icons (checkmark, error, info, clock)
- Color-coded backgrounds
- Smooth animations
- Auto-close functionality (5 seconds)
- Manual close buttons
- Error detail lists for validation errors
- Scroll-into-view behavior

### 2. Stylesheet: `static/core/css/review_messages.css`
Styling for all message types including:
- Flexbox layout for message content
- Icon styling with background colors
- Color schemes for each message type:
  - Success: Green (#4caf50)
  - Error: Red (#f44336)
  - Warning/Moderation: Yellow (#ffc107)
  - Info: Blue (#2196f3)
- Animations and transitions
- Responsive design for mobile devices
- Focus states and hover effects

### 3. JavaScript: `static/store/js/review-system.js`
Complete ReviewSystem class with:
- Rating star display and selection
- Form submission handling
- Helpful/Unhelpful vote tracking
- AJAX communication
- Integration with message display functions

### 4. Updated Template: `core/templates/core/product_detail.html`
- Added review_messages.html include
- Added review_messages.css link
- Added review-system.js script reference

## Message Functions

### showSuccessMessage(message)
Displays a success message that auto-closes after 5 seconds.

**Example:**
```javascript
showSuccessMessage('Your review has been submitted successfully!');
```

### showErrorMessage(message, errors)
Displays an error message with optional error details list.

**Example:**
```javascript
showErrorMessage('Please fix the errors below.', {
    'title': ['Title must be at least 3 characters long.'],
    'content': ['Content must be at least 10 characters long.']
});
```

### showInfoMessage(message)
Displays an info message for user notifications.

**Example:**
```javascript
showInfoMessage('You have already reviewed this product.');
```

### showModerationMessage(message)
Displays a moderation notice for reviews pending approval.

**Example:**
```javascript
showModerationMessage('Your review has been submitted and will appear after moderation.');
```

## HTML Structure

### Message Container
```html
<div id="review-[type]-message" class="review-message alert alert-[type]">
    <div class="message-content">
        <div class="message-icon">
            <i class="fas fa-[icon]"></i>
        </div>
        <div class="message-text">
            <h4>Title</h4>
            <p>Message content</p>
        </div>
        <button class="close-message" onclick="closeMessage(this)">
            <i class="fas fa-times"></i>
        </button>
    </div>
</div>
```

## CSS Classes

### Message Types
- `.alert-success` - Green background, success icon
- `.alert-danger` - Red background, error icon
- `.alert-warning` - Yellow background, clock icon
- `.alert-info` - Blue background, info icon

### Components
- `.review-message` - Main container
- `.message-content` - Flex container for message parts
- `.message-icon` - Icon container (circular background)
- `.message-text` - Text content container
- `.close-message` - Close button

## Usage in Review Form

### Integration Example:
```javascript
submitReview(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showModerationMessage(data.message);
            form.reset();
            setTimeout(() => location.reload(), 3000);
        } else {
            showErrorMessage(data.message, data.errors);
        }
    })
    .catch(error => {
        showErrorMessage('An error occurred while submitting your review');
    });
}
```

## Color Scheme

| Message Type | Background | Icon Color | Border Color |
|-------------|-----------|-----------|-------------|
| Success | #e8f5e9 | #4caf50 | #4caf50 |
| Error | #ffebee | #f44336 | #f44336 |
| Warning | #fff8e1 | #ffc107 | #ffc107 |
| Info | #e3f2fd | #2196f3 | #2196f3 |

## Features

✓ Animated slide-down entrance
✓ Auto-close after 5 seconds
✓ Manual close button
✓ Error list support with field names
✓ Smooth color transitions
✓ Accessibility friendly
✓ Mobile responsive
✓ Font Awesome icon support
✓ Scroll into view behavior
✓ CSRF protection compatible

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- IE11+ (with graceful degradation)

## Accessibility

- Semantic HTML structure
- Clear icon indicators
- High contrast colors (WCAG AA compliant)
- Keyboard navigable
- Screen reader friendly

## Customization

### Change message colors in CSS:
```css
.review-message.alert-success {
    background: #your-color;
    border-left-color: #your-color;
}
```

### Adjust auto-close timeout (in JavaScript):
```javascript
setTimeout(() => {
    messageDiv.style.display = 'none';
}, 5000); // Change 5000 to desired milliseconds
```

### Modify animation speed in CSS:
```css
animation: slideDown 0.4s ease-out; /* Change 0.4s */
```
