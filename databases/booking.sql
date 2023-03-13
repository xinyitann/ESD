CREATE DATABASE IF NOT EXISTS booking DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE booking;


-- Table structure for table `booking`
DROP TABLE IF EXISTS booking;
CREATE TABLE IF NOT EXISTS booking (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `property_id` int(11) NOT NULL,
  `datetime` timestamp NOT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`booking_id`)
);

--
-- Dumping data for table `property`
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetime`, `status`) VALUES
('1','1','1','1','2023-03-11 14:00:00','accepted' );


