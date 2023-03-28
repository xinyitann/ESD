SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `property_management`
--
CREATE DATABASE IF NOT EXISTS `property_management` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `property_management`;
-- --------------------------------------------------------

--
-- Table structure for table `agent`
--
DROP TABLE IF EXISTS `property_images`;
DROP TABLE IF EXISTS `booking`;
DROP TABLE IF EXISTS `bids`;
DROP TABLE IF EXISTS `property`;
DROP TABLE IF EXISTS `auctions`;



DROP TABLE IF EXISTS `agent`;
CREATE TABLE IF NOT EXISTS `agent` (
  `agent_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `phone` varchar(8) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`agent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `agent`
--

INSERT INTO `agent` (`agent_id`, `name`, `phone`, `email`) VALUES
(1, 'Luke Pang', '93750285', 'lukepang@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `phone` varchar(8) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_id`, `name`, `phone`, `email`) VALUES
(1, 'Apple TAN', '83848811', 'appletan@gmail.com');


-- --------------------------------------------------------
DROP TABLE IF EXISTS property_images;
CREATE TABLE property_images(
    `propertyID_image` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`img` mediumBLOB,
	`property_id` int(11) NOT NULL,
    PRIMARY KEY(`propertyID_image`)
);

--
-- Table structure for table `auctions`

DROP TABLE IF EXISTS `auctions`;
CREATE TABLE IF NOT EXISTS `auctions` (
  `auction_id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` TIMESTAMP NOT NULL,
  `end_time` TIMESTAMP NOT NULL,
  `starting_price` FLOAT(53) NOT NULL,
  `option_fee` FLOAT(53) NOT NULL,
  `highest_bid` FLOAT(2),
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`auction_id`)
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `auctions` (`auction_id`, `start_time`, `end_time`, `starting_price`,`option_fee`, `highest_bid`, `created_at`, `updated_at`)VALUES 
('1', '2023-03-23 12:00:00', '2023-03-27 12:00:00', '13150000','1000', '20000', '2023-03-20 12:00:00','2023-03-20 12:00:00');


-- Table structure for table `bids`
DROP TABLE IF EXISTS `bids`;
CREATE TABLE IF NOT EXISTS `bids` (
  `bid_id`int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `bid_amount` FLOAT(53) NOT NULL,
  `created_at` DATETIME  NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME  NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`bid_id`),
  constraint bids_fk1 foreign key (auction_id) references auctions(auction_id),
  constraint bids_fk2 foreign key (customer_id) references customer(customer_id)
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `bids` (`bid_id`, `auction_id`, `customer_id`, `bid_amount`, `created_at`, `updated_at`)VALUES 
('1', '1', '1', '22250000','2023-03-22 12:00:00','2023-03-22 12:00:00');

-- Table structure for table `property`
DROP TABLE IF EXISTS property;
CREATE TABLE IF NOT EXISTS property (
  `property_id` int NOT NULL AUTO_INCREMENT,
  `auction_id` int(11) NOT NULL,
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
  `neighbourhood` varchar(45) NOT NULL,
  `image` varchar(255) NOT NULL, -- store the file path instead of varbinary data
  PRIMARY KEY (`property_id`),
  constraint property_fk1 foreign key (agent_id) references agent(agent_id),
  constraint property_fk2 foreign key (customer_id) references customer(customer_id),
  constraint property_fk3 foreign key (auction_id) references auctions(auction_id)
);


--
-- Dumping data for table `property`
INSERT INTO `property` (`property_id`, `auction_id`, `agent_id`,`customer_id`, `name`, `address`, `postalcode`,`property_type`, `square_feet`, `room`, `facing`,`build_year`, `estimated_cost`,`neighbourhood`,`image`) VALUES
('1','1','1','1', 'Waterfront condominium', 'waterfront street 17', '123456', 'Condominium','5929',  '4', 'north','2011', '13150000','Bishan','../src/assets/backgroundhome.jpg');


DROP TABLE IF EXISTS property_images;
CREATE TABLE property_images(
    `propertyID_image` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`img` mediumBLOB,
	`property_id` int(11) NOT NULL,
    PRIMARY KEY(`propertyID_image`),
	constraint property_images_fk1 foreign key (property_id) references property(property_id)
);

-- Table structure for table `booking`
DROP TABLE IF EXISTS booking;
CREATE TABLE IF NOT EXISTS booking (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `property_id` int(11) NOT NULL,
  `datetime` timestamp NOT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`booking_id`),
  constraint booking_fk1 foreign key (agent_id) references agent(agent_id),
  constraint booking_fk2 foreign key (customer_id) references customer(customer_id),
  constraint booking_fk3 foreign key (property_id) references property(property_id)
);

--
-- Dumping data for table `property`
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetime`, `status`) VALUES
('1','1','1','1','2023-03-11 14:00:00','accepted' );

--
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
CREATE TABLE IF NOT EXISTS `error` (
  `error_id` int(11) NOT NULL AUTO_INCREMENT,
  `error_message` varchar(50) NOT NULL,
  PRIMARY KEY (`error_id`)
);

--
-- Dumping data for table `error`
INSERT INTO `error` (`error_id`,`error_message`)
VALUES ('1', 'Error: Booking is no longer available');


DROP TABLE IF EXISTS `extra`;
CREATE TABLE IF NOT EXISTS `extra` (
  `extra_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`extra_id`)
  
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
INSERT INTO `extra` (`extra_id`)VALUES 
('1');
