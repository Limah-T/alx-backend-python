'''
CREATE TABLE messaging_app.user (
    user_id CHAR(36) NOT NULL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6),
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) DEFAULT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    phone_number VARCHAR(16),
    role VARCHAR(6) NOT NULL DEFAULT 'user',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    UNIQUE KEY (email),
    INDEX (user_id),
    INDEX (email)
);
CREATE TABLE messaging_app.message (
    message_id CHAR(36) NOT NULL PRIMARY KEY,
    sender_id CHAR(36) NOT NULL,
    message_body TEXT NOT NULL,
    sent_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    FOREIGN KEY (sender_id) REFERENCES messaging_app.user(user_id) ON DELETE CASCADE,
    INDEX (message_id)
);
CREATE TABLE messaging_app.conversation (
    conversation_id CHAR(36) NOT NULL PRIMARY KEY,
    participants_id CHAR(36) NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    FOREIGN KEY (participants_id) REFERENCES messaging_app.user(user_id) ON DELETE CASCADE,
    INDEX (conversation_id)
);
'''