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
  CONSTRAINT `fk_bidding_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bidding`
--

INSERT INTO `bidding` (`start_date`, `end_date`, `option_fee`, `highest_bid`, `customer_id`)
VALUES ('2023-03-20 08:00:00', '2023-03-22 08:00:00', 1000.00, 1500.00, 1);
