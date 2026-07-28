# EchoDesk CSS Class Documentation - Summary

## 📋 Overview

EchoDesk uses a comprehensive CSS framework organized across 10 main CSS files:
- **admin.css** - Admin dashboard styling
- **auth.css** - Authentication pages (login, signup, etc.)
- **complaints.css** - Complaint management components
- **components.css** - Reusable UI components (buttons, cards, modals, etc.)
- **dashboard.css** - Dashboard layouts and widgets
- **forms.css** - Form elements and layouts
- **layout.css** - Page structure (header, sidebar, footer)
- **main.css** - Global styles
- **responsive.css** - Responsive design breakpoints
- **utilities.css** - Utility/helper classes

---

## 🎯 Main Class Categories

### 1. **Components & UI Elements**
- `.button`, `.btn`, `.btn--primary`, `.btn--secondary`, `.btn--danger`
- `.card`, `.card--glass`, `.card--hoverable`
- `.modal`, `.modal--sm`, `.modal--lg`
- `.badge`, `.chip`, `.notification-card`
- `.stat-card` - Statistics display cards
- `.timeline` - Timeline visualization

### 2. **Form Classes**
- `.form-group` - Form field grouping
- `.form-grid` - Form layout grid (2-3 columns)
- `.form-check` - Checkboxes and radio inputs
- `.form-file` - File upload styling
- `.form-floating` - Floating label inputs
- `.form-actions` - Form button containers

### 3. **Layout & Structure**
- `.app-shell` - Main application container
- `.page` - Page wrapper
- `.sidebar` - Navigation sidebar
- `.topbar` - Top navigation bar
- `.main-content` - Primary content area
- `.app-layout` - Overall app layout
- `.grid` - CSS Grid layouts

### 4. **Dashboard Classes**
- `.dashboard` - Main dashboard container
- `.dashboard-grid` - Dashboard grid layout
- `.dashboard--admin`, `.dashboard--student`, `.dashboard--staff`
- `.stat-grid` - Statistics grid
- `.chart-container` - Chart wrappers

### 5. **Status & State Classes**
- `.is-active` - Active state
- `.is-loading` - Loading state
- `.is-disabled` - Disabled state
- `.is-invalid` - Invalid/error state
- `.is-valid` - Valid state
- `.status-badge--open`, `.status-badge--closed`, `.status-badge--resolved`

### 6. **Authentication Classes**
- `.auth__card` - Login/signup card containers
- `.auth__form` - Auth form styling
- `.auth__header`, `.auth__footer` - Auth page sections
- `.auth__container--split` - Split layout for auth pages
- `.auth__floating-shape` - Decorative shapes

---

## 🎨 **Classes for Centering Elements**

### **Flexbox Centering** (Most Common)
```html
<!-- Center items horizontally and vertically -->
<div class="d-flex justify-center align-center">
    <p>Centered content</p>
</div>

<!-- Center items horizontally only -->
<div class="d-flex justify-center">
    <button>Centered Button</button>
</div>

<!-- Center items vertically only -->
<div class="d-flex align-center">
    <span>Vertically centered</span>
</div>
```

**Key Classes:**
- `.d-flex` - Enable flexbox display
- `.justify-center` - Horizontal centering (main axis)
- `.align-center` - Vertical centering (cross axis)
- `.justify-between` - Space items between
- `.justify-end` - Align to right
- `.flex-column` - Stack vertically
- `.flex-row` - Arrange horizontally (default)

### **Grid Centering**
```html
<!-- Center using CSS Grid -->
<div class="grid-center">
    <div>Centered Grid Item</div>
</div>

<!-- Multi-column grid -->
<div class="grid grid-2">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

**Key Classes:**
- `.grid-center` - Center items in grid
- `.grid`, `.grid--2`, `.grid--3`, `.grid--4` - Grid layouts
- `.d-grid` - Enable grid display

### **Text Centering**
```html
<div class="text-center">
    <h1>Centered Heading</h1>
    <p>Centered paragraph</p>
</div>
```

**Key Classes:**
- `.text-center` - Text alignment center
- `.text-left`, `.text-right` - Other text alignments

### **Form Action Centering**
```html
<div class="form-actions form-actions--center">
    <button class="btn btn--primary">Submit</button>
    <button class="btn btn--secondary">Cancel</button>
</div>
```

**Key Classes:**
- `.form-actions--center` - Center form buttons
- `.form-actions--right` - Align buttons right
- `.form-actions--spread` - Distribute buttons across width

---

## 🌙 **Classes for Dark Mode**

### **Current Status**
⚠️ **Note:** The documentation doesn't explicitly list dedicated dark mode classes. Dark mode is likely implemented through:

1. **CSS Variables/Themes** - The actual CSS files may use CSS custom properties
2. **System Preference Detection** - Modern approach using `prefers-color-scheme`
3. **Theme Toggle** - JavaScript-based theme switching

### **Recommended Approach for Dark Mode**

If implementing dark mode, look for:

**In CSS Files:**
- Search for `@media (prefers-color-scheme: dark)` 
- Look for CSS variables like `--bg-color`, `--text-color`, `--primary-color`
- Check for `.dark` or `.theme-dark` classes

**Color/Text Classes (Light Mode Default):**
```html
<!-- These may have dark mode equivalents in CSS -->
<div class="text-primary">Primary text</div>
<div class="text-secondary">Secondary text</div>
<div class="text-muted">Muted text</div>
<div class="text-white">White text</div>

<!-- State-based colors -->
<div class="text-danger">Error/Danger text</div>
<div class="text-success">Success text</div>
<div class="text-warning">Warning text</div>
```

**Background Classes:**
- `.card` - Card background
- `.card--glass` - Glassmorphism effect (works in both modes)
- `.bg-primary`, `.bg-secondary` (if available)

### **How to Check for Dark Mode**
1. Open the actual CSS files (especially `main.css` and `utilities.css`)
2. Search for `dark`, `theme`, or `prefers-color-scheme`
3. Check for CSS variables in the `:root` selector
4. Look for media queries: `@media (prefers-color-scheme: dark)`

---

## ⚠️ **Most Commonly Used Classes**

### **Spacing (Padding & Margin)**
- `.p-{0-16}` - Padding (0, 1, 2, 3, 4, 6, 8, 10, 12, 16)
- `.m-{0-16}` - Margin
- `.px-{value}` - Horizontal padding
- `.py-{value}` - Vertical padding
- `.mb-{value}` - Bottom margin
- `.mt-{value}` - Top margin

### **Display & Visibility**
- `.d-flex` - Flexbox
- `.d-grid` - Grid
- `.d-block` - Block display
- `.d-none` - Hide element
- `.d-inline`, `.d-inline-block` - Inline display

### **Gaps & Spacing in Flex/Grid**
- `.gap-{1-16}` - Gap between items
- `.gap-2`, `.gap-4`, `.gap-6`, `.gap-8` (most common)

### **Text & Typography**
- `.fs-{xs,sm,base,lg,xl}` - Font size
- `.fw-{normal,medium,semibold,bold}` - Font weight
- `.text-muted`, `.text-subtle` - Muted text
- `.text-xs`, `.text-sm` - Small text sizes

### **Responsive**
- All classes adjust for mobile/tablet/desktop
- Use `.sidebar--collapsed` for mobile

---

## 🔧 **Quick Reference Examples**

### **Centered Card**
```html
<div class="d-flex justify-center align-center" style="min-height: 100vh;">
    <div class="card p-6">
        <h2 class="card__title">Centered Card</h2>
        <p>Your content here</p>
    </div>
</div>
```

### **Centered Form**
```html
<div class="form-actions form-actions--center">
    <button class="btn btn--primary">Save</button>
    <button class="btn btn--secondary">Cancel</button>
</div>
```

### **Centered Text in Container**
```html
<div class="text-center p-6">
    <h1 class="fs-xl fw-bold">Heading</h1>
    <p class="text-muted">Subheading</p>
</div>
```

---

## 📝 **Next Steps**

To fully understand dark mode support:
1. Review the actual CSS files in `/static/css/`
2. Check if theme variables are defined
3. Look for a theme toggle component
4. Test with system dark mode preference

**Need more specifics?** Check the individual CSS files for exact color values and dark mode implementations.