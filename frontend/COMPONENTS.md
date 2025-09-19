# Component Documentation

## Overview

This document provides detailed information about each component in the Aselo Support Platform frontend.

## Core Components

### Chatbot Component (`src/components/Chatbot.tsx`)

**Purpose**: Interactive chat interface for real-time conversation with the support assistant.

**Props**:
```typescript
interface ChatbotProps {
  sessionId: string;
  onSessionUpdate?: (sessionId: string) => void;
}
```

**Features**:
- Real-time message exchange with typing indicators
- Auto-scroll to latest messages
- Message timestamps and sender identification
- Loading states and error handling
- Keyboard shortcuts (Enter to send)
- Message persistence during session

**State Management**:
- `messages`: Array of chat messages with unique IDs
- `inputMessage`: Current input field value
- `isLoading`: API call loading state
- `messagesEndRef`: Reference for auto-scrolling
- `inputRef`: Reference for input focus management

**API Integration**:
- Uses `apiService.sendMessage()` for chat communication
- Handles session ID updates from backend
- Error recovery with user-friendly messages

### FormSection Component (`src/components/FormSection.tsx`)

**Purpose**: Contact information form with validation and auto-fill functionality.

**Props**:
```typescript
interface FormSectionProps {
  sessionId: string;
}
```

**Form Fields**:
- **Full Name** (required): Text input with validation
- **Email Address** (required): Email input with format validation
- **Phone Number** (required): Tel input with format validation
- **Address** (required): Textarea for full address
- **Additional Notes** (optional): Textarea for extra information

**Features**:
- Real-time field validation with error messages
- Auto-fill button that populates fields from chat context
- Form submission with success/error feedback
- Field-level error clearing on user input
- Responsive form layout

**Validation Rules**:
- Name: Required, minimum 2 characters
- Email: Required, valid email format
- Phone: Required, valid phone number format
- Address: Required, minimum 10 characters

**State Management**:
- `formData`: Object containing all form field values
- `errors`: Object containing field-specific error messages
- `isAutoFilling`: Loading state for auto-fill operation
- `isSubmitting`: Loading state for form submission
- `submitStatus`: Success/error status after submission

### SummaryPanel Component (`src/components/SummaryPanel.tsx`)

**Purpose**: Displays AI-generated conversation summaries with auto-refresh capability.

**Props**:
```typescript
interface SummaryPanelProps {
  sessionId: string;
}
```

**Features**:
- Auto-refreshing summary every 30 seconds
- Manual refresh button with loading indicator
- Formatted summary display with proper typography
- Last updated timestamp with relative time display
- Error handling with retry mechanisms
- Empty state for new conversations

**State Management**:
- `summary`: Current conversation summary text
- `lastUpdated`: Timestamp of last summary update
- `isLoading`: Loading state for summary fetching
- `error`: Error message for failed requests
- `hasLoadedOnce`: Flag to differentiate first load vs. errors

**Auto-refresh Logic**:
- Automatically fetches summary on component mount
- Sets up interval for periodic updates
- Cleans up interval on unmount
- Pauses auto-refresh during manual refresh

### Layout Component (`src/components/Layout.tsx`)

**Purpose**: Main application layout with responsive design and navigation.

**Features**:
- **Desktop Layout**: Side-by-side grid with chatbot (5 columns) and form/summary (7 columns)
- **Mobile Layout**: Tabbed interface with smooth transitions
- Session management and status indicators
- Professional header with branding
- Footer with session information

**Responsive Breakpoints**:
- **Mobile**: < 1024px - Tabbed interface
- **Desktop**: ≥ 1024px - Side-by-side layout

**State Management**:
- `sessionId`: Current chat session identifier
- `isMobileMenuOpen`: Mobile tab state (Chat/Form)

**Session Management**:
- Generates unique session ID on mount
- Passes session ID to all child components
- Handles session updates from chatbot

## UI Components (shadcn/ui)

### Button Component (`src/components/ui/button.tsx`)

**Variants**:
- `default`: Primary blue button
- `destructive`: Red for dangerous actions
- `outline`: Transparent with border
- `secondary`: Muted background
- `ghost`: No background, hover effect
- `link`: Text link styling

**Sizes**:
- `default`: Standard height (40px)
- `sm`: Small height (36px)
- `lg`: Large height (44px)
- `icon`: Square icon button (40x40px)

### Input Component (`src/components/ui/input.tsx`)

**Features**:
- Consistent styling across all input types
- Focus ring and error state support
- Disabled state styling
- Placeholder text styling

### Textarea Component (`src/components/ui/textarea.tsx`)

**Features**:
- Resizable textarea with minimum height
- Consistent styling with input component
- Auto-resize capability
- Error state support

### Card Components (`src/components/ui/card.tsx`)

**Structure**:
- `Card`: Main container
- `CardHeader`: Header section with padding
- `CardTitle`: Styled heading
- `CardDescription`: Muted description text
- `CardContent`: Main content area
- `CardFooter`: Footer section

### ScrollArea Component (`src/components/ui/scroll-area.tsx`)

**Features**:
- Custom scrollbar styling
- Smooth scrolling behavior
- Cross-browser compatibility
- Overflow handling

## Styling and Theming

### CSS Variables

The application uses CSS custom properties for theming:

```css
:root {
  --background: 222.2 84% 4.9%;      /* Dark background */
  --foreground: 210 40% 98%;         /* Light text */
  --primary: 217.2 91.2% 59.8%;      /* Blue primary */
  --secondary: 217.2 32.6% 17.5%;    /* Dark blue secondary */
  --muted: 217.2 32.6% 17.5%;        /* Muted backgrounds */
  --border: 217.2 32.6% 17.5%;       /* Border color */
  --radius: 0.5rem;                  /* Border radius */
}
```

### Animation Classes

Custom animation classes for enhanced UX:

```css
.message-enter {
  opacity: 0;
  transform: translateY(10px);
}

.message-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.3s ease, transform 0.3s ease;
}
```

### Responsive Design Utilities

- Container max-width with responsive padding
- Grid system with 12-column layout
- Responsive text sizing
- Mobile-first breakpoint system

## Performance Considerations

### Component Optimization

- **React.memo**: Used for expensive re-renders
- **useCallback**: For stable function references
- **useMemo**: For expensive calculations
- **Lazy Loading**: Components load on demand

### API Optimization

- **Request Debouncing**: Prevents excessive API calls
- **Caching**: Stores responses for better performance
- **Error Boundaries**: Prevents app crashes
- **Retry Logic**: Automatic retry for failed requests

### Bundle Optimization

- **Tree Shaking**: Removes unused code
- **Code Splitting**: Loads components on demand
- **Asset Optimization**: Optimized images and fonts
- **Minification**: Compressed production builds

## Accessibility Features

### Keyboard Navigation

- Tab order follows logical flow
- Enter key submits forms
- Escape key closes modals
- Arrow keys for navigation

### Screen Reader Support

- Proper ARIA labels and roles
- Semantic HTML elements
- Status announcements
- Error message associations

### Visual Accessibility

- High contrast color scheme
- Focus indicators
- Consistent typography scale
- Responsive text sizing

## Testing Strategy

### Unit Tests

- Component rendering tests
- User interaction tests
- API integration tests
- Form validation tests

### Integration Tests

- Component communication tests
- API flow tests
- Session management tests
- Error handling tests

### E2E Tests

- Complete user journeys
- Cross-browser testing
- Mobile responsiveness
- Performance testing

## Maintenance Guidelines

### Code Quality

- TypeScript strict mode
- ESLint and Prettier
- Consistent naming conventions
- Documentation requirements

### Component Updates

- Backward compatibility
- Prop interface stability
- Migration guides
- Version management

### Performance Monitoring

- Bundle size tracking
- Render performance
- API response times
- User experience metrics
