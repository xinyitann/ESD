CREATE DATABASE IF NOT EXISTS property DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE property;


-- Table structure for table `property`
DROP TABLE IF EXISTS property;
CREATE TABLE IF NOT EXISTS property (
  `property_id` int NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `address` varchar(45) NOT NULL,
  `postalcode` int(11) NOT NULL,
  `property_type` varchar(45) NOT NULL,
  `square_feet` int(11) NOT NULL,
  `room` int(11) NOT NULL,
  `facing` varchar(45)NOT NULL ,
  `build_year` int(11) NOT NULL,
  `estimated_cost` float(53) NOT NULL,
  `image` varbinary(50) NOT NULL,
  PRIMARY KEY (`property_id`)
);


--
-- Dumping data for table `property`
INSERT INTO `property` (`property_id`, `agent_id`,`customer_id`, `name`, `address`, `postalcode`,`property_type`, `square_feet`, `room`, `facing`,`build_year`, `estimated_cost`,`image`) VALUES
('1','1','1', 'Waterfront condominium', 'waterfront street 17', '123456', 'Condominium','5929',  '4', 'north','2011', '13150000','');


