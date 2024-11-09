<?php
/**
 * Plugin Name: Chatbot Plugin
 * Description: A plugin to integrate a chatbot with a FastAPI backend into WordPress.
 * Version: 1.0
 * Author: Your Name
 * License: GPL2
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Define plugin constants
define( 'CHATBOT_PLUGIN_URL', plugin_dir_url( __FILE__ ) );
define( 'CHATBOT_PLUGIN_PATH', plugin_dir_path( __FILE__ ) );

// Include necessary files
require_once( CHATBOT_PLUGIN_PATH . 'src/admin/settings-page.php' );       // Admin settings page
require_once( CHATBOT_PLUGIN_PATH . 'src/public/chatbot-widget.php' );    // Frontend chatbot widget
require_once( CHATBOT_PLUGIN_PATH . 'includes/api/api-integration.php' ); // API integration
require_once( CHATBOT_PLUGIN_PATH . 'includes/utils/common-functions.php' ); // Common functions

// Load frontend Vue.js app (compiled assets)
function chatbot_enqueue_scripts() {
    wp_enqueue_script('chatbot-vue-js', CHATBOT_PLUGIN_URL . 'frontend/dist/js/app.js', array(), '1.0', true);
    wp_enqueue_style('chatbot-vue-css', CHATBOT_PLUGIN_URL . 'frontend/dist/css/app.css', array(), '1.0');
}
add_action('wp_enqueue_scripts', 'chatbot_enqueue_scripts');

// Register chatbot widget shortcode
function chatbot_widget_shortcode() {
    return '<div id="chatbot-app"></div>'; // This is where Vue.js will render the chatbot
}
add_shortcode('chatbot_widget', 'chatbot_widget_shortcode');
