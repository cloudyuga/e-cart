DROP DATABASE IF EXISTS `ecommerce`;
CREATE DATABASE `ecommerce`;
USE `ecommerce`;

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
);

INSERT INTO `product` VALUES (1,'nike','shoe',11,'/static/shoe.jpg'),(2,'iphone','mobile',100,'/static/mobile.jpg');

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
);
