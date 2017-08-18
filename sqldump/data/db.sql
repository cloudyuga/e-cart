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
