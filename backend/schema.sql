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

-- 插入一些示例数据
INSERT INTO `solution_notes` (`content`, `author_name`, `author_type`, `like_count`, `helped_count`) VALUES
('I quit filters and watched more vlogs by ordinary people.', 'Sarah M.', 'signature', 123, 123),
('Look at yourself smiling more often.', 'Emily R.', 'signature', 87, 87),
('Practice self-compassion and positive self-talk.', 'David L.', 'signature', 54, 54),
('Focus on inner qualities rather than physical appearance.', 'Jessica K.', 'signature', 32, 32);
