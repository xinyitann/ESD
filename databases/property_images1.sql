CREATE DATABASE IF NOT EXISTS property_images DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE property_images;

-- Table structure for table `property_images`
DROP TABLE IF EXISTS property_images;
CREATE TABLE property_images.pic (
`propertyID_image` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
`img` mediumBLOB,
PRIMARY KEY(`propertyID_image`)
)
ENGINE = InnoDB;

insert into pic(propertyID_image,img) values(1,'//Users//perlineong//Documents//SMU//AY 2022-2023//IS 214 - ESD//project//Databases//property_images_upload');

