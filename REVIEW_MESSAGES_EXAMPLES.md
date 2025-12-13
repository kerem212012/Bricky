# Review Message Display Examples

## Success Message Example

### When Displayed:
After a user successfully submits a review

### HTML:
```html
<div id="review-success-message" class="review-message alert alert-success" style="display: block;">
    <div class="message-content">
        <div class="message-icon">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="message-text">
            <h4>Thank You!</h4>
            <p>Your review has been submitted successfully and will appear after moderation.</p>
        </div>
        <button class="close-message" onclick="closeMessage(this)">
            <i class="fas fa-times"></i>
        </button>
    </div>
</div>
```

### Appearance:
- **Background**: Light green (#e8f5e9)
- **Icon**: Green check circle (#4caf50)
- **Border**: Green left border (4px)
- **Duration**: Auto-closes after 5 seconds or manual close

---

## Error Message Example

### When Displayed:
When form validation fails or submission encounters an error

### HTML with Errors:
```html
<div id="review-error-message" class="review-message alert alert-danger" style="display: block;">
    <div class="message-content">
        <div class="message-icon">
            <i class="fas fa-exclamation-circle"></i>
        </div>
        <div class="message-text">
            <h4>Error</h4>
            <p>Please fix the errors below.</p>
            <div id="error-details" style="display: block;">
                <ul id="error-list">
                    <li>title: Title must be at least 3 characters long.</li>
                    <li>content: Content must be at least 10 characters long.</li>
                    <li>rating: Rating must be between 1 and 5.</li>
                </ul>
            </div>
        </div>
        <button class="close-message" onclick="closeMessage(this)">
            <i class="fas fa-times"></i>
        </button>
    </div>
</div>
```

### Appearance:
- **Background**: Light red (#ffebee)
- **Icon**: Red exclamation circle (#f44336)
- **Border**: Red left border (4px)
- **Error List**: Shows field names and specific validation errors
- **Duration**: Stays until manually closed

---

## Info Message Example

### When Displayed:
When a user who has already reviewed tries to review again

### HTML:
```html
<div id="review-info-message" class="review-message alert alert-info" style="display: block;">
    <div class="message-content">
        <div class="message-icon">
            <i class="fas fa-info-circle"></i>
        </div>
        <div class="message-text">
            <h4>Info</h4>
            <p>You have already reviewed this product. Thank you for your feedback!</p>
        </div>
        <button class="close-message" onclick="closeMessage(this)">
            <i class="fas fa-times"></i>
        </button>
    </div>
</div>
```

### Appearance:
- **Background**: Light blue (#e3f2fd)
- **Icon**: Blue info circle (#2196f3)
- **Border**: Blue left border (4px)
- **Duration**: Auto-closes after 5 seconds

---

## Moderation Message Example

### When Displayed:
When review is submitted but awaiting admin approval

### HTML:
```html
<div id="review-moderation-message" class="review-message alert alert-warning" style="display: block;">
    <div class="message-content">
        <div class="message-icon">
            <i class="fas fa-clock"></i>
        </div>
        <div class="message-text">
            <h4>Under Review</h4>
            <p>Your review has been submitted and will appear after moderation.</p>
        </div>
        <button class="close-message" onclick="closeMessage(this)">
            <i class="fas fa-times"></i>
        </button>
    </div>
</div>
```

### Appearance:
- **Background**: Light yellow (#fff8e1)
- **Icon**: Yellow clock (#ffc107)
- **Border**: Yellow left border (4px)
- **Duration**: Auto-closes after 5 seconds

---

## JavaScript Usage Examples

### Show Success:
```javascript
showSuccessMessage('Thank you for your review!');
```

### Show Error with Details:
```javascript
showErrorMessage('Please fix the errors below.', {
    'title': ['Title must be at least 3 characters long.'],
    'content': ['Content must be at least 10 characters long.'],
    'rating': ['Please select a rating.']
});
```

### Show Info:
```javascript
showInfoMessage('You have already reviewed this product.');
```

### Show Moderation:
```javascript
showModerationMessage('Your review has been submitted and will appear after moderation.');
```

---

## Message Lifecycle

### Success/Info/Moderation Flow:
1. Message appears with slide-down animation
2. User reads the message (5 seconds)
3. Message auto-closes with fade-out
4. User can manually close anytime with X button

### Error Flow:
1. Message appears with slide-down animation
2. Error details are displayed in a list
3. Message stays visible (no auto-close)
4. User must manually close with X button after fixing errors and resubmitting

---

## Responsive Design

### Desktop (> 768px):
- Full width message with padding
- Icons are 40x40px
- Proper spacing between elements

### Mobile (≤ 768px):
- Adjusted spacing (smaller gaps)
- Icons reduced to 36x36px
- Text size optimized for readability
- Close button easily tappable

---

## Animation Details

### Entrance Animation (slideDown):
```
Duration: 0.4s
Easing: ease-out
Effect: Slides down from -20px with fade-in
```

### Message Colors

| Type | Icon | Background | Text Color | Border |
|------|------|------------|-----------|---------|
| Success | ✓ | #e8f5e9 | #2e7d32 | #4caf50 |
| Error | ! | #ffebee | #c62828 | #f44336 |
| Warning | 🕐 | #fff8e1 | #f57f17 | #ffc107 |
| Info | ℹ | #e3f2fd | #0d47a1 | #2196f3 |

---

## Integration Points

### In Product Detail Page:
1. Review form submission → Success/Error message
2. Review already exists → Info message
3. Review approved → Success message with reload
4. Validation errors → Error message with details
5. Admin moderation pending → Moderation message

### Automatic Page Reload:
```javascript
setTimeout(() => location.reload(), 3000);
```
Reloads page after moderation message (shows new review in list)

---

## Accessibility Features

✓ High contrast colors (WCAG AA compliant)
✓ Clear icon indicators
✓ Semantic HTML structure
✓ Keyboard navigable (Tab, Enter for close)
✓ Screen reader announcements
✓ Sufficient color differentiation (not relying on color alone)

---

## Customization Options

### Change Auto-Close Duration:
In `review_messages.html`, change timeout value:
```javascript
setTimeout(() => {
    messageDiv.style.display = 'none';
}, 5000); // 5000ms = 5 seconds
```

### Change Animation Speed:
In `review_messages.css`, adjust animation:
```css
animation: slideDown 0.4s ease-out; /* Change 0.4s to desired value */
```

### Change Colors:
In `review_messages.css`, update color values:
```css
.review-message.alert-success {
    background: #your-color;
    border-left-color: #your-color;
}
```

### Add Persistent Messages:
Modify JavaScript to not auto-close:
```javascript
// Remove setTimeout for messages that should stay visible
// messageDiv.style.display = 'block'; // stays forever until closed
```
