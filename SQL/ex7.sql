-- EX7.SQL — Views on WildlifeTravelDB

USE WildlifeTravelDB;

DROP VIEW IF EXISTS vw_CanadianUsers;

CREATE VIEW vw_CanadianUsers AS
SELECT
    userEmail,
    firstName,
    lastName,
    country,
    joinDate
FROM User
WHERE country = 'Canada';

SELECT * FROM vw_CanadianUsers LIMIT 10;

INSERT INTO vw_CanadianUsers (
    userEmail, firstName, lastName, country, joinDate
) VALUES (
    'canadian.new@example.com',
    'New', 'Canadian', 'Canada', '2024-11-01'
);

SELECT * FROM User
WHERE userEmail = 'canadian.new@example.com';

DROP VIEW IF EXISTS vw_LocationReviewStats;

CREATE VIEW vw_LocationReviewStats AS
SELECT
    L.locationID,
    L.name,
    COUNT(R.reviewID) AS reviewCount,
    AVG(R.rating)     AS avgRating
FROM Location L
JOIN Review   R ON L.locationID = R.locationID
GROUP BY L.locationID, L.name;

SELECT * FROM vw_LocationReviewStats;

INSERT INTO vw_LocationReviewStats (
    locationID, name, reviewCount, avgRating
)
VALUES (999, 'Imaginary Park', 10, 4.5);
