# Common Components

This directory contains reusable UI components used throughout the application.

## Components

### AppHeader.vue
Main application header with title and responsive navigation.

**Features:**
- Mobile-first design
- Hamburger menu on mobile devices
- Integrates AppNavigation component
- Responsive layout (mobile/desktop)

**Usage:**
```vue
<template>
  <AppHeader />
</template>

<script setup lang="ts">
import AppHeader from '@/components/common/AppHeader.vue';
</script>
```

### AppNavigation.vue
Responsive navigation menu component.

**Props:**
- `isMobile` (boolean, optional): Whether to render in mobile mode

**Events:**
- `navigate`: Emitted when a navigation link is clicked (mobile only)

**Features:**
- Responsive layout (horizontal on desktop, vertical on mobile)
- Active route highlighting
- Tailwind CSS styling

**Usage:**
```vue
<template>
  <AppNavigation :is-mobile="false" />
  <AppNavigation :is-mobile="true" @navigate="handleNavigate" />
</template>

<script setup lang="ts">
import AppNavigation from '@/components/common/AppNavigation.vue';

function handleNavigate() {
  console.log('Navigation clicked');
}
</script>
```

### LoadingSpinner.vue
Animated loading spinner component.

**Features:**
- Centered layout
- Smooth animation
- Blue color scheme

**Usage:**
```vue
<template>
  <LoadingSpinner v-if="loading" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';

const loading = ref(true);
</script>
```

### ErrorMessage.vue
Error message display component with icon.

**Props:**
- `message` (string, required): Error message to display

**Features:**
- Red color scheme
- Error icon (X in circle)
- Left border accent
- Tailwind CSS styling

**Usage:**
```vue
<template>
  <ErrorMessage v-if="error" :message="error" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';

const error = ref('Something went wrong');
</script>
```

### SuccessMessage.vue
Success message display component with icon.

**Props:**
- `message` (string, required): Success message to display

**Features:**
- Green color scheme
- Success icon (checkmark in circle)
- Left border accent
- Tailwind CSS styling

**Usage:**
```vue
<template>
  <SuccessMessage v-if="success" :message="success" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SuccessMessage from '@/components/common/SuccessMessage.vue';

const success = ref('Operation completed successfully');
</script>
```

## Design Principles

All components follow these principles:

1. **Mobile-First**: Designed for mobile devices first, then enhanced for larger screens
2. **Responsive**: Adapt to different screen sizes using Tailwind CSS breakpoints
3. **Accessible**: Include proper ARIA labels and semantic HTML
4. **Consistent**: Use consistent color schemes and spacing
5. **Reusable**: Can be used throughout the application without modification

## Tailwind CSS Classes

Common Tailwind patterns used:
- `md:hidden` / `md:flex`: Show/hide on mobile/desktop
- `container mx-auto px-4`: Centered container with padding
- `text-gray-600 hover:text-blue-600`: Interactive text colors
- `transition`: Smooth transitions for interactive elements
