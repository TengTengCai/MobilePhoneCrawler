CREATE DATABASE IF NOT EXISTS mobile_phone_crawler CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `mobile_phone_crawler`;
create table if not exists phone(
    p_id         int auto_increment primary key,
    zol_id       int            not null unique,
    p_name       varchar(64)    not null,
    price        float          null,
    image_url    varchar(256)   not null,
    p_cpu        varchar(64)    not null,
    front_camera varchar(64)    null,
    rear_camera  varchar(64)    null,
    ram          int            null,
    battery      varchar(16)    null,
    screen       varchar(16)    null,
    resolution   varchar(32)    null,
    web_url      varchar(256)   not null
);