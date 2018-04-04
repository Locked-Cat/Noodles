DROP DATABASE IF EXISTS noodles;

CREATE DATABASE noodles;
USE noodles;

CREATE TABLE users (
    `id` VARCHAR(50) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `password` VARCHAR(50) NOT NULL,
    `created_at` REAL NOT NULL,
    UNIQUE KEY `idx_email` (`email`),
    KEY `idx_created_at` (`created_at`),
    PRIMARY KEY (`id`)
) engine=innodb DEFAULT charset=utf8;

CREATE TABLE blogs (
    `id` VARCHAR(50) NOT NULL,
    `user_id` VARCHAR(50) NOT NULL,
    `created_at` REAL NOT NULL,
    key `idx_created_at` (`created_at`),
    PRIMARY KEY (`id`)
) engine=innodb DEFAULT charset=utf8;