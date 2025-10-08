-- 创建数据库
CREATE DATABASE IF NOT EXISTS `mirror-notes-db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `mirror-notes-db`;

-- 解决方案笔记表
CREATE TABLE IF NOT EXISTS `solution_notes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `content` TEXT NOT NULL COMMENT '笔记内容',
    `author_name` VARCHAR(50) DEFAULT 'Anonymous' COMMENT '作者名称',
    `author_type` ENUM('anonymous', 'signature') DEFAULT 'anonymous' COMMENT '作者类型',
    `like_count` INT DEFAULT 0 COMMENT '点赞数',
    `helped_count` INT DEFAULT 0 COMMENT '帮助人数',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_author_type` (`author_type`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='解决方案笔记表';

-- 用户点赞表
CREATE TABLE IF NOT EXISTS `user_likes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_ip` VARCHAR(45) NOT NULL COMMENT '用户IP地址',
    `note_id` INT NOT NULL COMMENT '笔记ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '点赞时间',
    UNIQUE KEY `unique_user_note` (`user_ip`, `note_id`),
    FOREIGN KEY (`note_id`) REFERENCES `solution_notes`(`id`) ON DELETE CASCADE,
    INDEX `idx_note_id` (`note_id`),
    INDEX `idx_user_ip` (`user_ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户点赞表';

-- 便签表 (Message Wall Stickers)
CREATE TABLE IF NOT EXISTS `wall_stickers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `text` TEXT NOT NULL COMMENT '便签内容',
    `type` ENUM('anxiety', 'support') DEFAULT 'anxiety' COMMENT '便签类型',
    `category` VARCHAR(50) DEFAULT '' COMMENT '分类',
    `body_part` VARCHAR(100) DEFAULT '' COMMENT '身体部位',
    `intensity` TINYINT DEFAULT 3 COMMENT '焦虑程度(1-5)',
    `position_x` DECIMAL(5,2) DEFAULT 50.00 COMMENT 'X坐标百分比',
    `position_y` DECIMAL(5,2) DEFAULT 50.00 COMMENT 'Y坐标百分比',
    `rotation` DECIMAL(5,2) DEFAULT 0.00 COMMENT '旋转角度',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_type` (`type`),
    INDEX `idx_category` (`category`),
    INDEX `idx_intensity` (`intensity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息墙便签表';

-- 便签连接表
CREATE TABLE IF NOT EXISTS `sticker_connections` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `sticker1_id` INT NOT NULL COMMENT '便签1 ID',
    `sticker2_id` INT NOT NULL COMMENT '便签2 ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '连接时间',
    UNIQUE KEY `unique_connection` (`sticker1_id`, `sticker2_id`),
    FOREIGN KEY (`sticker1_id`) REFERENCES `wall_stickers`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sticker2_id`) REFERENCES `wall_stickers`(`id`) ON DELETE CASCADE,
    INDEX `idx_sticker1` (`sticker1_id`),
    INDEX `idx_sticker2` (`sticker2_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='便签连接表';

-- 便签反应表
CREATE TABLE IF NOT EXISTS `sticker_reactions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `sticker_id` INT NOT NULL COMMENT '便签ID',
    `reaction_type` ENUM('same', 'great') NOT NULL COMMENT '反应类型',
    `user_ip` VARCHAR(45) NOT NULL COMMENT '用户IP',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '反应时间',
    UNIQUE KEY `unique_user_reaction` (`sticker_id`, `reaction_type`, `user_ip`),
    FOREIGN KEY (`sticker_id`) REFERENCES `wall_stickers`(`id`) ON DELETE CASCADE,
    INDEX `idx_sticker_id` (`sticker_id`),
    INDEX `idx_user_ip` (`user_ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='便签反应表';

-- 插入一些示例数据
INSERT INTO `solution_notes` (`content`, `author_name`, `author_type`, `like_count`, `helped_count`) VALUES
('I quit filters and watched more vlogs by ordinary people.', 'Sarah M.', 'signature', 123, 123),
('Look at yourself smiling more often.', 'Emily R.', 'signature', 87, 87),
('Practice self-compassion and positive self-talk.', 'David L.', 'signature', 54, 54),
('Focus on inner qualities rather than physical appearance.', 'Jessica K.', 'signature', 32, 32);

-- 插入示例便签数据
INSERT INTO `wall_stickers` (`text`, `type`, `category`, `body_part`, `intensity`, `position_x`, `position_y`, `rotation`) VALUES
('It feels too large and affects my confidence', 'anxiety', 'nose', 'My nose', 5, 10.00, 20.00, 2.5),
('The scars on my face make me feel self-conscious', 'anxiety', 'skin', 'Acne scars', 4, 30.00, 50.00, -1.2),
('My hair never looks the way I want it to', 'anxiety', 'hair', 'Frizzy hair', 2, 55.00, 10.00, 3.8),
("You're beautiful just the way you are", 'support', '', '', 3, 70.00, 60.00, -2.1),
('My teeth are not straight and I feel embarrassed', 'anxiety', 'mouth', 'Crooked teeth', 5, 50.00, 35.00, 1.5),
('I feel uncomfortable with my body proportions', 'anxiety', 'body', 'Body shape', 4, 5.00, 75.00, -0.8),
('I understand how you feel, we all have insecurities', 'support', '', '', 2, 25.00, 5.00, 4.2),
('People always comment on my ears', 'anxiety', 'other', 'Big ears', 2, 45.00, 80.00, -3.1),
('My eyes look different from each other', 'anxiety', 'eyes', 'Asymmetrical eyes', 3, 2.00, 40.00, 2.8),
('Your smile lights up the room, never hide it', 'support', '', '', 4, 82.00, 70.00, -1.5),
('My hairline is receding and I feel older', 'anxiety', 'hair', 'Receding hairline', 5, 75.00, 15.00, 0.9),
('My skin tone is uneven and I feel less attractive', 'anxiety', 'skin', 'Dull skin', 2, 50.00, 65.00, -2.7);
