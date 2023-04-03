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
INSERT INTO agent (agent_id, name, phone, email) VALUES
(2, 'Lea Johnson', '84760934', 'leajohnson@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(3, 'Maxwell Lee', '93745823', 'maxwelllee@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(4, 'Amy Wong', '94752038', 'amywong@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(5, 'Tommy Tan', '83857684', 'tommytan@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(6, 'Samantha Lim', '92340567', 'samanthalim@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(7, 'William Ng', '81027546', 'williamng@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(8, 'Cindy Goh', '94562189', 'cindygoh@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(9, 'John Lee', '83104759', 'johnlee@gmail.com');
INSERT INTO agent (agent_id, name, phone, email) VALUES
(10, 'Elaine Tan', '91283476', 'elainetan@gmail.com');


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
INSERT INTO customer (customer_id, name, phone, email) VALUES
(2, 'Benjamin LIM', '94562189', 'benjaminlim@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(3, 'Cheryl LEE', '92340567', 'cheryllee@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(4, 'David WONG', '81027546', 'davidwong@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(5, 'Emily TAN', '91283476', 'emilytan@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(6, 'Frankie NG', '83104759', 'frankieng@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(7, 'Grace TAN', '93750285', 'gracetan@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(8, 'Henry LIM', '84760934', 'henrylim@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(9, 'Isabelle GOH', '93745823', 'isabellegoh@gmail.com');
INSERT INTO customer (customer_id, name, phone, email) VALUES
(10, 'Jason LEE', '94752038', 'jasonlee@gmail.com');

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
  `customer_id` INT NOT NULL,
  `starting_price` FLOAT(53) NOT NULL,
  `option_fee` FLOAT(53) NOT NULL,
  `highest_bid` FLOAT(2),
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`auction_id`),
  constraint auctions_fk1 foreign key (customer_id) references customer(customer_id)
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `auctions` (`auction_id`, `customer_id`, `starting_price`,`option_fee`, `highest_bid`, `created_at`, `updated_at`, `status`)VALUES 
('1', '1', '13150000','1000', '20000', '2023-03-20 12:00:00','2023-03-20 12:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('2', '2', '15000000', '2000', '25000', '2023-03-21 10:00:00', '2023-03-21 10:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('3', '3', '12000000', '1500', '18000', '2023-03-22 14:00:00', '2023-03-22 14:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('4', '4', '16500000', '3000', '35000', '2023-03-23 16:00:00', '2023-03-23 16:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('5', '5', '14200000', '1800', '21000', '2023-03-24 09:00:00', '2023-03-24 09:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('6', '6', '12750000', '1200', '15000', '2023-03-25 11:00:00', '2023-03-25 11:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('7', '7', '13800000', '2200', '27000', '2023-03-26 13:00:00', '2023-03-26 13:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('8', '8', '15750000', '2700', '32000', '2023-03-27 15:00:00', '2023-03-27 15:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('9', '9', '11450000', '900', '12000', '2023-03-28 17:00:00', '2023-03-28 17:00:00', 'open');
INSERT INTO auctions (auction_id, customer_id, starting_price, option_fee, highest_bid, created_at, updated_at, status) VALUES
('10', '2', '18500000', '2500', '31000', '2023-03-29 10:00:00', '2023-03-29 10:00:00', 'open');


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
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('2', '2', '2', '27000000', '2023-03-23 14:00:00', '2023-03-23 14:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('3', '3', '3', '14250000', '2023-03-24 16:00:00', '2023-03-24 16:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('4', '4', '4', '36500000', '2023-03-25 09:00:00', '2023-03-25 09:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('5', '5', '5', '15250000', '2023-03-26 11:00:00', '2023-03-26 11:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('6', '6', '6', '13500000', '2023-03-27 13:00:00', '2023-03-27 13:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('7', '7', '7', '28000000', '2023-03-28 15:00:00', '2023-03-28 15:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('8', '8', '8', '37250000', '2023-03-29 17:00:00', '2023-03-29 17:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('9', '9', '9', '14750000', '2023-03-30 10:00:00', '2023-03-30 10:00:00');
INSERT INTO bids (bid_id, auction_id, customer_id, bid_amount, created_at, updated_at) VALUES
('10', '10', '2', '39000000', '2023-03-31 12:00:00', '2023-03-31 12:00:00');

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
('1','1','1','1', 'Waterfront condominium', 'waterfront street 17', '123456', 'Condominium','5929',  '4', 'north','2011', '13150000','Bishan','room1.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('2', '2', '2', '2', 'HDB flat in Punggol', 'Punggol field street 2', '654321', 'HDB', '1076', '3', 'south', '2005', '27000000', 'Punggol', 'room2.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('3', '3', '3', '3', 'Condominium in Jurong', 'Jurong west street 41', '555555', 'Condominium', '1281', '3', 'east', '2010', '14250000', 'Jurong', 'room3.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('4', '4', '4', '4', 'Luxury house in Sentosa Cove', 'Sentosa cove street 1', '098765', 'Landed', '7500', '5', 'south', '2015', '36500000', 'Sentosa', 'room4.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('5', '5', '5', '5', 'HDB in Bukit Batok', 'Bukit Batok street 22', '222222', 'HDB', '1076', '3', 'west', '1995', '15250000', 'Bukit Batok', 'room5.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('6', '6', '6', '6', 'Condominium in Clementi', 'Clementi street 1', '456789', 'Condominium', '1087', '3', 'north', '2008', '13500000', 'Clementi', 'room6.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('7','7','7','7', 'Luxury Condo', 'Grange Road', '249583', 'Condominium','2000', '4', 'west','2015', '4500000','Orchard','room7.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('8','8','8','8', 'Spacious HDB', 'Tampines Street 45', '523465', 'HDB','1000', '3', 'north','2000', '450000','Tampines','room8.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('9','9','9','9', 'Good Class Bungalow', 'Ridout Road', '248745', 'Detached House','10000', '6', 'east','1990', '20000000','Tanglin','room9.jpg');
INSERT INTO property (property_id, auction_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood, image) VALUES
('10','10','10','10', 'City Fringe Condo', 'Jalan Besar', '208792', 'Condominium','800', '2', 'south','2010', '1000000','Jalan Besar','room10.jpg');


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
  `datetimestart` timestamp NOT NULL,
  `datetimeend` timestamp NOT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`booking_id`),
  constraint booking_fk1 foreign key (agent_id) references agent(agent_id),
  constraint booking_fk2 foreign key (customer_id) references customer(customer_id),
  constraint booking_fk3 foreign key (property_id) references property(property_id)
);

-- Dumping data for table `booking`
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('1','1','1','1','2023-03-11 14:00:00', '2023-03-11 15:00:00','pending' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('2','2','2','2','2023-03-12 10:00:00', '2023-03-12 11:00:00','confirmed' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('3','3','3','3','2023-03-13 14:00:00', '2023-03-13 15:00:00','pending' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('4','4','4','4','2023-03-14 11:00:00', '2023-03-14 12:00:00','cancelled' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('5','5','5','5','2023-03-15 15:00:00', '2023-03-15 16:00:00','confirmed' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('6','6','6','6','2023-03-16 10:00:00', '2023-03-16 11:00:00','pending' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('7','7','7','7','2023-03-17 14:00:00', '2023-03-17 15:00:00','confirmed' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('8','8','8','8','2023-03-18 11:00:00', '2023-03-18 12:00:00','pending' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('9','9','9','9','2023-03-19 15:00:00', '2023-03-19 16:00:00','confirmed' );
INSERT INTO `booking` (`booking_id`,`agent_id`,`customer_id`, `property_id`,`datetimestart`, `datetimeend`, `status`) VALUES
('10','10','10','10','2023-03-20 10:00:00', '2023-03-20 11:00:00','pending' );

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

