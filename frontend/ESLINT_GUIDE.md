# ESLint & Prettier Setup Guide

## Overview

This project uses ESLint for code quality and Prettier for code formatting to ensure consistent, maintainable code.

## Quick Start

### Install Dependencies

```bash
cd frontend
npm install
```

### Run Linting

```bash
# Check for linting errors
npm run lint

# Auto-fix linting errors
npm run lint:fix

# Format code with Prettier and fix ESLint issues
npm run format

# Check formatting without fixing
npm run format:check
```

## Configuration Files

- **`.eslintrc.json`** - ESLint rules and configuration
- **`.prettierrc`** - Prettier formatting rules
- **`.eslintignore`** - Files/folders to ignore during linting
- **`.prettierignore`** - Files/folders to ignore during formatting

## Common ESLint Rules

- **react-hooks/exhaustive-deps**: Warns about missing dependencies in useEffect/useCallback
- **no-unused-vars**: Warns about unused variables
- **no-console**: Warns about console.log (allows console.warn/error)
- **react/prop-types**: Disabled (using TypeScript-style props)

## Pre-commit Hook (Optional)

To automatically format code before committing:

1. Install husky:
```bash
npm install --save-dev husky lint-staged
```

2. Add to `package.json`:
```json
{
  "lint-staged": {
    "*.{js,jsx}": [
      "prettier --write",
      "eslint --fix"
    ]
  }
}
```

## VS Code Integration

Add to `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact"
  ]
}
```

## CI/CD Integration

The build process will fail if there are ESLint errors. To ensure code quality:

1. Run `npm run lint` before committing
2. Fix all errors with `npm run lint:fix`
3. Format code with `npm run format`

## Troubleshooting

### ESLint errors in build

If Netlify build fails due to ESLint errors:
1. Run `npm run lint` locally
2. Fix errors with `npm run lint:fix`
3. Commit and push changes

### Prettier conflicts with ESLint

The `.eslintrc.json` includes `"prettier"` in extends to prevent conflicts.

### Disable rules for specific lines

```javascript
// eslint-disable-next-line rule-name
const variable = value;

// eslint-disable-line rule-name
```

## Best Practices

1. **Run linting before committing**: `npm run lint`
2. **Auto-fix when possible**: `npm run lint:fix`
3. **Format code regularly**: `npm run format`
4. **Fix warnings, not just errors**: Warnings can become errors in production builds
5. **Don't disable rules unnecessarily**: Try to fix the underlying issue
