# Aselo Support Platform

A modern, responsive React frontend for customer support conversations with integrated form submission and AI-powered summarization.

## Features

### 🎯 Core Functionality
- **Interactive Chatbot**: Real-time conversation with typing indicators and auto-scroll
- **Smart Form Auto-fill**: AI-powered form population based on chat context
- **Live Conversation Summary**: Automatically updated conversation summaries
- **Responsive Design**: Seamless experience across desktop and mobile devices

### 🎨 UI/UX Features
- **Dark Theme**: Professional dark bluish theme optimized for extended use
- **Smooth Animations**: Framer Motion animations for enhanced user experience
- **Accessibility**: ARIA-compliant components with keyboard navigation
- **Real-time Updates**: Live session status and automatic summary refresh

### 📱 Responsive Design
- **Desktop**: Side-by-side layout with chatbot on left, form and summary on right
- **Mobile**: Tabbed interface for easy navigation between chat and form sections

## Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Framer Motion** for animations
- **Axios** for API communication
- **Lucide React** for icons

## Project Structure

```
frontend/
├── COMPONENTS.md
├── package.json
├── postcss.config.js
├── QUICK_START.md
├── tailwind.config.js
├── tsconfig.json
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── App.tsx
│   ├── index.css
│   ├── index.tsx
│   ├── components/
│   │   ├── Chatbot.tsx
│   │   ├── Layout.tsx
│   │   ├── forms/
│   │   │   ├── category_form.tsx
│   │   │   ├── child_form.tsx
│   │   │   ├── FormSection.tsx
│   │   │   └── summary_form.tsx
│   │   ├── ui/
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── scroll-area.tsx
│   │   │   ├── select.tsx
│   │   │   └── textarea.tsx
│   ├── lib/
│   │   └── utils.ts
│   ├── services/
│   │   └── api.ts
```

## Component Architecture

### 🤖 Chatbot Component
- Real-time messaging with WebSocket-like experience
- Auto-scroll to latest messages
- Typing indicators and loading states
- Message timestamps and sender identification
- Error handling and retry mechanisms

### 📝 FormSection Component
- Comprehensive form validation
- Auto-fill functionality powered by chat context
- Real-time field validation with error messages
- Success/error status indicators
- Responsive form layout

### 📊 SummaryPanel Component
- Auto-refreshing conversation summaries
- Manual refresh capability
- Loading and error states
- Formatted summary display with typography
- Last updated timestamps

### 🎯 Layout Component
- Responsive grid layout for desktop
- Mobile-first tabbed navigation
- Session management and status indicators
- Professional header and footer
- Smooth page transitions

## API Integration

### Endpoints
- `POST /chat` - Send message to chatbot
- `POST /autofill` - Get form auto-fill suggestions
- `POST /submitForm` - Submit completed form
- `GET /summarize/{sessionId}` - Get conversation summary

### Error Handling
- Comprehensive error boundaries
- User-friendly error messages
- Automatic retry mechanisms
- Graceful degradation

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- Backend API server running

### Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure environment:**
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8001
```

3. **Start development server:**
```bash
npm start
```

The application will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Design System

### Color Palette
- **Primary**: Blue (#3b82f6) - Interactive elements
- **Background**: Dark slate (#0f172a) - Main background
- **Card**: Dark blue-gray (#1e293b) - Component backgrounds
- **Muted**: Gray-blue (#64748b) - Secondary text
- **Border**: Dark gray (#334155) - Element borders

### Typography
- **Headings**: Semibold weights with proper hierarchy
- **Body Text**: Regular weight, optimized line height
- **UI Text**: Small, muted for secondary information

### Spacing & Layout
- **Grid System**: 12-column grid for desktop layouts
- **Gaps**: Consistent 4px, 8px, 16px, 24px spacing
- **Responsive Breakpoints**: Mobile-first with lg+ breakpoints

## Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Responsive images with proper sizing
- **Bundle Analysis**: Optimized dependency bundling
- **Lazy Loading**: Components load on demand
- **Memoization**: React.memo for expensive components

## Accessibility Features

- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and roles
- **Focus Management**: Logical focus flow
- **Color Contrast**: WCAG AA compliant contrast ratios
- **Responsive Text**: Scalable typography

## Browser Support

- **Modern Browsers**: Chrome 88+, Firefox 85+, Safari 14+, Edge 88+
- **Mobile Browsers**: iOS Safari 14+, Chrome Mobile 88+
- **Progressive Enhancement**: Graceful degradation for older browsers

## Development Guidelines

### Code Style
- **TypeScript**: Strict mode enabled
- **ESLint**: React and TypeScript rules
- **Prettier**: Consistent code formatting
- **Component Structure**: Functional components with hooks

### Best Practices
- **Single Responsibility**: Each component has one clear purpose
- **Prop Interfaces**: Strong typing for all component props
- **Error Boundaries**: Comprehensive error handling
- **Performance**: Optimized re-renders and state management

## Contributing

1. Follow the established code style and patterns
2. Add TypeScript types for all new components
3. Include error handling and loading states
4. Test responsive design on multiple devices
5. Ensure accessibility compliance

## License

© 2024 Aselo Support Platform. All rights reserved.
