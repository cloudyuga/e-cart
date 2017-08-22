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

INSERT INTO `product` VALUES (1,'nike','shoe',11,'/static/shoe.jpg'),
                             (2,'iphone','mobile',100,'/static/mobile.jpg'),
                             (3, 'titan', 'watch', 50, '/static/watch.jpeg'),
                             (4, 'philips', 'speaker', 75, '/static/speaker.jpeg'),
                             (5, 'adidas', 'tshirt', 60, '/static/tshirt.jpeg'),
                             (6, 'sony', 'tv', 1000, '/static/tv.jpg'),
                             (7, 'seagate', 'harddisk', 200, '/static/harddisk.jpg'),
                             (8, 'journal', 'book', 30, '/static/journal.jpg');

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

DROP TABLE IF EXISTS `cart`;

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `total_price` int(11) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ;

DROP TABLE IF EXISTS `cart_items`;

CREATE TABLE `cart_items` (
  `cart_items_id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`cart_items_id`),
  KEY `cart_id` (`cart_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`),
  CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
);

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` int(11) DEFAULT NULL,
  `order_status` varchar(50) DEFAULT NULL,
  `orderDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  KEY `cart_id` (`cart_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`)
);


DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) DEFAULT NULL,
  `paid_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
);






