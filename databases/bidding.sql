SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `bidding`
--
CREATE DATABASE IF NOT EXISTS `bidding` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bidding`;
-- --------------------------------------------------------

--
-- Table structure for table `bidding`
--

DROP TABLE IF EXISTS `bidding`;
CREATE TABLE IF NOT EXISTS `bidding` (
  `bidding_id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` timestamp NOT NULL,
  `end_date` timestamp NOT NULL,
  `option_fee` float(53) NOT NULL,
  `highest_bid` float(53) NOT NULL,
  PRIMARY KEY (`bidding_id`)
  
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;