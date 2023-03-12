SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `agent`
--
CREATE DATABASE IF NOT EXISTS `agent` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `agent`;
-- --------------------------------------------------------

--
-- Table structure for table `agent`
--

DROP TABLE IF EXISTS `agent`;
CREATE TABLE IF NOT EXISTS `agent` (
  `agent_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `phone` varchar(8) NOT NULL,
  `email` varchar(20) NOT NULL,
  PRIMARY KEY (`agent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


--
-- Dumping data for table `order`
--

INSERT INTO `agent` (`agent_id`, `name`, `phone`, `email`) VALUES
(1, 'Luke Pang', '93750285', 'lukepang@gmail.com');

-- --------------------------------------------------------