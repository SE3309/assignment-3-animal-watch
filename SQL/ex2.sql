-- ============================================================
-- EX2.SQL — Clean, Simplified, BCNF-Compliant Database
-- ============================================================
USE WildlifeTravelDB;
-- ============================================================
-- DROP TABLES IN REVERSE DEPENDENCY ORDER
-- ============================================================
DROP TABLE IF EXISTS ReviewPhoto;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Sighting;
DROP TABLE IF EXISTS SpeciesHabitat;
DROP TABLE IF EXISTS Species;
DROP TABLE IF EXISTS ItineraryDailySchedule;
DROP TABLE IF EXISTS ItineraryDestination;
DROP TABLE IF EXISTS Itinerary;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS CorporateAccount;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Location;

-- ============================================================
-- 1. USER
-- ============================================================
CREATE TABLE User (
    userEmail VARCHAR(255) PRIMARY KEY,
    phoneNo VARCHAR(20) UNIQUE,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    password VARCHAR(255),
    dateOfBirth DATE,
    country VARCHAR(100),
    joinDate DATE
);

-- ============================================================
-- 2. CORPORATE ACCOUNT
-- ============================================================
CREATE TABLE CorporateAccount (
    cAccountID INT PRIMARY KEY,
    companyName VARCHAR(255) UNIQUE
);

-- ============================================================
-- 3. TRIP
-- ============================================================
CREATE TABLE Trip (
    tripID INT PRIMARY KEY,
    userEmail VARCHAR(255), 
    cAccountID INT,
    tripName VARCHAR(255),
    destination VARCHAR(255),
    startDate DATE,
    endDate DATE,
    budget DECIMAL(10,2),
    FOREIGN KEY (userEmail) REFERENCES User(userEmail),
    FOREIGN KEY (cAccountID) REFERENCES CorporateAccount(cAccountID)
);

-- ============================================================
-- 4. ITINERARY
-- ============================================================
CREATE TABLE Itinerary (
    itineraryID INT PRIMARY KEY,
    tripID INT,
    FOREIGN KEY (tripID) REFERENCES Trip(tripID)
);

-- Multiple destinations per itinerary
CREATE TABLE ItineraryDestination (
    itineraryID INT,
    destination VARCHAR(255),
    PRIMARY KEY (itineraryID, destination),
    FOREIGN KEY (itineraryID) REFERENCES Itinerary(itineraryID)
);

-- Daily schedule per itinerary
CREATE TABLE ItineraryDailySchedule (
    itineraryID INT,
    dayNumber INT,
    activity VARCHAR(500),
    PRIMARY KEY (itineraryID, dayNumber),
    FOREIGN KEY (itineraryID) REFERENCES Itinerary(itineraryID)
);

-- ============================================================
-- 5. LOCATION
-- ============================================================
CREATE TABLE Location (
    locationID INT PRIMARY KEY,
    name VARCHAR(255),
    region VARCHAR(255),
    entryFee DECIMAL(10,2),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    type VARCHAR(100),
    description TEXT,
    UNIQUE(latitude, longitude)
);

-- ============================================================
-- 6. SPECIES
-- ============================================================
CREATE TABLE Species (
    speciesID INT PRIMARY KEY,
    specificName VARCHAR(255) UNIQUE,
    commonName VARCHAR(255),
    conservationStatus VARCHAR(100),
    description TEXT
);

-- Habitat (the only meaningful multi-valued species attribute you kept)
CREATE TABLE SpeciesHabitat (
    speciesID INT,
    habitat VARCHAR(255),
    PRIMARY KEY (speciesID, habitat),
    FOREIGN KEY (speciesID) REFERENCES Species(speciesID)
);

-- ============================================================
-- 7. SIGHTING
-- ============================================================
CREATE TABLE Sighting (
    sightingID INT PRIMARY KEY,
    speciesID INT,
    locationID INT,
    itineraryID INT,
    observedAt DATETIME,
    userEmail VARCHAR(255),
    FOREIGN KEY (speciesID) REFERENCES Species(speciesID),
    FOREIGN KEY (locationID) REFERENCES Location(locationID),
    FOREIGN KEY (itineraryID) REFERENCES Itinerary(itineraryID),
    FOREIGN KEY (userEmail) REFERENCES User(userEmail)
);

-- ============================================================
-- 8. REVIEW
-- ============================================================
CREATE TABLE Review (
    reviewID INT PRIMARY KEY,
    userEmail VARCHAR(255),
    locationID INT,
    rating INT,
    reviewText TEXT,
    datePosted DATE,
    helpfulCount INT,
    FOREIGN KEY (userEmail) REFERENCES User(userEmail),
    FOREIGN KEY (locationID) REFERENCES Location(locationID)
);

-- Photos attached to reviews
CREATE TABLE ReviewPhoto (
    reviewID INT,
    photoSeq INT,
    photoURL VARCHAR(500),
    PRIMARY KEY (reviewID, photoSeq),
    FOREIGN KEY (reviewID) REFERENCES Review(reviewID)
);

DESCRIBE User;
DESCRIBE Trip;
DESCRIBE Location;
DESCRIBE Sighting;

