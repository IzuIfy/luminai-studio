# Luminai Studio - Mobile & Web Apps Setup Guide

## 📱 Project Overview

This monorepo contains:
- **Web App**: Next.js 14 with TypeScript, Tailwind CSS, Zustand
- **Mobile App**: React Native with Expo, Bottom Tab Navigation
- **Shared Packages**: Type-safe API client and shared types

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pnpm install
```

### 2. Web App Development
```bash
cd apps/web
pnpm dev
```
Visit: http://localhost:3000

### 3. Mobile App Development
```bash
cd apps/mobile
pnpm start
```
Then press 'i' for iOS or 'a' for Android

## 📁 Project Structure

```
luminai-studio/
├── apps/
│   ├── web/                  # Next.js web application
│   │   ├── src/
│   │   │   ├── app/          # Pages and routes
│   │   │   ├── components/   # Reusable components
│   │   │   └── stores/       # Zustand state
│   │   ├── next.config.js
│   │   └── tsconfig.json
│   │
│   └── mobile/               # React Native with Expo
│       ├── src/
│       │   ├── screens/      # Screen components
│       │   └── stores/       # Zustand state
│       ├── app.json
│       └── App.tsx
│
├── packages/
│   ├── shared/               # Shared types & utilities
│   │   └── src/
│   │       └── types/
│   │           └── user.ts
│   │
│   └── api-client/           # Unified API client
│       └── src/
│           ├── http-client.ts
│           └── modules/
│               ├── auth.ts
│               ├── projects.ts
│               └── content.ts
│
├── pnpm-workspace.yaml
├── tsconfig.json
└── package.json
```

## 🎯 Key Features

### Web App (`apps/web`)
✅ Dashboard with sidebar navigation
✅ Image generation interface
✅ Video creator
✅ Project management
✅ Settings page
✅ Responsive Tailwind CSS design
✅ Dark theme UI

### Mobile App (`apps/mobile`)
✅ Bottom tab navigation (5 tabs)
✅ Native iOS/Android support
✅ Camera integration
✅ Image picker
✅ Same auth system as web
✅ Material Design inspired UI

### Shared Packages
✅ Type-safe API client
✅ Authentication module
✅ Project management APIs
✅ Content generation APIs
✅ Shared user types

## 🔐 Authentication

Both apps use the same authentication system via `@luminai/api-client`:

```typescript
import { apiClient } from '@luminai/api-client'

// Login
const response = await apiClient.auth.login({
  email: 'user@example.com',
  password: 'password'
})
// Response: { token: string, user: User }

// Register
await apiClient.auth.register({
  email: 'user@example.com',
  password: 'password',
  name: 'John Doe'
})

// Logout
await apiClient.auth.logout()
```

## 📚 API Client Modules

### Auth Module
- `login(email, password)` - User login
- `register(email, password, name)` - User registration
- `logout()` - User logout
- `refreshToken()` - Refresh auth token

### Projects Module
- `getProjects(page, limit)` - Get user's projects
- `getProject(id)` - Get single project
- `createProject(data)` - Create new project
- `updateProject(id, data)` - Update project
- `deleteProject(id)` - Delete project
- `duplicateProject(id)` - Duplicate project

### Content Module
- `generateImage(prompt, options)` - Generate images
- `createVideo(prompt, options)` - Create videos
- `textToSpeech(text, options)` - Convert text to audio
- `removeBackground(imageUrl)` - Remove backgrounds
- `cloneVoice(audioUrl, options)` - Clone voices

## 🔧 Environment Variables

### Web App (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_STORAGE_URL=http://localhost:3000/storage
```

### Mobile App (`app.json` extra section)
```json
{
  "extra": {
    "apiUrl": "http://localhost:3000"
  }
}
```

## 📦 Dependencies

### Web App
- `next@14` - React framework
- `react@18` - UI library
- `tailwindcss@3` - Styling
- `zustand@4` - State management
- `react-query@3` - Data fetching
- `axios@1.6` - HTTP client
- `framer-motion` - Animations
- `react-hot-toast` - Notifications

### Mobile App
- `expo@50` - React Native framework
- `react-native@0.74` - Mobile framework
- `@react-navigation@6` - Navigation
- `zustand@4` - State management
- `react-query@3` - Data fetching
- `axios@1.6` - HTTP client

### Shared
- `typescript@5` - Type safety
- `axios@1.6` - HTTP requests

## 🎨 UI/UX

### Web App Features
- Purple and pink gradient theme
- Dark slate background
- Tailwind CSS components
- Smooth transitions and hover effects
- Responsive grid layouts
- Sidebar navigation

### Mobile App Features
- Material Design inspired
- Bottom tab navigation
- Dark theme
- Touch-friendly spacing
- Native icons via Ionicons

## 🔌 Integration with Backend

The API client connects to your backend at the configured URL. Implement these endpoints:

### Authentication
```
POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout
POST /api/auth/refresh
```

### Projects
```
GET /api/projects?page=1&limit=20
GET /api/projects/:id
POST /api/projects
PUT /api/projects/:id
DELETE /api/projects/:id
POST /api/projects/:id/duplicate
```

### Content
```
POST /api/content/image/generate
POST /api/content/video/create
POST /api/content/tts
POST /api/content/background/remove
POST /api/content/voice/clone
```

## 🧪 Development

### Web App Development
```bash
cd apps/web

# Development server
pnpm dev

# Build for production
pnpm build
pnpm start

# Type checking
pnpm type-check

# Linting
pnpm lint
```

### Mobile App Development
```bash
cd apps/mobile

# Start dev server
pnpm start

# iOS
pnpm ios

# Android
pnpm android

# Web
pnpm web
```

## 🚢 Deployment

### Web App (Vercel/Netlify)
```bash
pnpm web:build
# Deploy the build output
```

### Mobile App (Expo)
```bash
# Configure EAS
eas build --platform ios
eas build --platform android

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

## 📖 Shared Code Example

### Using Auth Store
```typescript
'use client'  // Web app
// or no directive (Mobile app)

import { useAuthStore } from '@/stores/auth'

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuthStore()

  if (!isAuthenticated) {
    return <button onClick={() => login('email', 'password')}>Login</button>
  }

  return (
    <div>
      <p>Welcome, {user?.name}</p>
      <button onClick={() => logout()}>Logout</button>
    </div>
  )
}
```

### Using API Client
```typescript
import { useQuery } from 'react-query'
import { apiClient } from '@luminai/api-client'

function ProjectsList() {
  const { data, isLoading } = useQuery(
    ['projects'],
    () => apiClient.projects.getProjects(1, 20)
  )

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      {data?.items.map(project => (
        <div key={project.id}>{project.title}</div>
      ))}
    </div>
  )
}
```

## 🎯 Next Steps

1. ✅ **Setup Complete** - Monorepo structure ready
2. **Connect Backend** - Update API endpoints
3. **Add Auth Pages** - Login/register UI
4. **Implement Features** - Image generator, video creator
5. **Add Testing** - Jest & React Testing Library
6. **CI/CD Pipeline** - GitHub Actions
7. **Deploy** - Vercel (web), EAS (mobile)

## 📚 Resources

- [Next.js Docs](https://nextjs.org/docs)
- [React Native Docs](https://reactnative.dev)
- [Expo Docs](https://docs.expo.dev)
- [Zustand Docs](https://github.com/pmndrs/zustand)
- [React Query Docs](https://tanstack.com/query)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

## ⚠️ Important Notes

- Both apps share the same API client for consistency
- Authentication state is synchronized via Zustand
- Token is stored in localStorage (web) or AsyncStorage (mobile)
- All API calls are intercepted to add Authorization headers
- 401 responses redirect to login
