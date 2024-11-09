# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Chatbot Plugin

This WordPress plugin integrates a chatbot with a FastAPI backend.

## Installation

1. Upload the plugin folder to `/wp-content/plugins/` directory.
2. Activate the plugin from the WordPress admin dashboard.
3. Go to the **Chatbot Settings** page under the **Settings** menu to configure the WebSocket URL for your FastAPI backend.
4. Add the `[chatbot_widget]` shortcode to any page or post where you want the chatbot to appear.

## Frontend Integration

The chatbot UI is built with Vue.js. The plugin automatically loads the necessary Vue.js app files. You can customize the design by modifying the `App.vue` and `chatbot.css` files in the plugin's `/frontend/dist` directory.
