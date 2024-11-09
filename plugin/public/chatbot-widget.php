<?php
// Display the chatbot widget on frontend
function display_chatbot_widget() {
    // The Vue.js app will be rendered in the div with id 'chatbot-app'
    echo '<div id="chatbot-app"></div>';
}

// Hook into WordPress content to display the chatbot widget
add_action('the_content', function($content) {
    if (is_single() || is_page()) {
        $content .= do_shortcode('[chatbot_widget]');
    }
    return $content;
});
