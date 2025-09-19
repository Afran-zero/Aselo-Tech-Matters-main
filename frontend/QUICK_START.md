# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Create Environment File
Create `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8001
```

### 3. Start Development Server
```bash
npm start
```

Your app will be running at `http://localhost:3000`

## 🎯 Key Features Demo

### Chat Interface
1. Open the app in your browser
2. Type a message in the chat input
3. Press Enter or click the send button
4. Watch the typing indicator and receive responses

### Auto-Fill Form
1. Have a conversation with the chatbot
2. Mention personal information (name, email, address)
3. Click the "Auto Fill" button in the form section
4. Watch as the form fields populate automatically

### Live Summary
1. Have an extended conversation
2. Watch the summary panel update automatically
3. Click the refresh button for manual updates
4. View timestamp information

### Mobile Experience
1. Resize your browser to mobile width (< 1024px)
2. Use the tab navigation between Chat and Form
3. Experience smooth transitions and responsive design

## 🎨 Customization

### Change Theme Colors
Edit `src/index.css` and modify CSS variables:
```css
:root {
  --primary: 217.2 91.2% 59.8%;     /* Change primary color */
  --background: 222.2 84% 4.9%;     /* Change background */
}
```

### Add New Form Fields
1. Update `FormData` interface in `src/services/api.ts`
2. Add field to the form in `src/components/FormSection.tsx`
3. Include validation logic and error handling

### Customize Messages
Edit initial messages in `src/components/Chatbot.tsx`:
```typescript
const [messages, setMessages] = useState<ChatMessage[]>([
  {
    id: '1',
    content: 'Your custom welcome message here!',
    sender: 'bot',
    timestamp: new Date(),
  },
]);
```

## 🔧 API Integration

### Backend Endpoints Required
Your backend should implement these endpoints:

```typescript
// Send chat message
POST /chat
{
  "sessionId": "string",
  "message": "string"
}

// Auto-fill form data
POST /autofill
{
  "sessionId": "string"
}

// Submit form
POST /submitForm
{
  "sessionId": "string",
  "formData": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "notes": "string"
  }
}

// Get conversation summary
GET /summarize/{sessionId}
```

### Response Formats
All responses should follow this format:
```typescript
{
  "success": boolean,
  "data": any,
  "message": string,
  "error": string
}
```

## 📱 Browser Testing

### Desktop Testing
- Chrome 88+ ✅
- Firefox 85+ ✅
- Safari 14+ ✅
- Edge 88+ ✅

### Mobile Testing
- iOS Safari 14+ ✅
- Chrome Mobile 88+ ✅
- Samsung Internet ✅

## 🐛 Common Issues

### Issue: API Calls Failing
**Solution**: Check that your backend is running and the `REACT_APP_API_URL` environment variable is correct.

### Issue: Form Auto-fill Not Working
**Solution**: Ensure your backend `/autofill` endpoint returns data in the correct format with the `formData` property.

### Issue: Summary Not Updating
**Solution**: Verify your backend `/summarize` endpoint is accessible and returns the summary in the correct format.

### Issue: Mobile Layout Issues
**Solution**: Clear browser cache and ensure you're using a supported mobile browser.

## 📊 Performance Tips

### For Development
- Use React Developer Tools for debugging
- Enable network throttling to test slow connections
- Use Lighthouse for performance audits

### For Production
- Run `npm run build` for optimized builds
- Enable gzip compression on your server
- Use a CDN for static assets
- Implement proper caching headers

## 🎓 Learning Resources

### React + TypeScript
- [React TypeScript Documentation](https://react-typescript-cheatsheet.netlify.app/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Tailwind CSS
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind UI Components](https://tailwindui.com/)

### shadcn/ui
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Radix UI Primitives](https://www.radix-ui.com/)

### Framer Motion
- [Framer Motion Documentation](https://www.framer.com/motion/)
- [Animation Examples](https://www.framer.com/motion/examples/)

## 🤝 Getting Help

1. **Check the Documentation**: Start with README.md and COMPONENTS.md
2. **Review Component Code**: All components are thoroughly commented
3. **Test in Isolation**: Use React Storybook for component testing
4. **Debug Network Issues**: Use browser developer tools
5. **Performance Issues**: Use React Profiler and Lighthouse

## ✅ Production Checklist

- [ ] Environment variables configured
- [ ] API endpoints tested and working
- [ ] Form validation working correctly
- [ ] Mobile responsiveness verified
- [ ] Performance audit completed
- [ ] Accessibility testing completed
- [ ] Error handling tested
- [ ] Browser compatibility verified
- [ ] Security headers configured
- [ ] Analytics integration (if needed)

Enjoy building with the Aselo Support Platform! 🎉
