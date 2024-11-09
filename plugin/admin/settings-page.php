<?php
// Add admin menu for settings page
function chatbot_add_admin_menu() {
    add_menu_page(
        'Chatbot Settings',
        'Chatbot Settings',
        'manage_options',
        'chatbot-settings',
        'chatbot_settings_page_html',
        'dashicons-format-chat'
    );
}
add_action('admin_menu', 'chatbot_add_admin_menu');

// Render settings page
function chatbot_settings_page_html() {
    ?>
    <div class="wrap">
        <h1>Chatbot Plugin Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('chatbot_options_group');
            do_settings_sections('chatbot-settings');
            ?>
            <table class="form-table">
                <tr valign="top">
                    <th scope="row">WebSocket URL</th>
                    <td><input type="text" name="chatbot_websocket_url" value="<?php echo esc_attr(get_option('chatbot_websocket_url')); ?>" /></td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Register settings
function chatbot_register_settings() {
    register_setting('chatbot_options_group', 'chatbot_websocket_url');
}
add_action('admin_init', 'chatbot_register_settings');
