use 3yp;
ALTER TABLE User DROP FOREIGN KEY user_fk1;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Friend;
DROP TABLE IF EXISTS Profile;
DROP TABLE IF EXISTS ProfileTransition;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Transition;
DROP TABLE IF EXISTS Cube;

CREATE TABLE User (
	id INT AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	email VARCHAR(50) UNIQUE,
	default_cube INT,
	PRIMARY KEY(id)
) ENGINE InnoDB;

CREATE TABLE Profile (
	id INT AUTO_INCREMENT,
	name VARCHAR(30),
	creator_id INT,
	describe_line VARCHAR(30),
	side1 VARCHAR(30),
	side2 VARCHAR(30),
	side3 VARCHAR(30),
	side4 VARCHAR(30),
	side5 VARCHAR(30),
	side6 VARCHAR(30),
	PRIMARY KEY(id),
	FOREIGN KEY `Profile`(`creator_id`)
		REFERENCES `User`(`id`)
		ON UPDATE CASCADE
) ENGINE InnoDB;

CREATE TABLE Cube (
	id INT AUTO_INCREMENT,
	current_profile INT,
	current_rotation INT,
	secret_key VARCHAR(56),
	owner INT,
	unique_id VARCHAR(6),
	public BOOL,
	PRIMARY KEY(id),
	FOREIGN KEY (`owner`)
		REFERENCES `User`(`id`)
) ENGINE InnoDB;

CREATE TABLE ProfileTransition (
	id INT AUTO_INCREMENT,
	profile_id INT,
	time DATETIME,
	cube_id INT,
	PRIMARY KEY(id),
	FOREIGN KEY (`profile_id`)
		REFERENCES `Profile`(`id`),
		
	FOREIGN KEY (`cube_id`)
		REFERENCES `Cube`(`id`)
) ENGINE InnoDB;

CREATE TABLE Friend (
	user1 INT,
	user2 INT,
	FOREIGN KEY (`user1`)
		REFERENCES `User`(`id`),
		
	FOREIGN KEY (`user2`)
		REFERENCES `User`(`id`)
) ENGINE InnoDB;

CREATE TABLE Transition (
	id INT AUTO_INCREMENT,
	position INT(6),
	time DATETIME,
	cube_id INT,
	PRIMARY KEY(id),
	FOREIGN KEY (`cube_id`)
		REFERENCES `Cube`(`id`)
) ENGINE InnoDB;

CREATE TABLE Event (
	id INT AUTO_INCREMENT,
	owner INT,
	cube_id INT,
	action VARCHAR(30),
	profile_id INT,
	rotation INT,
	seen datetime,
	PRIMARY KEY(id),
	FOREIGN KEY (`cube_id`)
		REFERENCES `Cube`(`id`)
	FOREIGN KEY (`owner`)
		REFERENCES `User`(`id`)
	FOREIGN KEY (`profile_id`)
		REFERENCES `Profile`(`id`)
) ENGINE InnoDB;

CREATE TABLE ApiKey (
	id INT AUTO_INCREMENT,
	user_id INT,
	api_key VARCHAR(128),
	created DATETIME,
	PRIMARY KEY(id),
	FOREIGN KEY (`user_id`)
		REFERENCES `User`(`id`)
) ENGINE InnoDB;

ALTER TABLE User ADD CONSTRAINT user_fk1 FOREIGN KEY `User`(`default_cube`)
		REFERENCES `Cube`(`id`)
		ON DELETE CASCADE
		ON UPDATE CASCADE

