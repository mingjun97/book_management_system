# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.21)
# Database: library
# Generation Time: 2018-04-19 16:44:31 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table admins
# ------------------------------------------------------------

DROP TABLE IF EXISTS `admins`;

CREATE TABLE `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(256) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `contact` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;

INSERT INTO `admins` (`id`, `password`, `name`, `contact`)
VALUES
	(1,'12345','admin',NULL);

/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table books
# ------------------------------------------------------------

DROP TABLE IF EXISTS `books`;

CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(256) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `publisher` varchar(256) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `author` varchar(256) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `store` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;

INSERT INTO `books` (`id`, `type`, `name`, `publisher`, `year`, `author`, `price`, `amount`, `store`)
VALUES
	(100,'文学','活着','中国青年出版社',2017,'老舍',30,30,30),
	(101,'技术','计算机科学','清华大学出版社',2018,'诸葛',100,10,10),
	(102,'医学','内科学','中国卫生出版社',2000,'主编',120.3,12,12),
	(103,'历史','资治通鉴','新华书局',2001,'司马迁',30.5,20,20),
	(104,'国外','Compiler Princple','Hust',2003,'Jun',155,5,5),
	(105,'教育','概率论与数理统计','中国教育出版社',2003,'小光',25.6,6,6),
	(106,'科技','PhotoShop 入门','中国科技出版社',2008,'军哥',20.4,10,10),
	(107,'人文','探索发现','地质出版社',2007,'CCTV',80.9,14,14),
	(108,'文学','活着','中国青年出版社',1999,'老舍',94.65,13,13),
	(109,'技术','计算机科学','清华大学出版社',2003,'诸葛',18.98,5,5),
	(110,'医学','内科学','中国卫生出版社',2018,'主编',14.82,21,21),
	(111,'历史','资治通鉴','新华书局',2001,'司马迁',62.69,20,20),
	(112,'国外','Compiler Princple','Hust',1997,'Jul',53.07,22,22),
	(113,'教育','概率论与数理统计','中国教育出版社',2003,'小光',29.87,13,13),
	(114,'科技','PhotoShop 入门','中国科技出版社',1996,'军哥',31.6,26,26),
	(115,'人文','探索发现','地质出版社',2017,'CCTV',71.25,6,6),
	(116,'文学','活着','中国青年出版社',2010,'老舍',45.75,17,17),
	(117,'技术','计算机科学','清华大学出版社',2002,'诸葛',33.53,18,18),
	(118,'医学','内科学','中国卫生出版社',1998,'主编',23.25,17,17),
	(119,'历史','资治通鉴','新华书局',2007,'司马迁',82.11,23,23),
	(120,'国外','Compiler Princple','Hust',1995,'Aug',90.17,18,18),
	(121,'教育','概率论与数理统计','中国教育出版社',2004,'小光',98.64,2,2),
	(122,'科技','PhotoShop 入门','中国科技出版社',2004,'军哥',84.08,20,20),
	(123,'人文','探索发现','地质出版社',2017,'CCTV',14.25,15,15),
	(124,'文学','活着','中国青年出版社',2009,'老舍',62.85,18,18),
	(125,'技术','计算机科学','清华大学出版社',2016,'诸葛',65.36,17,17),
	(126,'医学','内科学','中国卫生出版社',1999,'主编',32.95,5,5),
	(127,'历史','资治通鉴','新华书局',2015,'司马迁',38.68,10,10),
	(128,'国外','Compiler Princple','Hust',2004,'Sep',47.05,13,13),
	(129,'教育','概率论与数理统计','中国教育出版社',2008,'小光',14.52,11,11),
	(130,'科技','PhotoShop 入门','中国科技出版社',2003,'军哥',72.73,5,5);

/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table readers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `readers`;

CREATE TABLE `readers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `department` varchar(256) DEFAULT NULL,
  `type` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

LOCK TABLES `readers` WRITE;
/*!40000 ALTER TABLE `readers` DISABLE KEYS */;

INSERT INTO `readers` (`id`, `name`, `department`, `type`)
VALUES
	(1,'殷明军','计算机学院','学生');

/*!40000 ALTER TABLE `readers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table records
# ------------------------------------------------------------

DROP TABLE IF EXISTS `records`;

CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reader_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `borrow_date` datetime DEFAULT NULL,
  `receive_date` datetime DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reader_id` (`reader_id`),
  KEY `book_id` (`book_id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`id`),
  CONSTRAINT `records_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `records_ibfk_3` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;

INSERT INTO `records` (`id`, `reader_id`, `book_id`, `borrow_date`, `receive_date`, `admin_id`)
VALUES
	(1,1,100,'2018-09-11 12:33:11','2018-04-20 00:36:50',1),
	(3,1,101,'2018-04-20 00:22:46','2018-04-20 00:36:58',1),
	(4,1,102,'2018-04-20 00:23:44','2018-04-20 00:36:54',1),
	(5,1,103,'2018-04-20 00:30:32','2018-04-20 00:36:45',1),
	(6,1,107,'2018-04-20 00:31:23','2018-04-20 00:36:36',1);

/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
