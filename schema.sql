CREATE SCHEMA `tarkov` ;

USE `tarkov`;

DROP TABLE IF EXISTS `teamkills`;
CREATE TABLE `teamkills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(254) DEFAULT NULL,
  `discord_id` varchar(255) DEFAULT NULL,
  `deaths` int DEFAULT NULL,
  `guild_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) 
